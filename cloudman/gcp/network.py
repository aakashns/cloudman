from cloudman.utils.logger import log
from cloudman.gcp.utils import run


def list_networks():
    """Get list of networks in current project"""
    res = run('compute networks list')
    return [str(net['name']) for net in res]


def has_network(name):
    """Check if a network with given name exists"""
    nets = list_networks()
    return name in nets


def create_network(name):
    """Create a networks with the given name"""
    log("Creating network '" + name + "'. This may take a while...", prefix=True)
    return run('compute networks create ' + name)


def delete_network(name):
    """Delete a networks with the given name"""
    log("Deleting network '" + name + "'. This may take a while...", prefix=True)
    return run('compute networks delete ' + name + ' -q')
