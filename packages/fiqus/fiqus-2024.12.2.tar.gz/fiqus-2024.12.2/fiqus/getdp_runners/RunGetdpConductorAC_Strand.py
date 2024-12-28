import timeit
import logging
import os
import subprocess
import re
import pandas as pd
import pickle
import numpy as np

import gmsh

from fiqus.utils.Utils import GmshUtils, FilesAndFolders
from fiqus.data.RegionsModelFiQuS import RegionsModel
import fiqus.data.DataFiQuSConductor as geom
from fiqus.geom_generators.GeometryConductorAC_Strand import TwistedStrand

from fiqus.pro_assemblers.ProAssembler import ASS_PRO

logger = logging.getLogger(__name__)

class Solve:
    def __init__(self, fdm, GetDP_path, geometry_folder, mesh_folder, verbose=True):
        self.fdm = fdm
        self.cacdm = fdm.magnet
        self.GetDP_path = GetDP_path
        self.solution_folder = os.path.join(os.getcwd())
        self.magnet_name = fdm.general.magnet_name
        self.geometry_folder = geometry_folder
        self.mesh_folder = mesh_folder
        self.mesh_file = os.path.join(self.mesh_folder, f"{self.magnet_name}.msh")
        self.pro_file = os.path.join(self.solution_folder, f"{self.magnet_name}.pro")
        self.regions_file = os.path.join(mesh_folder, f"{self.magnet_name}.regions")
        
        self.verbose = verbose
        self.gu = GmshUtils(self.solution_folder, self.verbose)
        self.gu.initialize()

        self.ass_pro = ASS_PRO(os.path.join(self.solution_folder, self.magnet_name))
        self.regions_model = FilesAndFolders.read_data_from_yaml(self.regions_file, RegionsModel)
        self.material_properties_model = None

        self.ed = {} # excitation dictionary

        gmsh.option.setNumber("General.Terminal", verbose)

    def read_excitation(self, inputs_folder_path):
        """
        Function for reading a CSV file for the 'from_file' excitation case.

        :param inputs_folder_path: The full path to the folder with input files.
        :type inputs_folder_path: str
        """
        if self.cacdm.solve.source_parameters.source_type == 'piecewise' and self.cacdm.solve.source_parameters.piecewise.source_csv_file:
            input_file = os.path.join(inputs_folder_path, self.cacdm.solve.source_parameters.piecewise.source_csv_file)
            print(f'Using excitation from file: {input_file}')
            df = pd.read_csv(input_file, delimiter=',', engine='python')
            excitation_time = df['time'].to_numpy(dtype='float').tolist()
            self.ed['time'] = excitation_time
            excitation_value = df['value'].to_numpy(dtype='float').tolist()
            self.ed['value'] = excitation_value

    def get_solution_parameters_from_yaml(self, inputs_folder_path):
        """
        Function for reading material properties from the geometry YAML file.

        This reads the 'solution' section of the YAML file and stores it in the solution folder.
        This could also be a place to change the material properties in the future.

        :param inputs_folder_path: The full path to the folder with input files.
        :type inputs_folder_path: str
        """
        if self.cacdm.geometry.io_settings.load.load_from_yaml:
            #load the geometry class from the pkl file
            geom_save_file = os.path.join(self.geometry_folder, f'{self.magnet_name}.pkl')
            with open(geom_save_file, "rb") as geom_save_file: 
                geometry_class: TwistedStrand = pickle.load(geom_save_file)
            
            input_yaml_file = os.path.join(inputs_folder_path, self.cacdm.geometry.io_settings.load.filename)
            Conductor_dm = FilesAndFolders.read_data_from_yaml(input_yaml_file, geom.Conductor)
            solution_parameters = Conductor_dm.Solution

            # The geometry YAML file lists surfaces to exclude from the TI problem by their IDs. Here we convert these IDs to Gmsh physical surface tags.
            # This is done by comparing the outer boundary points of the surfaces to exclude with the outer boundary points of the matrix partitions.
            surfaces_excluded_from_TI_tags = []

            for surface_ID in solution_parameters.Surfaces_excluded_from_TI: # 1) Find the outer boundary points of the surfaces to exclude
                outer_boundary_points_a = []
                outer_boundary_curves_a = Conductor_dm.Geometry.Areas[surface_ID].Boundary
                for curve_ID in outer_boundary_curves_a:
                    curve = Conductor_dm.Geometry.Curves[curve_ID]
                    for point_ID in curve.Points:
                        point = Conductor_dm.Geometry.Points[point_ID]
                        outer_boundary_points_a.append(tuple(point.Coordinates))
                
                for matrix_partition in geometry_class.matrix: # 2) Find the outer boundary points of the matrix partitions
                    outer_boundary_points_b = []
                    outer_boundary_curves_b = matrix_partition.boundary_curves
                    if len(outer_boundary_curves_b) == len(outer_boundary_curves_a): # If the number of boundary curves is different, the surfaces are not the same
                        for curve in outer_boundary_curves_b:
                            for point in curve.points:
                                outer_boundary_points_b.append(tuple(point.pos))
                        
                        if np.allclose(sorted(outer_boundary_points_a), sorted(outer_boundary_points_b)): # If the outer boundary points are the same, the surfaces are the same
                            surfaces_excluded_from_TI_tags.append(matrix_partition.physical_surface_tag) # 3) Add the physical surface tag to the list of surfaces to exclude
                            break
            
            solution_parameters.Surfaces_excluded_from_TI = surfaces_excluded_from_TI_tags # Replace the surface IDs with the physical surface tags

            FilesAndFolders.write_data_to_yaml(os.path.join(self.solution_folder, "MaterialProperties.yaml"), solution_parameters.dict())
            self.material_properties_model = solution_parameters

        


    def assemble_pro(self):
        print("Assembling .pro file")
        self.ass_pro.assemble_combined_pro(template = self.cacdm.solve.pro_template, rm = self.regions_model, dm = self.fdm, ed=self.ed, mp=self.material_properties_model)

    def run_getdp(self, solve = True, postOperation = True, gui = False):

        command = ["-v2", "-verbose", "3"]
        if solve: 
            command += ["-solve", "MagDyn"]
        if self.cacdm.solve.formulation_parameters.dynamic_correction:
            command += ["-pos", "MagDyn", "MagDyn_dynCorr"]
        else:
            command += ["-pos", "MagDyn"]


        startTime = timeit.default_timer()
        getdpProcess = subprocess.Popen([self.GetDP_path, self.pro_file, "-msh", self.mesh_file] + command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        with getdpProcess.stdout:
            for line in iter(getdpProcess.stdout.readline, b""):
                line = line.decode("utf-8").rstrip()
                line = line.split("\r")[-1]
                if not "Test" in line:
                    if line.startswith("Info"):
                        parsedLine = re.sub(r"Info\s+:\s+", "", line)
                        logger.info(parsedLine)
                    elif line.startswith("Warning"):
                        parsedLine = re.sub(r"Warning\s+:\s+", "", line)
                        logger.warning(parsedLine)
                    elif line.startswith("Error"):
                        parsedLine = re.sub(r"Error\s+:\s+", "", line)
                        logger.error(parsedLine)
                        logger.error("Solving CAC failed.")
                        # raise Exception(parsedLine)
                    elif re.match("##", line):
                        logger.critical(line)
                    else:
                        logger.info(line)
        
        simulation_time = timeit.default_timer()-startTime
        # Save simulation time:
        if solve:
            logger.info(f"Solving CAC_1 has finished in {round(simulation_time, 3)} seconds.")
            with open(os.path.join(self.solution_folder, 'test_temporary', 'simulation_time.txt'), 'w') as file:
                file.write(str(simulation_time))


        if gui and ((postOperation and not solve) or (solve and postOperation and self.cacdm.postproc.generate_pos_files)):
            # gmsh.option.setNumber("Geometry.Volumes", 1)
            # gmsh.option.setNumber("Geometry.Surfaces", 1)
            # gmsh.option.setNumber("Geometry.Curves", 1)
            # gmsh.option.setNumber("Geometry.Points", 0)
            posFiles = [
                fileName
                for fileName in os.listdir(self.solution_folder)
                if fileName.endswith(".pos")
            ]
            for posFile in posFiles:
                gmsh.open(os.path.join(self.solution_folder, posFile))
            self.gu.launch_interactive_GUI()
        else:
            gmsh.clear()
            gmsh.finalize()

    def cleanup(self):
        """
            This funtion is used to remove .msh, .pre and .res files from the solution folder, as they may be large and not needed.
        """
        magnet_name = self.fdm.general.magnet_name
        cleanup = self.cacdm.postproc.cleanup

        if cleanup.remove_res_file:
            res_file_path = os.path.join(self.solution_folder, f"{magnet_name}.res")
            if os.path.exists(res_file_path):
                os.remove(res_file_path)
                logger.info(f"Removed {magnet_name}.res")
        
        if cleanup.remove_pre_file:
            pre_file_path = os.path.join(self.solution_folder, f"{magnet_name}.pre")
            if os.path.exists(pre_file_path):
                os.remove(pre_file_path)
                logger.info(f"Removed {magnet_name}.pre")

        if cleanup.remove_msh_file:
            msh_file_path = os.path.join(self.mesh_folder, f"{magnet_name}.msh")
            if os.path.exists(msh_file_path):
                os.remove(msh_file_path)
                logger.info(f"Removed {magnet_name}.msh")