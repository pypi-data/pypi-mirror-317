"""Module for managing the virtual machine disks"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class VirtualDisk:
    """Data structure that contains the virtual machine disk info"""

    driver: None = field(repr=False)
    name: str
    path: str
    storage: str
    size: int
    used: int

    def __post_init__(self):
        object.__setattr__(self, "path", Path(self.path))

    def resize(self, required_size: int) -> None:
        """Resize the virtual disk"""
        object.__setattr__(self, "size", self.driver.resize(required_size))
