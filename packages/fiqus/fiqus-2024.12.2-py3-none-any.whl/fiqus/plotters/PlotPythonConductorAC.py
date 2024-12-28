import os
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.animation import FuncAnimation
import pandas as pd
from scipy import integrate, interpolate
from ruamel.yaml import YAML
import subprocess

# from fiqus.utils.Utils import FilesAndFolders as Util
# from fiqus.data.DataFiQuSConductorAC_Strand import CACStrandSolve, CACStrandPostproc, CACStrandMesh, CACStrandGeometry

def create_non_overwriting_filepath(folder_path, base_name, extension, overwrite):
        """
            Creates a filepath that does not overwrite any existing files.

            This function checks if a file already exists at the specified filepath. If the file exists and `overwrite` is False, 
            it modifies the filepath to create a new file instead of overwriting the existing one. 
            If `overwrite` is True or the file does not exist, it returns the filepath as it is.

            Parameters
            ----------
            folder_path : str
                The path to the folder where the file will be created.
            base_name : str
                The base name of the file.
            extension : str
                The extension of the file.
            overwrite : bool, optional
                If True, the function will overwrite an existing file. If False, the function will modify the filepath to avoid overwriting. Defaults to False.

            Returns
            -------
            str
                The final filepath. If `overwrite` is False and a file already exists at the original filepath, this will be a new filepath that does not overwrite any existing files.
        """
        if os.path.exists(os.path.join(folder_path, base_name+extension)) and not overwrite:
            counter = 1
            new_name = base_name + f"_{counter}" + extension
            while os.path.exists(os.path.join(folder_path, new_name)):
                new_name = base_name + f"_{counter}" + extension
                counter += 1
            return os.path.join(folder_path, new_name)

        return os.path.join(folder_path, base_name+extension)

class YamlWrapper:
    """
    A wrapper class for YAML data that allows accessing dictionary data using dot notation.
    """
    def __init__(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                value = YamlWrapper(value)
            self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__.get(item)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

def load_yaml(file_path):
    """
    Load a YAML file and return the data as a YamlWrapper object. This enables accessing the data using dot notation (e.g., data.key.subkey), without needing a predefined pydantic model, allowing for better backwards compatibility.
    """
    yaml = YAML()
    with open(file_path, 'r') as file:
        data = yaml.load(file)
    return YamlWrapper(data)

def is_latex_installed():
    """
    Check if LaTeX is installed on the system.
    """
    try:
        subprocess.run(['pdflatex', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

class SimulationData:
    """
    Class used to store and manage data from a single simulation.

    This class is responsible for loading and organizing the data from a single simulation. 
    It stores the data in various attributes and provides methods for retrieving and processing the data.

    """
    def __init__(self, model_data_output_path, geometry_name, mesh_name, solution_name) -> None:
        self.model_data_output_path = model_data_output_path # This is the path to the folder where the model output data is stored (e.g. geometries)
        self.geometry_name = geometry_name # Name of the geometry folder
        self.mesh_name = mesh_name # Name of the mesh folder 
        self.solution_name = solution_name # Name of the solution folder

        # Organize the folders:
        self.geometry_folder = os.path.join(self.model_data_output_path, geometry_name) # Path to the geometry folder
        self.mesh_folder = os.path.join(self.geometry_folder, mesh_name) # Path to the mesh folder
        self.solution_folder = os.path.join(self.mesh_folder, solution_name) # Path to the solution folder

        # Store the YAML input-files in a data model, fdm:
        self.geometry, self.mesh, self.solve = self.retrieve_fiqusDataModel()

        # Store losses, simulation time and check if the simulation crashed:
        temp_file_path = os.path.join(self.solution_folder, 'test_temporary')
        loss_file = [f for f in os.listdir(temp_file_path) if f.startswith('power') and f.endswith('.txt')][0]
        self.power_columns = ['Time', 'FilamentLoss', 'CouplingLoss', 'EddyLoss', 'TotalLoss', 'CouplingLoss_dyn', 'TotalLoss_dyn'] # Only in the case dynamic correction is used, must be changed later
        self.power = pd.read_csv(os.path.join(self.solution_folder, 'test_temporary', loss_file), sep = ' ', names=self.power_columns) # Store instantaneous losses as pandas dataframe
        self.crash = True if 'crash_report.txt' in os.listdir(temp_file_path) else False

        # Add a row of zeros at the beginning of the dataframe to account for the initial condition:
        self.power = pd.concat([pd.DataFrame({col: 0 for col in self.power_columns}, index=[0]), self.power]).reset_index(drop=True)
        # Integrate the losses to obtain the cumulative power and the total power per cycle:
        self.cumulative_power, self.total_power_per_cycle = self.integrate_power() # Store cumulative power and total cumulative power per cycle
        # Store simulation time:
        try:
            with open(os.path.join(self.solution_folder, 'test_temporary', 'simulation_time.txt'), 'r') as f: 
                self.simulation_time = float(f.readline().strip())
        except:
            self.simulation_time = None # If the simulation time file does not exist, the simulation has not finished running.

        # Store the rest of the post-processing data:
        self.time = self.power['Time']
        self.instantaneous_temperature = self.load_standard_data(os.path.join(temp_file_path, 'temperature.txt'), 1, add_initial_zero=True)
        self.temperature = self.load_standard_data(os.path.join(temp_file_path, 'temperature.txt'), 2, add_initial_zero=True)
        self.I_transport = self.load_standard_data(os.path.join(temp_file_path, 'I_transport.txt'), 1)
        self.V_transport = self.load_standard_data(os.path.join(temp_file_path, 'V_transport.txt'), 1)
        self.hs_val = self.load_standard_data(os.path.join(temp_file_path, 'hs_val.txt'), 1)
        self.magn_fil = self.load_standard_data(os.path.join(temp_file_path, 'magn_fil.txt'), [1, 2, 3])
        self.magn_matrix = self.load_standard_data(os.path.join(temp_file_path, 'magn_matrix.txt'), [1, 2, 3])
        self.I = self.load_standard_data(os.path.join(temp_file_path, 'I.txt'), 1, len(self.time))
        self.V = self.load_standard_data(os.path.join(temp_file_path, 'V.txt'), 1, len(self.time))
        self.I_integral = self.load_standard_data(os.path.join(temp_file_path, 'I_integral.txt'), 1, len(self.time))
        self.I_abs_integral = self.load_standard_data(os.path.join(temp_file_path, 'I_abs_integral.txt'), 1, len(self.time))
        self.magnetic_energy_internal = self.load_standard_data(os.path.join(temp_file_path, 'magnetic_energy_internal.txt'), 1)
        self.Ip = self.load_standard_data(os.path.join(temp_file_path, 'Ip.txt'), 1, len(self.time))
        self.Vp = self.load_standard_data(os.path.join(temp_file_path, 'Vp.txt'), 1, len(self.time))


    def load_standard_data(self, file_path, columns, reshape = None, add_initial_zero = False):
        """
        There are many output .txt-files with similar format. This function loads the data from one of these files and returns it as a numpy array.
        If the file does not exist, None is returned without raising an error.
        """
        try:
            data = np.loadtxt(file_path, comments='#', usecols=columns)
            if reshape:
                data = data.reshape(-1, reshape).T
        except IOError:
            return None

        if add_initial_zero:
            if len(data.shape) == 1:
                data = np.insert(data, 0, 0)
            else:
                zeros = np.zeros((1, data.shape[1]))
                data = np.vstack((zeros, data))
        return data

    def retrieve_fiqusDataModel(self):
        """
        This function reads the YAML input-files for geometry, mesh and solve and stores them in three dictionaries which are returned.
        This function is to be called only once, when the object is created.
        """
        geometry_dataModel = load_yaml(os.path.join(self.geometry_folder, 'geometry.yaml'))
        mesh_dataModel = load_yaml(os.path.join(self.mesh_folder, 'mesh.yaml'))
        solution_dataModel = load_yaml(os.path.join(self.solution_folder, 'solve.yaml'))

        return geometry_dataModel, mesh_dataModel, solution_dataModel

    def integrate_power(self):
        """ 
        This function integrates the instantaneous power over time to obtain the cumulative power. 
        It also calculates the total cumulative power per cycle.
        The cumulative power is returned as a pandas dataframe and the total cumulative power per cycle is returned as a dictionary.
        """
        find_closest_idx = lambda arr, val: np.abs(arr - val).argmin() 

        t = np.array(self.power['Time'])
        t_final = t[-1]
        t_init = find_closest_idx(t, t_final/2)
        
        cumulative_power = pd.DataFrame(columns= self.power_columns)
        total_power_per_cycle = {}

        cumulative_power['Time'] = self.power["Time"]
        for column in self.power_columns[1:]:
            cumulative_power[column] = np.insert(integrate.cumulative_trapezoid(self.power[column], t), 0, 0)
            total_power_per_cycle[column] = 2 * (cumulative_power[column].iloc[-1]-cumulative_power[column].iloc[t_init]) # / (np.pi*matrix_radius**2 * loss_factor) # Why do we divide by pi*matrix_radius**2*loss_factor?

        return cumulative_power, total_power_per_cycle
    
    def plot_instantaneous_power(self, show:bool = True, title:str = "Power", save_plot:bool = False, save_folder_path:str = None, save_file_name:str = None, overwrite:bool = False):
        plt.figure()
        plt.plot(self.power['Time'], self.power[self.power_columns[1:]] , label = self.power_columns[1:])
        plt.xlabel('Time [s]')
        plt.ylabel('Power [W/m]')
        plt.legend()

        # Configure title:
        # Class attributes can be accessed by using '<< ... >>' in the title string.
        commands = re.findall('<<(.*?)>>', title)
        for c in commands:
            title = title.replace(f"<<{c}>>", str(eval('self.'+c)))
        plt.title(title)


        if save_plot: # Save the plot
            filePath = create_non_overwriting_filepath(save_folder_path, save_file_name, '.png', overwrite)
            plt.savefig(filePath)

        if show: 
            plt.show()
        else:
            plt.close()

class PlotPython:
    """
    This class loads and stores the data from the simulations specified in a csv file and can apply various postprocessing operations on the data. 
    The data from each simulation is saved as a SimulationData object which is subsequently stored in a list in this class.
    """
    def __init__(self, fdm, csv_filename = None, lossMap_gridData_folder = None, inputs_folder_path='', outputs_folder_path='') -> None:
        self.fdm = fdm
        self.inputs_folder_path = inputs_folder_path # This is the path to the folder where the input data is stored
        self.model_data_output_path = outputs_folder_path # This is the path to the folder where the model output data is stored (e.g. geometries)
        self.outputs_folder_path = os.path.join(outputs_folder_path, fdm.magnet.postproc.batch_postproc.output_folder) # This is the path to the folder where the postprocessed data is written
        

        if not os.path.exists(self.outputs_folder_path):
            os.makedirs(self.outputs_folder_path)

        if csv_filename is not None:
            try:
                self.input_csv = pd.read_csv(os.path.join(self.inputs_folder_path, f'{csv_filename}.csv')) # Read the csv file with the input data
            except:
                raise FileNotFoundError(f'No csv file with the name {fdm.magnet.postproc.batch_postproc.postProc_csv}.csv was found in the inputs folder.')
            
            self.simulation_collection = self.retrieve_simulation_data()

            self.avg_simulation_time = np.mean([sd.simulation_time for sd in self.simulation_collection])
            self.total_simulation_time = np.sum([sd.simulation_time for sd in self.simulation_collection])

            print('Number of simulations considered: ', len(self.simulation_collection)	)
            print('Average simulation time: ', self.avg_simulation_time, 's')
            print('Total simulation time: ', self.total_simulation_time, 's')



        elif lossMap_gridData_folder is not None:
            self.input_csv = None
            self.simulation_collection = None

            self.totalLoss_gridData = self.load_lossMap_gridData('TotalLoss', lossMap_gridData_folder)
            self.filamentLoss_gridData = self.load_lossMap_gridData('FilamentLoss', lossMap_gridData_folder)
            self.eddyLoss_gridData = self.load_lossMap_gridData('EddyLoss', lossMap_gridData_folder)
            self.couplingLoss_gridData = self.load_lossMap_gridData('CouplingLoss', lossMap_gridData_folder)
        else:
            raise ValueError('No input data specified. Either a csv file or a folder with loss map grid data must be provided.')
            
        
        

    def retrieve_simulation_data(self):
        """
        This function iterates over the input CSV-file (specifying which simulations to postprocess) and returns a list of SimulationData objects
        containing all the simulation data. If no CSV-file is specified, the data from the single simulation specified in the input YAML-file is returned.
        """
        if self.input_csv is not None:
            simulationCollection = []
            for index, row in self.input_csv.iterrows():
                if pd.isna(row['input.run.geometry']) and pd.isna(row['input.run.mesh']) and pd.isna(row['input.run.solution']):
                    continue
                geometry_name = 'Geometry_'+str(row['input.run.geometry'])
                mesh_name = 'Mesh_'+str(row['input.run.mesh'])

                if isinstance(row['input.run.solution'], float) and row['input.run.solution'].is_integer():
                    solution_name = 'Solution_'+str(int(row['input.run.solution']))
                else:
                    solution_name = 'Solution_'+str(row['input.run.solution'])

                # Check if the row refers to a valid simulation by checking if the solution folder exists:
                # solution_folder = os.path.join(os.getcwd(), 'tests', '_outputs', self.fdm.general.magnet_name, geometry_name, mesh_name, solution_name)
                solution_folder = os.path.join(self.model_data_output_path, geometry_name, mesh_name, solution_name)
                if os.path.exists(solution_folder): # If the solution folder exists, add the simulation to the simulationCollection
                    sd = SimulationData(self.model_data_output_path, geometry_name, mesh_name, solution_name)
                    if sd.simulation_time is not None: # Only add the simulation if it has finished running (and therefore has written the simulation time to a file)
                        simulationCollection.append(sd)
        else:
            simulationCollection = [SimulationData(self.model_data_output_path, 'Geometry_'+self.fdm.run.geometry, 'Mesh_'+self.fdm.run.mesh, 'Solution_'+self.fdm.run.solution)]
        
        return self.sort_simulationCollection(self.filter_simulationCollection(simulationCollection))

    def filter_simulationCollection(self, simulationCollection):
        """ 
        This function is used to filter the simulationCollection based on the filter criterion specified in the yaml input file.
        An example of a filter criterion is '<<solve.source_parameters.sine.frequency>> == 18', which will disregard all simulations with frequency != 18Hz.
        """
        if self.fdm.magnet.postproc.batch_postproc.filter.apply_filter:
            filter_criterion = self.fdm.magnet.postproc.batch_postproc.filter.filter_criterion
            class_params = re.findall('<<(.*?)>>', filter_criterion)
            for cp in class_params:
                filter_criterion = filter_criterion.replace(f"<<{cp}>>", 'sd.'+cp)
            filtering_function = eval(f'lambda sd: {filter_criterion}')
            return list(filter(filtering_function, simulationCollection))
        else:
            return simulationCollection
    
    def sort_simulationCollection(self, simulationCollection):
        """ 
        This function is used to sort the simulationCollection based on the sort key specified in the yaml input file.
        An example of a sort key is 'solve.source_parameters.sine.frequency', which will sort the simulations based on frequency.
        """
        if self.fdm.magnet.postproc.batch_postproc.sort.apply_sort:
            sorting_function = eval(f'lambda sd: sd.{self.fdm.magnet.postproc.batch_postproc.sort.sort_key}')
            return sorted(simulationCollection, key=sorting_function)
        else:
            return simulationCollection

    def lossMap_createGridData(self, lossType = 'TotalLoss', x_val_to_include = None, y_val_to_include = None):
        """
        This function creates the grid data needed for the loss map, based on the yaml input file.
        Given a collection of simulations it interpolates the loss data between the datapoints to a grid and returns the grid data.
        """
        lm = self.fdm.magnet.postproc.batch_postproc.loss_map

        # Extract data from simulation collection and normalize
        x_arr = np.array([eval('sd.'+lm.x_val)/lm.x_norm for sd in self.simulation_collection])
        y_arr = np.array([eval('sd.'+lm.y_val)/lm.y_norm for sd in self.simulation_collection])
        loss = np.array([sd.total_power_per_cycle[lossType]/lm.loss_norm for sd in self.simulation_collection])

        # Logarithmic scaling
        if lm.x_log: x_arr = np.log10(x_arr)
        if lm.y_log: y_arr = np.log10(y_arr) 
        if lm.loss_log: loss = np.log10(loss)

        x_arr_interpolated = np.linspace(min(x_arr), max(x_arr), lm.x_steps)
        y_arr_interpolated = np.linspace(min(y_arr), max(y_arr), lm.y_steps)
        # Insert specific values to the grid if they are not already included (useful for cross sections)
        if x_val_to_include is not None and x_val_to_include not in x_arr_interpolated: 
            x_arr_interpolated = np.insert(x_arr_interpolated, np.where(x_arr_interpolated > x_val_to_include)[0][0], x_val_to_include)
        if y_val_to_include is not None and y_val_to_include not in y_arr_interpolated:
            y_arr_interpolated = np.insert(y_arr_interpolated, np.where(y_arr_interpolated > y_val_to_include)[0][0], y_val_to_include)

        # Create grid
        X, Y = np.meshgrid(x_arr_interpolated, y_arr_interpolated, indexing='ij')
        gridPoints = np.c_[X.ravel(), Y.ravel()]
        dataPoints = np.c_[x_arr, y_arr]

        # Interpolate the simulation data onto the grid
        V = interpolate.griddata(
            dataPoints,
            loss,
            gridPoints,
            method='linear' # Cubic produces cleaner plots. Any incentive to go back to linear?
        ).reshape(X.shape)

        return X, Y, V, dataPoints
    
    def save_lossMap_gridData(self, save_folder_name = 'lossMap_gridData'):
        """
        This function calls the lossMap_createGridData function and saves the grid data.
        """
        lm = self.fdm.magnet.postproc.batch_postproc.loss_map

        lossTypes = ['TotalLoss', 'FilamentLoss', 'EddyLoss', 'CouplingLoss', 'CouplingLoss_dyn', 'TotalLoss_dyn'] # Only in the case dynamic correction is used, must be changed later
        # 1) Create a folder to store the output files
        gridData_folder_path = create_non_overwriting_filepath(self.outputs_folder_path, save_folder_name, '', self.fdm.run.overwrite)
        if not os.path.exists(gridData_folder_path): os.makedirs(gridData_folder_path)
        # 2) Create the grid data for each loss type and save it
        for lossType in lossTypes:
            X, Y, V, _ = self.lossMap_createGridData(lossType)
            if lm.x_log: X = np.power(10, X)
            if lm.y_log: Y = np.power(10, Y)
            if lm.loss_log: V = np.power(10, V)
            np.savetxt(os.path.join(gridData_folder_path, f'{lossType}.txt'), np.column_stack((X.ravel(), Y.ravel(), V.ravel())), delimiter=' ', header=f'{lm.x_val} {lm.y_val} {lossType}', comments='')

    def load_lossMap_gridData(self, lossType = 'TotalLoss', save_folder_name = 'lossMap_gridData'):
        """
        This function loads the grid data for a given loss type.
        """
        lm = self.fdm.magnet.postproc.batch_postproc.loss_map
        gridData_folder_path = os.path.join(self.inputs_folder_path, save_folder_name)
        
        if not os.path.exists(gridData_folder_path):
            raise FileNotFoundError(f'The folder {gridData_folder_path} does not exist.')

        X, Y, V = np.loadtxt(os.path.join(gridData_folder_path, f'{lossType}.txt'), unpack=True, skiprows=1)

        if lm.x_log: X = np.log10(X)
        if lm.y_log: Y = np.log10(Y)
        if lm.loss_log: V = np.log10(V)

        # Get the unique counts of X and Y
        unique_X = np.unique(X)
        unique_Y = np.unique(Y)

        # Reshape the data
        X = X.reshape((len(unique_X), len(unique_Y)))
        Y = Y.reshape((len(unique_X), len(unique_Y)))
        V = V.reshape((len(unique_X), len(unique_Y)))

        return X, Y, V
    
    # def add_value_to_gridData(self, X, Y, V, x_val = None, y_val = None):
    #     """
    #     This function adds a value to the grid data.
    #     Steps: 
    #         1) Revert the grid data to 1D arrays
    #         2) Add x or y value or both to the arrays
    #         3) Reshape the arrays back to grid data, interpolating the loss to the new grid points
    #     """
    #     gridPoints 
    
    def save_magnetization(self):
        """
        This function saves the magnetization data for all simulations in the simulation collection.
        """
        magnetization_folder_path = create_non_overwriting_filepath(self.outputs_folder_path, 'magnetization', '', self.fdm.run.overwrite)
        if not os.path.exists(magnetization_folder_path): os.makedirs(magnetization_folder_path)
        for sd in self.simulation_collection:
            magnetization = sd.magn_fil + sd.magn_matrix
            magnetization = np.c_[sd.time, magnetization]
            np.savetxt(os.path.join(magnetization_folder_path, f'magn_f{sd.solve.source_parameters.sine.frequency}_b{sd.solve.source_parameters.sine.field_amplitude}_I{sd.solve.source_parameters.sine.current_amplitude}.txt'), magnetization, delimiter=' ', header='t x y z', comments='')
        
            


        
    
    def lossMap_crossSection(self, slice_value, axis_to_cut = 'x'):
        """
        This function returns the data corresponding to a cross section of the loss map, for all loss types.
        Given an axis and a value, it sweeps the other axis for the closest value and returns the data.
        Example: Given slice value 0 and axis x, it returns the data for the cross section at x = 0.
        """

        lm = self.fdm.magnet.postproc.batch_postproc.loss_map
        if axis_to_cut == 'x':
            x_val_to_include = slice_value
            y_val_to_include = None
        elif axis_to_cut == 'y':
            x_val_to_include = None
            y_val_to_include = slice_value
        X, Y, V, dataPoints = self.lossMap_createGridData('TotalLoss', x_val_to_include, y_val_to_include)
        _,_,FilamentLoss, _ = self.lossMap_createGridData('FilamentLoss', x_val_to_include, y_val_to_include)
        _,_,EddyLoss, _ = self.lossMap_createGridData('EddyLoss', x_val_to_include, y_val_to_include)
        _,_,CouplingLoss, _ = self.lossMap_createGridData('CouplingLoss', x_val_to_include, y_val_to_include)


        if axis_to_cut == 'x':
            index = np.abs(X[:, 0] - slice_value).argmin()
            slice_vals = Y[index, :]

        elif axis_to_cut == 'y':
            index = np.abs(Y[0, :] - slice_value).argmin()
            slice_vals = X[:, index]

        # Extract the loss values for the constant frequency across all applied fields
        totalLoss = V[index, :] if axis_to_cut == 'x' else V[:, index]
        filamentLoss = FilamentLoss[index, :] if axis_to_cut == 'x' else FilamentLoss[:, index]
        eddyLoss = EddyLoss[index, :] if axis_to_cut == 'x' else EddyLoss[:, index]
        couplingLoss = CouplingLoss[index, :] if axis_to_cut == 'x' else CouplingLoss[:, index]

        return slice_vals, totalLoss, filamentLoss, eddyLoss, couplingLoss

    def plot_lossMap_crossSection(self):
        """
        This function calls the lossMap_crossSection function and plots the data it returns, which is the loss for all values of one axis, given a constant value of the other axis.
        """
        
        if is_latex_installed():
            plt.rcParams['text.usetex'] = True
            plt.rcParams['font.family'] = 'times'
            plt.rcParams['font.size'] = 20

        lm = self.fdm.magnet.postproc.batch_postproc.loss_map
        slice_value = lm.cross_section.cut_value
        axis_to_cut = lm.cross_section.axis_to_cut

        if (lm.x_log and axis_to_cut == 'x') or (lm.y_log and axis_to_cut == 'y'): 
            slice_value = np.log10(slice_value)

        slice_vals, totalLoss, filamentLoss, eddyLoss, couplingLoss = self.lossMap_crossSection(slice_value, axis_to_cut = axis_to_cut)

        def log_formatter(x, pos):
            """
                Format the tick labels on the plot.
            """
            return f"$10^{{{int(x)}}}$"

        # Plot the loss with respect to applied field for the constant frequency
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(slice_vals, totalLoss, label=f'Total Loss')
        ax.plot(slice_vals, filamentLoss, label=f'Filament Loss')
        ax.plot(slice_vals, eddyLoss, label=f'Eddy Loss')
        ax.plot(slice_vals, couplingLoss, label=f'Coupling Loss')

        tick_formatter = FuncFormatter(log_formatter)
        if lm.x_log and axis_to_cut == 'y' or lm.y_log and axis_to_cut == 'x': 
            ax.xaxis.set_major_formatter(tick_formatter)
        if lm.loss_log:
            ax.yaxis.set_major_formatter(tick_formatter)
        
        
        title = lm.cross_section.title.replace('<<cut_value>>', str(round(10**slice_value, 3)))
        ax.set_title(title)
        ax.set_xlabel(lm.ylabel if axis_to_cut == 'x' else lm.xlabel)
        ax.set_ylabel(lm.cross_section.ylabel)
        ax.legend()

        # np.savetxt(os.path.join(self.outputs_folder_path, 'lossMaps_cut_0p2T_0A.txt'), np.column_stack((10**slice_vals, 10**totalLoss, 10**eddyLoss, 10**couplingLoss, 10**filamentLoss)), delimiter=' ', header='f total eddy coupling filament', comments='')

        if lm.cross_section.save_plot:
            filePath = create_non_overwriting_filepath(self.outputs_folder_path, lm.cross_section.filename, '.png', self.fdm.run.overwrite)
            plt.savefig(filePath)

        if self.fdm.run.launch_gui: plt.show()

    def animate_lossMap_crossSection(self):
        """
        This function is similar to the plot_lossMap_crossSection function, but instead of plotting the loss for at a constant crossection, 
        it sweeps the crossection over a chosen axis and plots the loss for each crossection as an animation.
        """
        lm = self.fdm.magnet.postproc.batch_postproc.loss_map
        axis = lm.cross_section_sweep.axis_to_sweep

        X, Y, V, dataPoints = self.lossMap_createGridData('TotalLoss')
        x_vals = X[:, 0] # x-values from the loss map
        y_vals = Y[0, :] # y-values from the loss map

        if axis == 'x':
            A = np.zeros((lm.y_steps, 4, lm.x_steps))
            axis_to_sweep = x_vals
            constant_axis = y_vals
        elif axis == 'y':
            A = np.zeros((lm.x_steps, 4, lm.y_steps))
            axis_to_sweep = y_vals
            constant_axis = x_vals


        for i, val in enumerate(axis_to_sweep):
            _, totalLoss, filamentLoss, eddyLoss, couplingLoss = self.lossMap_crossSection(val, axis_to_cut = axis)
            A[:, 0, i] = totalLoss
            A[:, 1, i] = filamentLoss
            A[:, 2, i] = eddyLoss
            A[:, 3, i] = couplingLoss
        
        # Initialize the plot
        fig, ax = plt.subplots()
        lines = ax.plot(constant_axis, A[:, :, 0], lw=2, label = ['total Loss', 'filament Loss', 'eddy Loss', 'coupling Loss'])

        # Set plot limits and labels
        ax.set_xlim(constant_axis[0], constant_axis[-1])
        ax.set_ylim(np.min(A), np.max(A))
        ax.set_xlabel(lm.ylabel if axis == 'x' else lm.xlabel)
        ax.set_ylabel(lm.cross_section_sweep.ylabel)


        # Define the animation update function
        def update(frame):
            for i, line in enumerate(lines):
                line.set_ydata(A[:, i, frame])
            
            if axis == 'x':
                if lm.x_log: 
                    sweep_value = 10**x_vals[frame]
                else:
                    sweep_value = x_vals[frame]
            elif axis == 'y':
                if lm.y_log:
                    sweep_value = 10**y_vals[frame]
                else:
                    sweep_value = y_vals[frame]

            title = lm.cross_section_sweep.title.replace('<<sweep_value>>', str(round(sweep_value, 3)))
            ax.set_title(title)
            return lines,# line1, line2, line3, line4

        # Create the animation
        dt = 0.1
        ani = FuncAnimation(fig, update, frames=lm.x_steps if axis == 'x' else lm.y_steps, interval=dt*1000, blit=False)

        # Show the animation
        plt.legend()
        plt.grid()
        
        if lm.cross_section_sweep.save_plot:
            filepath = create_non_overwriting_filepath(folder_path=self.outputs_folder_path, base_name=lm.cross_section_sweep.filename, extension='.gif', overwrite=self.fdm.run.overwrite)
            ani.save(filepath, writer='imagemagick', fps=1/dt)

        if self.fdm.run.launch_gui: plt.show()

    def create_lossMap(self):
        """
        This function creates a loss map based on the inputs given in the loss_map section of the input file.
        The loss-map can be plotted and saved as a .png file.
        """
        lm = self.fdm.magnet.postproc.batch_postproc.loss_map

        if self.simulation_collection:
            X, Y, V, dataPoints = self.lossMap_createGridData(lm.loss_type)
        else:
            X, Y, V = self.totalLoss_gridData

        if is_latex_installed():
            plt.rcParams['text.usetex'] = True
            plt.rcParams['font.family'] = 'times'
            plt.rcParams['font.size'] = 20

        fig, ax = plt.subplots(figsize=(10,8))
    
        c = plt.pcolormesh(X, Y, V, shading='gouraud', cmap='plasma_r')
        c_min = min([np.ceil(np.min(V)) for V in [V]])
        c_max = max([np.floor(np.max(V)) for V in [V]])
        c_ticks = [int(val) for val in np.arange(c_min, c_max+1)]
        cont = plt.contour(X,Y,V, c_ticks, colors='k', linestyles='dashed')
        
        if lm.show_datapoints: 
            plt.scatter(dataPoints[:, 0], dataPoints[:, 1], s=50, edgecolors='k')

        
        if lm.show_loss_type_dominance_contour:
            sigmoid = lambda x: 1/(1+np.exp(-x))
            if self.simulation_collection:
                _, _, FilamentLoss, _ = self.lossMap_createGridData(lossType='FilamentLoss')
                _, _, CouplingLoss, _ = self.lossMap_createGridData(lossType='CouplingLoss')
                _, _, EddyLoss, _ = self.lossMap_createGridData(lossType='EddyLoss')
            # else:
            #     _, _, FilamentLoss = self.filamentLoss_gridData
            #     _, _, CouplingLoss = self.couplingLoss_gridData
            #     _, _, EddyLoss = self.eddyLoss_gridData
            fil_vs_coupling_loss = np.maximum(FilamentLoss, EddyLoss) - CouplingLoss
            fil_vs_eddy_loss = EddyLoss - np.maximum(FilamentLoss, CouplingLoss)
            plt.contour(X,Y,sigmoid(fil_vs_coupling_loss),[0.5], colors='k')
            plt.contour(X,Y,sigmoid(fil_vs_eddy_loss),[0.5], colors='k')
        
        cbar = fig.colorbar(c, ticks=c_ticks)#, labels=c_labels)
        # cbar.ax.set_xticks([-7, -6, -5, -4, -3, -2, -1, 0, 1])
        # cbar.ax.set_yticklabels([r'$10^{-7}$', r'$10^{-6}$', r'$10^{-5}$', r'$10^{-4}$', r'$10^{-3}$', r'$10^{-2}$', r'$10^{-1}$', r'$10^0$', r'$10^1$'])
        cbar.ax.set_yticklabels([f"$10^{{{val}}}$" for val in c_ticks])
        # plt.grid(alpha=0.5)
        # plt.title(lm.title)
        # plt.xlabel(lm.xlabel)
        # plt.ylabel(lm.ylabel)
        plt.title(r'Loss per cycle (J/m)')
        plt.xlabel(r'Frequency $f$ (Hz)')
        plt.ylabel(r'Field amplitude $b$ (T)')


        # plt.annotate(r'Coupling', (np.log10(1.0), np.log10(0.007)), color='white')
        # plt.annotate(r'Filament', (np.log10(0.012), np.log10(0.74)), color='white')
        # plt.annotate(r'(uncoupled)', (np.log10(0.012), np.log10(0.55)), color='white')
        # plt.annotate(r'Filament', (np.log10(45), np.log10(0.38)), color='white')
        # plt.annotate(r'(coupled)', (np.log10(45), np.log10(0.28)), color='white')
        # plt.annotate(r'Eddy', (np.log10(2000), np.log10(0.03)), color='white')

        # ax.plot(np.log10(0.03), np.log10(0.2),  'o', color='white')#, xytext=(np.log10(0.03), np.log10(0.12)), arrowprops=dict(facecolor='black', shrink=0.02))
        # ax.plot(np.log10(30),   np.log10(1),    'o', color='white')#, xytext=(np.log10(40), np.log10(0.8)), arrowprops=dict(facecolor='black', shrink=0.02))
        # ax.plot(np.log10(3),    np.log10(0.2),  'o', color='white')#, xytext=(np.log10(2), np.log10(0.2)), arrowprops=dict(facecolor='black', shrink=0.02))
        # ax.plot(np.log10(5000), np.log10(0.2),  'o', color='white')#, xytext=(np.log10(5000), np.log10(0.1)), arrowprops=dict(facecolor='black', shrink=0.02))

        # ax.annotate('(a)', xy=(np.log10(0.03), np.log10(0.2)), xycoords='data', ha='right', va='bottom', fontsize=20, color='white')
        # ax.annotate('(b)', xy=(np.log10(3), np.log10(0.2)), xycoords='data', ha='right', va='bottom', fontsize=20, color='white')
        # ax.annotate('(c)', xy=(np.log10(30), np.log10(1)), xycoords='data', ha='right', va='bottom', fontsize=20, color='white')
        # ax.annotate('(d)', xy=(np.log10(5000), np.log10(0.2)), xycoords='data', ha='right', va='bottom', fontsize=20, color='white')

        # Define custom tick labels for x-axis
        x_min_log = int(np.log10(min([eval('sd.'+lm.x_val) for sd in self.simulation_collection])))
        x_max_log = int(np.log10(max([eval('sd.'+lm.x_val) for sd in self.simulation_collection])))
        x = np.arange(x_min_log, x_max_log+1)
        # Create a list of minor ticks
        minor_x_labels = []
        # 1) Add the ticks from x_min_log to ceil(x_min_log) to the minor_x_test list
        new_ticks = np.linspace(10.0**np.floor(x_min_log), 10.0**np.ceil(x_min_log), 10)[:-1]
        new_ticks = np.unique(new_ticks[new_ticks >= 10.0**x_min_log])
        minor_x_labels.extend(new_ticks)
        # 2) Add the ticks from ceil(x_min_log) to floor(x_max_log) to the minor_x_test list
        for x_val in x:
            new_ticks = np.linspace(10.0**x_val, 10.0**(x_val+1), 10)[1:-1]
            if x_val == x[-1]:
                new_ticks = new_ticks[new_ticks <= 10.0**x_max_log]
            minor_x_labels.extend(new_ticks)
        minor_x = [np.log10(val) for val in minor_x_labels]
        
        new_x_labels = [f"$10^{{{val}}}$" for val in x]
        plt.xticks(x, new_x_labels)
        plt.xticks(minor_x, minor=True)

        # Define custom tick labels for y-axis
        y_min_log = np.log10(min([eval('sd.'+lm.y_val) for sd in self.simulation_collection]))
        y_max_log = np.log10(max([eval('sd.'+lm.y_val) for sd in self.simulation_collection]))
        y = np.arange(np.ceil(y_min_log), np.floor(y_max_log)+1)
        # Create a list of minor ticks
        minor_y_labels = []
        # 1) Add the ticks from y_min_log to ceil(y_min_log) to the minor_y_test list
        new_ticks = np.linspace(10.0**np.floor(y_min_log), 10.0**np.ceil(y_min_log), 10)[:-1]
        new_ticks = np.unique(new_ticks[new_ticks >= 10.0**y_min_log])
        minor_y_labels.extend(new_ticks)
        # 2) Add the ticks from ceil(y_min_log) to floor(y_max_log) to the minor_y_test list
        for y_val in y:
            new_ticks = np.linspace(10.0**y_val, 10.0**(y_val+1), 10)[1:-1]
            if y_val == y[-1]:
                new_ticks = new_ticks[new_ticks <= 10.0**y_max_log]
            minor_y_labels.extend(new_ticks)

        new_y_labels = [f"$10^{{{int(val)}}}$" for val in y]
        minor_y = [np.log10(val) for val in minor_y_labels]
        plt.yticks(y, new_y_labels)
        plt.yticks(minor_y, minor=True)

        # plt.savefig('C:/Users/jdular/cernbox/Documents/Reports/CERN_Reports/linkedFluxPaper/fig/loss_map_54fil_noI.pdf', bbox_inches='tight')


        if lm.save_plot:
            filePath = create_non_overwriting_filepath(self.outputs_folder_path, lm.filename, '.pdf', self.fdm.run.overwrite)
            plt.savefig(filePath, bbox_inches='tight')

        if self.fdm.run.launch_gui: plt.show()


    def plot2d(self):  
        """
        This function is used to create a 2d plot. It is supposed to be flexible and work for various kinds of plots one may want to create.
        """
        if is_latex_installed():
            plt.rcParams['text.usetex'] = True
            plt.rcParams['font.family'] = 'times'
            # plt.rcParams['font.size'] = 20

        # Create the title (or titles if combined_plot is False)
        title = self.fdm.magnet.postproc.batch_postproc.plot2d.title
        if self.fdm.magnet.postproc.batch_postproc.plot2d.combined_plot:
            sd = self.simulation_collection[0]
            commands = re.findall('<<(.*?)>>', title)
            for c in commands:
                title = title.replace(f"<<{c}>>", str(eval('sd.'+c)))
        else:
            titles = []
            for sd in self.simulation_collection:
                commands = re.findall('<<(.*?)>>', title)
                title_i = title
                for c in commands:
                    title_i = title_i.replace(f"<<{c}>>", str(eval('sd.'+c)))
                titles.append(title_i)

        # Create the labels
        label_list = self.fdm.magnet.postproc.batch_postproc.plot2d.labels
        labels = np.zeros((len(self.simulation_collection), len(label_list)), dtype=object)
        for i, sd in enumerate(self.simulation_collection):
            simulation_labels = []
            for l in label_list:
                commands = re.findall('<<(.*?)>>', l)
                for c in commands:
                    l = l.replace(f"<<{c}>>", str(eval('sd.'+c)))

                simulation_labels.append(l)
            labels[i, :] = simulation_labels

        # colors = plt.cm.get_cmap('magma').resampled(len(self.simulation_collection)).colors
        colors = plt.cm.get_cmap('viridis').resampled(len(self.simulation_collection)).colors

        # Load the x-values:
        x_val = self.fdm.magnet.postproc.batch_postproc.plot2d.x_val
        commands = re.findall('<<(.*?)>>', x_val)
        for c in commands:
            x_val = x_val.replace(f"<<{c}>>", str('sd.'+c))
        x_arr = np.array([eval(x_val) for sd in self.simulation_collection], dtype=object)

        # Load the y-values:
        y_vals = self.fdm.magnet.postproc.batch_postproc.plot2d.y_vals
        y_arr = np.zeros((len(self.simulation_collection), len(y_vals)), dtype=object)
        for i, sd in enumerate(self.simulation_collection):
            for j, y_val in enumerate(y_vals):
                commands = re.findall('<<(.*?)>>', y_val)
                for c in commands:
                    y_val = y_val.replace(f"<<{c}>>", str('sd.'+c))
                y_arr[i, j] = eval(y_val)

        # data = np.column_stack((x_arr, y_arr))
        # np.savetxt(os.path.join(self.outputs_folder_path, self.fdm.magnet.postproc.batch_postproc.plot2d.filename+'.txt'), data, delimiter=' ', header='f total eddy coupling filament', comments='')

        
        

        # Plot and save the data:
        if not self.fdm.magnet.postproc.batch_postproc.plot2d.combined_plot and self.fdm.magnet.postproc.batch_postproc.plot2d.save_plot:  
            # Create a folder to save the plots if combined_plot is False and save_plot is True:  
            filename = self.fdm.magnet.postproc.batch_postproc.plot2d.filename
            folder_path = create_non_overwriting_filepath(self.outputs_folder_path, filename, '', self.fdm.run.overwrite)
            if not os.path.exists(folder_path): os.makedirs(folder_path)

        # Check if the y-values are all floats:
        y_is_float = np.all(np.apply_along_axis(lambda arr: np.all(np.vectorize(isinstance)(arr, float)), axis=1, arr=y_arr))
        # If they are all floats (not arrays), we can make a single plot, spanning all simulations, instead of one plot per simulation.
        if y_is_float:
            for column in range(y_arr.shape[1]):
                plt.plot(x_arr, y_arr[:, column], label=label_list[column])
            if self.fdm.magnet.postproc.batch_postproc.plot2d.legend:
                plt.legend()
            plt.grid()
            plt.xlabel(self.fdm.magnet.postproc.batch_postproc.plot2d.xlabel)
            plt.ylabel(self.fdm.magnet.postproc.batch_postproc.plot2d.ylabel)
            plt.title(title)
            if self.fdm.magnet.postproc.batch_postproc.plot2d.x_log:
                plt.xscale('log')
            if self.fdm.magnet.postproc.batch_postproc.plot2d.y_log:
                plt.yscale('log')

            if self.fdm.magnet.postproc.batch_postproc.plot2d.save_plot:
                filename = self.fdm.magnet.postproc.batch_postproc.plot2d.filename
                filePath = create_non_overwriting_filepath(self.outputs_folder_path, filename, '.png', self.fdm.run.overwrite)
                plt.savefig(filePath)

            
        else:
            for i, (x, y_vals_per_sim, labels_per_sim, color) in enumerate(zip(x_arr, y_arr, labels, colors)):
                if self.fdm.magnet.postproc.batch_postproc.plot2d.combined_plot:
                    # If combined_plot is true, plot all the data in the same figure:
                    # x_sin = 2*np.sin(2*np.pi*x/x.iloc[-1]) #temporary for missing hs_val
                    for y, label in zip(y_vals_per_sim, labels_per_sim):
                        # plt.plot(x_sin, x_sin+1.6*y, self.fdm.magnet.postproc.batch_postproc.plot2d.linestyle, label=label, color = color) #temporary for missing hs_val
                        plt.plot(x, y, self.fdm.magnet.postproc.batch_postproc.plot2d.linestyle, label=label, color = color)
                else:
                    # If combined_plot is false, plot data from each simulation in a separate figure:
                    plt.figure()
                    for y, label in zip(y_vals_per_sim, labels_per_sim):
                        plt.plot(x, y, self.fdm.magnet.postproc.batch_postproc.plot2d.linestyle, label=label)

                # Set the plot options
                if self.fdm.magnet.postproc.batch_postproc.plot2d.legend:
                    plt.legend()
                plt.grid()
                plt.xlabel(self.fdm.magnet.postproc.batch_postproc.plot2d.xlabel)
                plt.ylabel(self.fdm.magnet.postproc.batch_postproc.plot2d.ylabel)
                plt.title(title if self.fdm.magnet.postproc.batch_postproc.plot2d.combined_plot else titles[i])


                if not self.fdm.magnet.postproc.batch_postproc.plot2d.combined_plot and self.fdm.magnet.postproc.batch_postproc.plot2d.save_plot:
                    # If combined_plot is false we expect a lot of plots and save them all into a folder:
                    filename = self.fdm.magnet.postproc.batch_postproc.plot2d.filename
                    plt.savefig(os.path.join(folder_path, filename+f"_{i}.png"))

            if self.fdm.magnet.postproc.batch_postproc.plot2d.combined_plot and self.fdm.magnet.postproc.batch_postproc.plot2d.save_plot:
                # If combined_plot is true we expect only one plot and save it in the main folder:
                filename = self.fdm.magnet.postproc.batch_postproc.plot2d.filename
                filePath = create_non_overwriting_filepath(self.outputs_folder_path, filename, '.png', self.fdm.run.overwrite)
                plt.savefig(filePath, dpi=300)

        if self.fdm.run.launch_gui: plt.show()

    
