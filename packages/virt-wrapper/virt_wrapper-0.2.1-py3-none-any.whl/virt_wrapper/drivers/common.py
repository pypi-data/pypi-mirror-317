import libvirt

STATES = {
    libvirt.VIR_DOMAIN_RUNNING: "Running",
    libvirt.VIR_DOMAIN_BLOCKED: "Blocked",
    libvirt.VIR_DOMAIN_PAUSED: "Paused",
    libvirt.VIR_DOMAIN_SHUTDOWN: "Shutdown",
    libvirt.VIR_DOMAIN_SHUTOFF: "Shutoff",
    libvirt.VIR_DOMAIN_CRASHED: "Crashed",
    libvirt.VIR_DOMAIN_NOSTATE: "No state",
}


def request_cred(user: str, password: str):
    """Callback function for authentication"""

    def inner(credentials: list, user_data):  # pylint: disable=unused-argument
        for credential in credentials:
            if credential[0] == libvirt.VIR_CRED_AUTHNAME:
                credential[4] = user
            elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
                credential[4] = password
        return 0

    return inner
