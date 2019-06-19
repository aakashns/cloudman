from cloudman.utils.logger import log
from cloudman.gcloud.utils import run


def list_instances():
    """Get list of instances in current project"""
    res = run('compute instances list')
    return [str(vm['name']) for vm in res]


def has_instance(name):
    """Check if an instance with given name exists"""
    vms = list_instances()
    return name in vms


def delete_instance(name):
    """Delete an instance"""
    log("Deleting instance '" + name + "'. This may take a while...", prefix=True)
    return run('compute instances delete ' + name)
