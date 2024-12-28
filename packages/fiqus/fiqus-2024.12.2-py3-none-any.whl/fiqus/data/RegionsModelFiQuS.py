from pydantic import BaseModel
from typing import List, Dict, Union, Optional


class Region(BaseModel):
    name: Optional[str] = None
    number: Optional[int] = None


class Regions(BaseModel):
    names: Optional[List[str]] = None
    numbers: Optional[List[int]] = None


class TwoParBoundaryRegions(BaseModel):
    names: Optional[List[List[str]]] = None
    numbers: Optional[List[List[int]]] = None
    values: Optional[List[List[Union[float, str]]]] = None


class OneParBoundaryRegions(BaseModel):
    names: Optional[List[List[str]]] = None
    numbers: Optional[List[List[int]]] = None
    value: Optional[List[float]] = None


class PoweredRegions(BaseModel):
    names: Optional[List[str]] = None
    numbers: Optional[List[int]] = None
    currents: Optional[List[float]] = None
    sigmas: Optional[List[float]] = None
    mu_rs: Optional[List[float]] = None


class InducedRegions(BaseModel):
    names: Optional[List[str]] = None
    numbers: Optional[List[int]] = None
    sigmas: Optional[List[float]] = None
    mu_rs: Optional[List[float]] = None


class InsulatorRegions(BaseModel):
    names: Optional[List[str]] = None
    numbers: Optional[List[int]] = None
    sigmas: Optional[List[float]] = None
    mu_rs: Optional[List[float]] = None


class IronRegions(BaseModel):
    names: Optional[List[str]] = None
    numbers: Optional[List[int]] = None
    sigmas: Optional[List[float]] = None
    mu_rs: Optional[List[float]] = None


class AirRegion(BaseModel):
    name: Optional[str] = None
    number: Optional[int] = None
    sigma: Optional[float] = None
    mu_r: Optional[float] = None


class AirFarFieldRegions(BaseModel):
    names: Optional[List[str]] = None
    numbers: Optional[List[int]] = None
    radius_in: Optional[float] = None
    radius_out: Optional[float] = None


class NonPermeableSourceRegion(BaseModel):
    name: Optional[str] = None
    number: Optional[int] = None
    sigma: Optional[float] = None
    mu_r: Optional[float] = None


class SourceFreeRegion(BaseModel):
    name: Optional[str] = None
    number: Optional[int] = None
    sigma: Optional[float] = None
    mu_r: Optional[float] = None


class Powered(BaseModel):
    vol: PoweredRegions = PoweredRegions()  # volume region
    vol_in: Region = Region()  # input terminal volume region
    vol_out: Region = Region()  # input terminal volume region
    conductors: Dict[str, List[str]] = {}  # conductor types
    surf: Regions = Regions()  # surface region
    surf_th: Regions = Regions()  # surface region
    surf_in: Regions = Regions()  # input terminal surface region
    surf_out: Regions = Regions()  # output terminal surface region
    cochain: Regions = Regions()  # winding cochain (cut)
    curve: Regions = Regions()  # powered volumes lines


class Induced(BaseModel):
    vol: InducedRegions = InducedRegions()  # volume region
    surf_th: Regions = Regions()  # surface region
    surf_in: Regions = Regions()  # input terminal surface region
    surf_out: Regions = Regions()  # output terminal surface region
    cochain: Regions = Regions()  # winding cochain (cut)


class Insulator(BaseModel):
    vol: InsulatorRegions = InsulatorRegions()  # volume region
    surf: Regions = Regions()  # surface region
    curve: Regions = Regions()  # curve region


class Iron(BaseModel):
    vol: IronRegions = IronRegions()  # volume region
    surf: Regions = Regions()  # surface region


class Air(BaseModel):
    vol: AirRegion = AirRegion()  # volume region
    surf: Region = Region()  # surface region
    line: Region = Region()  # line region
    point: Regions = Regions()  # point region
    cochain: Regions = Regions()  # air cochain (cut)


class AirFarField(BaseModel):
    vol: AirFarFieldRegions = AirFarFieldRegions()  # volume region
    surf: Region = Region()  # surface region


class NonPermeableSource(BaseModel):
    vol: NonPermeableSourceRegion = NonPermeableSourceRegion()  # volume region
    surf: Region = Region()  # surface region


class SourceFree(BaseModel):
    vol: SourceFreeRegion = SourceFreeRegion()  # volume region
    surf: Region = Region()  # surface region


class RobinCondition(BaseModel):
    bc: TwoParBoundaryRegions = TwoParBoundaryRegions()
    groups: Dict[str, List[int]] = {}


class NeumannCondition(BaseModel):
    bc: OneParBoundaryRegions = OneParBoundaryRegions()
    groups: Dict[str, List[int]] = {}


class DirichletCondition(BaseModel):
    bc: OneParBoundaryRegions = OneParBoundaryRegions()
    groups: Dict[str, List[int]] = {}


class ThermalBoundaryConditions(BaseModel):
    temperature: DirichletCondition = DirichletCondition()
    heat_flux: NeumannCondition = NeumannCondition()
    cooling: RobinCondition = RobinCondition()


class SymmetryBoundaryConditions(BaseModel):
    normal_free: Region = Region()
    tangential_free: Region = Region()


class BoundaryConditions(BaseModel):
    thermal: ThermalBoundaryConditions = ThermalBoundaryConditions()
    symmetry: SymmetryBoundaryConditions = SymmetryBoundaryConditions()


class InsulationType(BaseModel):
    layers_number: List[int] = []
    thin_shells: List[List[int]] = []
    layers_material: List[List[str]] = []
    thicknesses: List[List[float]] = []
    label: List[List[Union[int, None]]] = (
        []
    )  # useful to indicate which quench heater a SS element refers to


class ThinShell(BaseModel):
    groups: Dict[str, List[int]] = {}
    mid_turns_layers_poles: Optional[List[int]] = None
    second_group_is_next: Dict[str, List[int]] = {}
    normals_directed: Dict[str, List[int]] = {}
    insulation_types: InsulationType = InsulationType()
    quench_heaters: InsulationType = InsulationType()


class PostProc(BaseModel):
    vol: Regions = Regions()  # postprocessing volumes general
    surf: Regions = Regions()  # postprocessing volumes general
    line: Regions = Regions()  # postprocessing volumes general
    point: Regions = Regions()  # postprocessing volumes general


class RegionsModel(BaseModel):
    powered: Dict[str, Powered] = {}
    induced: Dict[str, Induced] = {}
    insulator: Insulator = Insulator()
    iron: Iron = Iron()
    air: Air = Air()
    air_far_field: AirFarField = AirFarField()
    thin_shells: ThinShell = ThinShell()
    projection_points: Region = Region()
    boundaries: BoundaryConditions = BoundaryConditions()
    postproc_th: PostProc = PostProc()
    postproc_em: PostProc = PostProc()


# if __name__ == "__main__":
#     write = True
#     read = False
#
#     def read_regions(regions_file_name):
#         with open(regions_file_name, 'r') as stream:
#             yaml_str = ruamel.yaml.safe_load(stream)
#         return RegionsModel(**yaml_str)
#
#     def flist(x):
#         retval = ruamel.yaml.comments.CommentedSeq(x)
#         retval.fa.set_flow_style()  # fa -> format attribute
#         return retval
#
#     if write:
#         model = RegionsModel()
#         model.powered.vol = [1, 2]
#         data_dict = model.dict()
#         yaml = ruamel.yaml.YAML()
#         yaml.default_flow_style = False
#         yaml.emitter.alt_null = 'Null'
#
#         def my_represent_none(self, data):
#             return self.represent_scalar('tag:yaml.org,2002:null', 'null')
#
#         yaml.representer.add_representer(type(None), my_represent_none)
#         with open('cct_regions_empty.yaml', 'w') as yaml_file:
#             yaml.dump(model.dict(), yaml_file)
#     if read:
#         regions_file_name = 'cct1_regions_manual.yaml'
#         regions = read_regions(regions_file_name)
