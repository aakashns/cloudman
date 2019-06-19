from cloudman.gcloud.boot import derive_names, create_boot_instance, setup_boot_disk
from cloudman.gcloud.network import create_network, delete_network, has_network
from cloudman.gcloud.firewall import create_firewall, delete_firewall, has_firewall
from cloudman.gcloud.disk import has_disk, delete_disk
from cloudman.gcloud.instance import has_instance, delete_instance


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
