from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Optional


class Area(BaseModel):
    Material: Optional[str] = Field(
        None, description="Material of the area", examples=["Cu", "NbTi", "Nb3Sn"]
    )
    Boundary: List[int] = (
        []
    )  # List of curves that define the closed boundary of the area
    InnerBoundaries: List[List[int]] = (
        []
    )  # List of lists of curves that define the closed boundaries of the holes in the area
    BoundaryThickness: Optional[Optional[float]] = None  # Thickness of the boundary
    BoundaryMaterial: Optional[str] = Field(
        None,
        description="Material of the boundary",
        examples=["steel", "Cu", "direct", "etc."],
    )
    Layer: Optional[int] = Field(
        None,
        description="Filaments in the strand-model must be assigned to a layer. A layer is a collection of all filaments with the same radius from the center.",
    )
    LayerIndex: Optional[int] = Field(
        None, description="Index of the filament in the layer."
    )

# ========== GEOMETRY YAML CLASSES ========== #
class Material(BaseModel):
    Type: Optional[str] = Field(
        None, description="Type of material", examples=["NbTi", "Nb3Sn", "Cu"]
    )
    RRR: Optional[float] = Field(None, description="Residual resistivity ratio")
    T_ref_RRR_high: Optional[float] = Field(
        None, description="High reference temperature for RRR"
    )
    T_ref_RRR_low: Optional[float] = Field(
        None, description="Low reference temperature for RRR"
    )
    model_config = ConfigDict(frozen=True)


class Point(BaseModel):
    Coordinates: List[float] = []


class Curve(BaseModel):
    Type: str
    Points: List[int] = []

    Contact: Optional[str] = Field(
        None,
        description="If the curve is a contact layer between two surfaces this represents the contact type of strands",
        examples=["crossing", "parallel"],
    )
    Thickness: Optional[float] = Field(
        None, description="Thickness of the contact layer"
    )
    Material: Optional[str] = Field(
        None,
        description="Material of the contact layer",
        examples=["steel", "direct", "Cu"],
    )




class GeometryParameters(BaseModel):
    Points: Dict[int, Point] = {}
    Curves: Dict[int, Curve] = {}
    Areas: Dict[int, Area] = {}


class SolutionParameters(BaseModel):
    Materials: Dict[str, Material] = {}
    Surfaces_excluded_from_TI: List[int] = []


class Conductor(BaseModel):
    Geometry: GeometryParameters = GeometryParameters()
    Solution: SolutionParameters = SolutionParameters()


