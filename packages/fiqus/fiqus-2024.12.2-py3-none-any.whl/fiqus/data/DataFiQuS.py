from pydantic import BaseModel, Field
from typing import Dict, List, Union, Literal, Optional
from fiqus.data.DataRoxieParser import RoxieData
from fiqus.data.DataFiQuSCCT import CCTDM
from fiqus.data.DataFiQuSMultipole import Multipole
from fiqus.data.DataFiQuSPancake3D import Pancake3D
from fiqus.data.DataConductor import Conductor
from fiqus.data.DataFiQuSConductorAC_Strand import CACStrand


class FiQuSGeometry(BaseModel):
    """
    Class for Roxie data
    """

    Roxie_Data: RoxieData = RoxieData()


class RunFiQuS(BaseModel):
    """
    Class for FiQuS run
    """

    type: Literal[
        "start_from_yaml",
        "mesh_only",
        "geometry_only",
        "geometry_and_mesh",
        "pre_process_only",
        "mesh_and_solve_with_post_process_python",
        "solve_with_post_process_python",
        "solve_only",
        "post_process_getdp_only",
        "post_process_python_only",
        "post_process",
        "plot_python",
        "batch_post_process_python",
    ] = Field(
        default="start_from_yaml",
        title="Run Type of FiQuS",
        description="FiQuS allows you to run the model in different ways. The run type can be specified here. For example, you can just create the geometry and mesh or just solve the model with previous mesh, etc.",
    )
    geometry: Optional[Union[str, int]] = Field(
        default=None,
        title="Geometry Folder Key",
        description="This key will be appended to the geometry folder.",
    )
    mesh: Optional[Union[str, int]] = Field(
        default=None,
        title="Mesh Folder Key",
        description="This key will be appended to the mesh folder.",
    )
    solution: Optional[Union[str, int]] = Field(
        default=None,
        title="Solution Folder Key",
        description="This key will be appended to the solution folder.",
    )
    launch_gui: bool = Field(
        default=False,
        title="Launch GUI",
        description="If True, the GUI will be launched after the run.",
    )
    overwrite: bool = Field(
        default=False,
        title="Overwrite",
        description="If True, the existing folders will be overwritten, otherwise new folders will be created. NOTE: This setting has no effect for HTCondor runs.",
    )
    comments: str = Field(
        default="",
        title="Comments",
        description="Comments for the run. These comments will be saved in the run_log.csv file.",
    )
    verbosity_Gmsh: int = Field(
        default=5,
        title="verbosity_Gmsh",
        description="Level of information printed on the terminal and the message console (0: silent except for fatal errors, 1: +errors, 2: +warnings, 3: +direct, 4: +information, 5: +status, 99: +debug)",
    )
    verbosity_GetDP: int = Field(
        default=5,
        title="verbosity_GetDP",
        description="Level of information printed on the terminal and the message console. Higher number prints more, good options are 5 or 6.",
    )
    verbosity_FiQuS: bool = Field(
        default=True,
        title="verbosity_FiQuS",
        description="Level of information printed on the terminal and the message console by FiQuS. Only True of False for now.",
    )


class GeneralFiQuS(BaseModel):
    """
    Class for FiQuS general
    """

    magnet_name: Optional[str] = None


class EnergyExtraction(BaseModel):
    """
    Level 3: Class for FiQuS
    """

    t_trigger: Optional[float] = None
    R_EE: Optional[float] = None
    power_R_EE: Optional[float] = None
    L: Optional[float] = None
    C: Optional[float] = None


class QuenchHeaters(BaseModel):
    """
    Level 3: Class for FiQuS
    """

    N_strips: Optional[int] = None  # set to 0 to avoid building quench heater thin shells
    t_trigger: Optional[List[float]] = None
    U0: Optional[List[float]] = None
    C: Optional[List[float]] = None
    R_warm: Optional[List[float]] = None
    w: Optional[List[float]] = None
    h: Optional[List[float]] = None
    h_ins: List[List[float]] = []
    type_ins: List[List[str]] = []
    h_ground_ins: List[List[float]] = []
    type_ground_ins: List[List[str]] = []
    l: Optional[List[float]] = None
    l_copper: Optional[List[float]] = None
    l_stainless_steel: Optional[List[float]] = None
    ids: Optional[List[int]] = None
    turns: Optional[List[int]] = None
    turns_sides: Optional[List[str]] = None


class Cliq(BaseModel):
    """
    Level 3: Class for FiQuS
    """

    t_trigger: Optional[float] = None
    current_direction: Optional[List[int]] = None
    sym_factor: Optional[int] = None
    N_units: Optional[int] = None
    U0: Optional[float] = None
    C: Optional[float] = None
    R: Optional[float] = None
    L: Optional[float] = None
    I0: Optional[float] = None


class Circuit(BaseModel):
    """
    Level 2: Class for FiQuS
    """

    R_circuit: Optional[float] = None
    L_circuit: Optional[float] = None
    R_parallel: Optional[float] = None


class PowerSupply(BaseModel):
    """
    Level 2: Class for FiQuS
    """

    I_initial: Optional[float] = None
    t_off: Optional[float] = None
    t_control_LUT: Optional[List[float]] = Field(
        default=None,
        title="Time Values for Current Source",
        description="This list of time values will be matched with the current values in I_control_LUT, and then these (t, I) points will be connected with straight lines.",
    )
    I_control_LUT: Optional[List[float]] = Field(
        default=None,
        title="Current Values for Current Source",
        description="This list of current values will be matched with the time values in t_control_LUT, and then these (t, I) points will be connected with straight lines.",
    )
    R_crowbar: Optional[float] = None
    Ud_crowbar: Optional[float] = None


class QuenchProtection(BaseModel):
    """
    Level 2: Class for FiQuS
    """

    energy_extraction: EnergyExtraction = EnergyExtraction()
    quench_heaters: QuenchHeaters = QuenchHeaters()
    cliq: Cliq = Cliq()

class QuenchDetection(BaseModel):
    """
    Level 2: Class for FiQuS
    """

    voltage_thresholds: Optional[List[float]] = Field(
        default=None,
        title="List of quench detection voltage thresholds",
        description="Voltage thresholds for quench detection. The quench detection will be triggered when the voltage exceeds these thresholds continuously for a time larger than the discrimination time.",
    )

    discrimination_times: Optional[List[float]] = Field(
        default=None,
        title="List of quench detection discrimination times",
        description="Discrimination times for quench detection. The quench detection will be triggered when the voltage exceeds the thresholds continuously for a time larger than these discrimination times.",
    )

    voltage_tap_pairs: Optional[List[List[int]]] = Field(
        default=None,
        title="List of quench detection voltage tap pairs",
        description="Voltage tap pairs for quench detection. The voltage difference between these pairs will be used for quench detection.",
    )

class FDM(BaseModel):
    """
    Class for FiQuS
    """

    general: GeneralFiQuS = GeneralFiQuS()
    run: RunFiQuS = RunFiQuS()
    magnet: Union[Multipole, CCTDM, Pancake3D, CACStrand] = Field(
        default=Multipole(), discriminator="type"
    )
    circuit: Circuit = Circuit()
    power_supply: PowerSupply = PowerSupply()
    quench_protection: QuenchProtection = QuenchProtection()
    quench_detection: QuenchDetection = QuenchDetection()
    conductors: Dict[Optional[str], Conductor] = {}
