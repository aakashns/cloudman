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
    vms = list_instances(name_only=False)
    for vm in vms:
        if vm['name'] == name:
            return vm["networkInterfaces"][0]["accessConfigs"][0]["natIP"]


def delete_instance(name):
    """Delete an instance"""
    log("Removing instance '" + name + "'. This may take a while...", prefix=True)
    return run('compute instances delete ' + name + ' --zone=us-west1-b -q')


def create_instance(name, machine, gpu, gpucount=1, spot=True):
    """Create an instance for the given boot disk"""
    log("Starting an instance for '" + name +
        "' with machine type '" + machine + "' and GPU type '" + gpu + "'")
    # Network, firewall & boot instance name
    network, _, boot = derive_names(name)
    # GPU config
    if gpu == 'nogpu':
        gpu_arg = ''
    else:
        gpu_arg = '--accelerator="type={0},count={1}"'.format(gpu, gpucount)
    # Preemptible config
    spot_arg = '--preemptible' if spot else ''
    # Construct & run the command
    cmd = """compute instances create {0} \
      --subnet={1} \
      --network-tier=PREMIUM \
      --zone=us-west1-b \
      --machine-type={2} \
      {3} \
      --no-restart-on-failure \
      --maintenance-policy=TERMINATE \
      --disk=name={4},device-name={5},mode=rw,boot=yes \
      {6} \
    """.format(name, network, machine, gpu_arg, boot, boot, spot_arg)
    return run(cmd)
