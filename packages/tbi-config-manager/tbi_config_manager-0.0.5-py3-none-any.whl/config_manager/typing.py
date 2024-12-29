# Type definitions and enums
from enum import Enum
from typing import Any, Dict, Optional, Union
from pathlib import Path


class Provider(Enum):
    """Configuration provider types"""

    ENV = "env"
    GCP = "gcp"


ConfigValue = Union[str, int, float, bool, None]
PathLike = Union[str, Path]
