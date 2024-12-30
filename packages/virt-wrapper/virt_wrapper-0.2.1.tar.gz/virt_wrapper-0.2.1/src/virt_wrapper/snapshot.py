"""Module for managing the virtual machine snapshots"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class VirtualSnapshot:
    """Data structure that contains the virtual machine snapshot info"""

    driver: None = field(repr=False)
    identifier: str
    name: str
    parent_name: str
    creation_time: int
    is_applied: bool
    cpu: int
    ram: int

    def __post_init__(self):
        object.__setattr__(self, "creation_time", datetime.fromtimestamp(self.creation_time))

    def apply(self) -> None:
        """Apply the snapshot"""
        self.driver.apply()

    def destroy(self) -> None:
        """Destroy the snapshot"""
        self.driver.destroy()
