import time
import webbrowser
from cloudman.gcp.boot import create_boot_instance, setup_boot_disk
from cloudman.gcp.network import create_network, delete_network, has_network
from cloudman.gcp.firewall import create_firewall, delete_firewall, has_firewall
from cloudman.gcp.disk import has_disk, delete_disk
from cloudman.gcp.instance import has_instance, delete_instance, create_instance, get_instance_ip
from cloudman.gcp.utils import derive_names, has_gcloud, run_plain, run
from cloudman.gcp.constants import POST_INSTALL_MSG, GCLOUD_SDK_URL, DEFAULT_BOOT_CONFIG
from cloudman.utils.logger import log
from cloudman.gcp.machine import resolve_gpu_machine
from cloudman.gcp.project import get_active_project


def install_gcloud(force=False, automatic=False, nobrowser=False):
    """Install the `gcloud` command line tool (aka Google Cloud SDK)"""
    # Check if gcloud exists
    if has_gcloud() and not force:
        log('`gcloud` command line tool is already installed. Skipping...', error=True)
        log('Tip: Use "--force" to force reinstallation.')
        return

    if automatic:
        log('Automatic installation is not implemented yet.\n\nPlease install manually without the "--automatic" flag!', error=True)
        return

    # Log the URL
    log('Install gcloud CLI using this link: \n\t' + GCLOUD_SDK_URL)
    log(POST_INSTALL_MSG)

    # Open browser if requested
    if not nobrowser:
        log('Opening link in browser...')
        time.sleep(2)
        webbrowser.open(GCLOUD_SDK_URL)


def open_console(project=''):
    """Open the GCP console for selected project"""
    project = get_active_project() if not project else project
    url = 'https://console.cloud.google.com/compute?project='+project
    log('Opening ' + url)
    webbrowser.open(url)


def create(name, disk='50GB'):
    """Create a new network and boot disk with the given config"""
    # Create a config
    config = dict(DEFAULT_BOOT_CONFIG)
    config['disk'] = disk
    # Network, firewall & boot instance name
    network, firewall, boot = derive_names(name)
    # Create network & firewall
    create_network(network)
    create_firewall(firewall, network)
    # Create boot instance
    create_boot_instance(boot, network, config)
    # Set up boot disk
    setup_boot_disk(name, boot, config)
    # Delete boot instance (disk is retained)
    delete_instance(boot)


def list_disks():
    """Show the list of boot disks and running instances"""
    log('Boot disks:', prefix=True)
    run_plain('gcloud compute disks list')
    print('\n')
    log('Running instances:', prefix=True)
    run_plain('gcloud compute instances list')


def start(name, gpu='nogpu', machine='auto', spot=True):
    # Check if exists
    if has_instance(name):
        # Log and skip creation
        log("Compute instance for '" +
            name + "' is already running. Skipping.. ", prefix=True)
    else:
        # Get GCP types and create machine
        gpu, machine = resolve_gpu_machine(gpu, machine)
        create_instance(name, machine, gpu, spot)
    # Print Jupyter URL
    ext_ip = get_instance_ip(name)
    jupyter_url = "http://" + ext_ip + ":8080"
    log("Access Jupyter notebook here: " + jupyter_url)


def stop(name):
    """Stop a running instance for the given boot disk"""
    # Check if exists
    if has_instance(name):
        delete_instance(name)
    else:
        log("Instance for '" + name + "' is not running. Skipping..")


def delete(name):
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


def ssh(name):
    """SSH into the given machine"""
    run('compute ssh ' + name + ' --zone=us-west1-b')
