from cloudman.utils.logger import log
from cloudman.gcp.utils import run


def list_disks():
    """Get list of disks in current project"""
    res = run('compute disks list')
    return [str(disk['name']) for disk in res]


def has_disk(name):
    """Check if a disk with given name exists"""
    return name in list_disks()


def delete_disk(name):
    """Delete a disk"""
    log("Deleting disk '" + name + "'. This may take a while...", prefix=True)
    return run('compute disks delete ' + name + " --zone=us-west1-b")
