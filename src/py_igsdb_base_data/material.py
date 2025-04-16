from dataclasses import dataclass, field
from enum import Enum

from typing import Dict, Optional


class MaterialType(Enum):
    UNKNOWN = "Unknown"
    NOT_APPLICABLE = "Not applicable"
    GLASS = "glass"
    PVB = "PVB"
    POLYCARBONATE = "polycarbonate"
    ACRYLIC = "acrylic"
    PET = "PET"


material_type_lookup = {
    1: "UNKNOWN",
    2: "NA",
    3: "GLASS",
    4: "PVB",
    5: "POLYCARBONATE",
    6: "ACRYLIC",
    7: "PET"
}


@dataclass
class MaterialBulkProperties:
    name: Optional[str] = None
    display_name: Optional[str] = None
    version: Optional[str] = None
    conductivity: Optional[float] = None
    youngs_modulus: Optional[float] = None
    poissons_ratio: Optional[float] = None
    elasticity: Optional[float] = None
    moisture_properties: Optional[Dict] = field(default_factory=dict)
