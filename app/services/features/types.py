"""DTO for features service."""

from dataclasses import dataclass
from typing import Dict

AppName = str
IsEnabled = bool


@dataclass
class AppFeatures:
    """Application features."""

    app: str
    features: Dict[AppName, IsEnabled]
