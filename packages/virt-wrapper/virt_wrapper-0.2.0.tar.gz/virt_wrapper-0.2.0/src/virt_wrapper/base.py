"""Essential classes for managing hypervisors and virtual machines"""

from .drivers.hyperv import HyperVirtualHostDriver, HyperVirtualMachineDriver
from .drivers.kvm import KernelVirtualHostDriver, KernelVirtualMachineDriver
from .snapshot import VirtualSnapshot
from .disk import VirtualDisk
from .network import VirtualNetwork
from .memory import MemoryStat
from .storage import Storage


class VirtualMachine:
    """Essential class for managing the virtual machine"""

    def __init__(self, driver: KernelVirtualMachineDriver | HyperVirtualMachineDriver) -> None:
        self.driver = driver

    def uuid(self) -> str:
        """Get the virtual machine identifier"""
        return self.driver.uuid

    @property
    def name(self) -> str:
        """Get the virtual machine name"""
        return self.driver.get_name()

    @name.setter
    def name(self, name: str) -> None:
        """Set new the virtual machine name"""
        self.driver.set_name(name=name)

    def state(self) -> str:
        """Get the virtual machine state"""
        return self.driver.get_state()

    def description(self) -> str | None:
        """Get the virtual machine description"""
        return self.driver.get_description()

    def guest_os(self) -> str | None:
        """Get the name of the virtual machine guest operating system"""
        return self.driver.get_guest_os()

    def memory_stat(self) -> MemoryStat:
        """Get the memory statistic of the virtual machine"""
        return MemoryStat(**self.driver.get_memory_stat())

    def snapshots(self) -> list[VirtualSnapshot]:
        """Get the list of the virtual machine snapshots"""
        return [VirtualSnapshot(**snapshot) for snapshot in self.driver.get_snapshots()]

    def disks(self) -> list[VirtualDisk]:
        """Get the list of the virtual machine connected disks"""
        return [VirtualDisk(**disk) for disk in self.driver.get_disks()]

    def networks(self) -> list[VirtualNetwork]:
        """Get the list of the virtual machine network adapters"""
        return [VirtualNetwork(**net) for net in self.driver.get_networks()]

    def run(self) -> None:
        """Power on the virtual machine"""
        self.driver.run()

    def shutdown(self) -> None:
        """Shutdown the virtual machine"""
        self.driver.shutdown()

    def poweroff(self) -> None:
        """Force off the virtual machine"""
        self.driver.poweroff()

    def save(self) -> None:
        """Pause the virtual machine and temporarily saving its memory state to a file"""
        self.driver.save()

    def suspend(self) -> None:
        """Pause the virtual machine and temporarily saving its memory state"""
        self.driver.suspend()

    def resume(self) -> None:
        """Unpause the suspended virtual machine"""
        self.driver.resume()

    def snap_create(self, name: str) -> None:
        """Create a new snapshot of virtual machine"""
        self.driver.snapshot_create(name=name)

    def export(self, storage: str) -> str:
        """Export the virtual machine to a storage destination"""
        return self.driver.export(storage=storage)


class Host:
    """Essential class for managing the hypervisor"""

    def __init__(self, driver: KernelVirtualHostDriver | HyperVirtualHostDriver):
        self.driver = driver

    def virtual_machines(self) -> list[VirtualMachine]:
        """Get list of virtual machines on the hypervisor"""
        return [VirtualMachine(driver=driver) for driver in self.driver.virtual_machine_drivers()]

    def import_vm(self, source: str, storage: str, name: str) -> VirtualMachine:
        """Import a virtual machine from a source path"""
        return VirtualMachine(driver=self.driver.import_vm(source=source, storage=storage, name=name))

    def storages(self) -> list[Storage]:
        """Get information about the host storage systems"""
        return [Storage(**storage) for storage in self.driver.get_storages()]
