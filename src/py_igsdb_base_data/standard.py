from dataclasses import dataclass
from enum import Enum


class CalculationStandardName(Enum):
    NFRC = "NFRC"
    CES = "CES"


class CalculationStandardMethodTypes(Enum):
    SOLAR = "Solar"
    PHOTOPIC = "Photopic"
    THERMAL_IR = "Thermal IR"
    TUV = "TUV"
    SPF = "SPF"
    TDW = "TDW"
    TKR = "TKR"


@dataclass
class CalculationStandard:
    name: str
    method_type: str
    description: str
    contents: str
