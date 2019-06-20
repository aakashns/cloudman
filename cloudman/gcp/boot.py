from cloudman.gcp.constants import DEFAULT_BOOT_CONFIG
from cloudman.gcp.utils import run, await_ssh, derive_names, run_plain
from cloudman.utils.logger import log


def create_boot_instance(name, network, config=DEFAULT_BOOT_CONFIG):
    """Create a boot instance for setting up a boot disk"""
    cmd = """compute instances create {0} \
      --boot-disk-device-name={1} \
      --subnet={2} \
      --zone=us-west1-b \
      --image-family={3} \
      --boot-disk-size={4} \
      --network-tier=PREMIUM \
      --machine-type=n1-highcpu-8 \
      --accelerator="type=nvidia-tesla-k80,count=1" \
      --image-project=ubuntu-os-cloud \
      --maintenance-policy=TERMINATE \
      --boot-disk-type=pd-ssd \
      --no-boot-disk-auto-delete \
    """.format(name, name, network, config['os'], config['disk'])
    return run(cmd)


def setup_boot_disk(name, boot_instance, config=DEFAULT_BOOT_CONFIG):
    """Set up a boot disk using a given script"""
    log("Setting up the boot disk '" + boot_instance +
        "'. This may take up to an hour..")
    # Wait for SSH access
    await_ssh(boot_instance)
    # Download and run setup script
    cmd = """gcloud compute ssh "{0}" --zone=us-west1-b \
    -- "curl {1} > /tmp/setup.sh && bash /tmp/setup.sh" \
    """.format(boot_instance, config['setup-script-url'])
    return run_plain(cmd)
