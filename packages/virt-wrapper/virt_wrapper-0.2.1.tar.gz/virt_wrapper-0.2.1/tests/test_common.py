"""Integration tests of the virt-wrapper module"""

import pytest

from virt_wrapper import Host  # pylint: disable=import-error


@pytest.mark.parametrize("host", ["kvm_host", "hv_host"])
def test(host: Host, request):
    """Integration tests"""
    host = request.getfixturevalue(host)
    print(host.storages())

    for vm in host.virtual_machines():
        if vm.name.startswith("pytest-"):
            break
    else:
        raise ValueError("Virtual machine for tests wasn't found")

    # Testing the management of virtual disks
    disk = vm.disks()[0]
    old_size = disk.size
    disk.resize(old_size + 1024**3)  # Add 1GB
    assert disk.size == old_size + 1024**3

    # Testing the management of snapshots
    for snap in vm.snapshots():
        snap.destroy()

    # Check if there are no snapshots
    assert len(vm.snapshots()) == 0

    vm.snap_create("parent")
    vm.snap_create("child")

    for snap in vm.snapshots():
        assert snap.name in ("parent", "child")
        if snap.name == "parent":
            assert snap.parent_name is None
        elif snap.name == "child":
            assert snap.parent_name == "parent"

    vm.run()
    assert vm.state() == "Running"
    vm.poweroff()
    assert vm.state() == "Shutoff"

    print(vm.networks())
    print(vm.memory_stat())
