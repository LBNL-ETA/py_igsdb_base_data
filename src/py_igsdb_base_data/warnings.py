from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseWarning:
    warning_type: Optional[str] = None
    warning_subtype: Optional[str] = None
    message: Optional[str] = None
    field_name: Optional[str] = None
