from cloudman.utils.logger import log
from cloudman.gcp.utils import run, derive_names
from cloudman.utils.misc import attr


def list_instances(name_only=True):
    """Get list of instances in current project"""
    vms = run('compute instances list')
    return [str(vm['name']) for vm in vms] if name_only else vms


def has_instance(name):
    """Check if an instance with given name exists"""
    vms = list_instances()
    return name in vms


def get_instance_ip(name):
    """Get the external IP for an instance"""
    vms = list_instances()
    for vm in vms:
        if vm['name'] == name:
            return attr(vm, "networkInterfaces", 0, "accessConfigs", 0, "natIP")


def delete_instance(name):
    """Delete an instance"""
    log("Deleting instance '" + name + "'. This may take a while...", prefix=True)
    return run('compute instances delete ' + name)


def create_instance(name, machine, gpu, spot=True):
    """Create an instance for the given boot disk"""
    log("Starting an instance for '" + name +
        "' with machine type '" + machine + "' and GPU type '" + gpu + "'")
    # Network, firewall & boot instance name
    network, _, _ = derive_names(name)
    # GPU config
    gpu_arg = '--accelerator="type={0},count=1"'.format(gpu) if gpu else ''
    # Preemptible config
    spot_arg = '--preemptible' if spot else ''
    # Construct & run the command
    cmd = """gcloud compute instances create {0} \
      --subnet={1} \
      --network-tier=PREMIUM \
      --machine-type={2} \
      {3} \
      --no-restart-on-failure \
      --maintenance-policy=TERMINATE \
      --disk=name={4},device-name={5},mode=rw,boot=yes \
      {6} \
    """.format(name, network, machine, gpu_arg, name, name, spot_arg)
    return run(cmd)
