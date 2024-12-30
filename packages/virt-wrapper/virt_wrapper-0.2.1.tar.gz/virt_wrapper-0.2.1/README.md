# Description

Python wrapper for managing virtual infrastructure based on Hyper-V or KVM (libvirt)

# Example usage
## Get access to particular VM by UUID
```python
from virt_wrapper import *

kvm_driver = KernelVirtualMachineDriver(
    host="linux-server.lan",
    uuid="c7c2f567-064f-464e-9843-1ed55c04f35e",
    auth=("user", "123456"),
)
kvm = VirtualMachine(driver=kvm)

hvm_driver = HyperVirtualMachineDriver(
    host="windows-server.lan",
    uuid="37a6cee8-f6ce-48c4-a635-7145e8770cca",
    auth=("user", "123456"),
)
hvm = VirtualMachine(driver=hvm_driver)

print(f"Virtual machine on Linux has name: {kvm.name}\nVirtual machine on Windows has name: {hvm.name}")

```

## Get all VMs on particular hypervisor
```python
from virt_wrapper import *

host_driver = HyperVirtualHostDriver(
    address="windows-server.lan",
    auth=("user", "123456"),
)
host = Host(driver=host_driver)

# OR

host_driver = KernelVirtualHostDriver(
    address="linux-server.lan",
    auth=("user", "123456"),
)
host = Host(driver=host_driver)

for vm in host.virtual_machines():
    print(vm.name())
```


# Requirements
## KVM

- SSH-key must be imported on target server
- User must have full access to libvirt
```sh
usermod <your_user> -aG libvirt
systemctl restart libvirtd
```

## Hyper-V
- User must have full access to Hyper-V
- WinRM must be enabled with this parameters
    - HTTPS
    - Basic auth

```powershell
# Enables the WinRM service and sets up the HTTP listener
Enable-PSRemoting -Force

# Create HTTPS listener
$httpsParams = @{
    ResourceURI = 'winrm/config/listener'
    SelectorSet = @{
        Transport = "HTTPS"
        Address   = "*"
    }
    ValueSet = @{
        CertificateThumbprint = ""
        Enabled               = $true
    }
}
New-WSManInstance @httpsParams

# Enable basic auth
Set-Item -Path WSMan:\localhost\Service\Auth\Basic -Value $true

# Opens port 5986 for all profiles
$firewallParams = @{
    Action      = 'Allow'
    Description = 'Inbound rule for Windows Remote Management via WS-Management. [TCP 5986]'
    Direction   = 'Inbound'
    DisplayName = 'Windows Remote Management (HTTPS-In)'
    LocalPort   = 5986
    Profile     = 'Any'
    Protocol    = 'TCP'
}
New-NetFirewallRule @firewallParams
```

# Available functions:
- Getting and managing snapshots
- Getting virtual disks
- Getting network adapters
- Getting state
- Getting description
- Getting guest OS (guest tools must be installed)
- Managing of VM state (run, shutdown, poweroff, save, suspend, resume)
- Getting list of all VMs on host
- Resize virtual disks
- Export/Import virtual machines

# TODO
- Migrating
- Cloning