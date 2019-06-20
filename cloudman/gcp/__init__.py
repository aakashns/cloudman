from cloudman.gcp.boot import create_boot_instance, setup_boot_disk
from cloudman.gcp.network import create_network, delete_network, has_network
from cloudman.gcp.firewall import create_firewall, delete_firewall, has_firewall
from cloudman.gcp.disk import has_disk, delete_disk
from cloudman.gcp.instance import has_instance, delete_instance, create_instance, get_instance_ip
from cloudman.gcp.utils import derive_names
from cloudman.utils.logger import log
from cloudman.gcp.machine import resolve_gpu_machine


def create(name, config):
    """Create a new network and boot disk with the given config"""
    # Network, firewall & boot instance name
    network, firewall, boot_instance = derive_names(name)
    # Create network & firewall
    create_network(network)
    create_firewall(firewall, network)
    # Create boot instance
    create_boot_instance(name, boot_instance, network, config)
    # Set up boot disk
    setup_boot_disk(name, config)
    # Delete boot instance (disk is retained)
    delete_instance(name)


def start(name, gpu='nogpu', machine='auto', spot=True):
    # Check if exists
    if has_instance(name):
        # Log and skip creation
        log("Compute instance for boot disk '" +
            name + "' is already running. Skipping.. ", prefix=True)
    else:
        # Get GCP types and create machine
        gpu, machine = resolve_gpu_machine(gpu, machine)
        create_instance(name, machine, gpu, spot)
    # Print Jupyter URL
    ext_ip = get_instance_ip(name)
    jupyter_url = "http://" + ext_ip + ":8888"
    log("Access Jupyter notebook here: " + jupyter_url)


def destroy(name):
    """Remove boot disk, network and all related things"""
    # Network, firewall & boot instance name
    network, firewall, boot_instance = derive_names(name)
    # Delete boot instance
    if has_instance(boot_instance):
        delete_instance(boot_instance)
    # Delete boot disk
    if has_disk(name):
        delete_disk(name)
    # Delete firewall
    if has_firewall(firewall):
        delete_firewall(firewall)
    # Delete network
    if has_network(network):
        delete_network(network)
