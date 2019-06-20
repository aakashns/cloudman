from cloudman.utils.logger import log
from cloudman.gcp.utils import run


def list_firewalls():
    """Get list of firewall rules in current project"""
    rules = run('compute firewall-rules list')
    return [str(rule['name']) for rule in rules]


def create_firewall(name, network):
    """Create an ingress allow-all firewall with given name"""
    log("Creating allow-all firewall '" + name + "' for network '" +
        network + "'. This may take a while...", prefix=True)
    return run('compute firewall-rules create ' + name + ' --network=' + network +
               ' --direction=INGRESS --priority=1000 --action=ALLOW' +
               ' --rules=all --source-ranges=0.0.0.0/0')


def has_firewall(name):
    """Check if a firewall with given name exists"""
    return name in list_firewalls()


def delete_firewall(name):
    """Delete a firewall with the given name"""
    log("Deleting firewall '" + name + "'. This may take a while...", prefix=True)
    return run('compute firewall-rules delete ' + name + ' -q')
