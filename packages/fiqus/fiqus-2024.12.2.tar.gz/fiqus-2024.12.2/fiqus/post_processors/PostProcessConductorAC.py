import os
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
from matplotlib.animation import FuncAnimation
import pandas as pd
from scipy import integrate, interpolate
from typing import (List, Literal, Callable)
from pydantic import BaseModel

from fiqus.utils.Utils import FilesAndFolders as Util
from fiqus.data.DataFiQuSConductorAC_Strand import CACStrandSolve, CACStrandPostproc, CACStrandMesh, CACStrandGeometry
from fiqus.plotters.PlotPythonConductorAC import PlotPython, SimulationData


class PostProcess:
    """
    This class loads and stores the data from a simulation and can apply various postprocessing operations on the data. 
    The simulation data is saved as a SimulationData object.
    """
    def __init__(self, fdm, model_data_output_path) -> None:
        self.fdm = fdm
        self.model_data_output_path = model_data_output_path
        self.geometry_name = f"Geometry_{self.fdm.run.geometry}"
        self.mesh_name = f"Mesh_{self.fdm.run.mesh}"
        self.solution_name = f"Solution_{self.fdm.run.solution}"

        self.simulation_data = SimulationData(model_data_output_path, self.geometry_name, self.mesh_name, self.solution_name)

    def plot_instantaneous_loss(self):
        print("Total loss: ", self.simulation_data.cumulative_power["TotalLoss"].iloc[-1])
        print("Total filament loss: ", self.simulation_data.cumulative_power["FilamentLoss"].iloc[-1])
        print("Total coupling loss: ", self.simulation_data.cumulative_power["CouplingLoss"].iloc[-1])
        print("Total eddy loss: ", self.simulation_data.cumulative_power["EddyLoss"].iloc[-1])
        plot_options = self.fdm.magnet.postproc.plot_instantaneous_power
        self.simulation_data.plot_instantaneous_power(
            show=plot_options.show, 
            title=plot_options.title, 
            save_plot=plot_options.save, 
            save_folder_path=os.path.join(self.model_data_output_path, self.geometry_name, self.mesh_name, self.solution_name),
            save_file_name=plot_options.save_file_name,
            overwrite=self.fdm.run.overwrite
            )





