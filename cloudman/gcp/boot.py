from cloudman.gcp.constants import DEFAULT_BOOT_CONFIG
from cloudman.gcp.utils import run, await_ssh
from cloudman.utils.logger import log


def create_boot_instance(disk_name, instance, network, config=DEFAULT_BOOT_CONFIG):
    """Create a boot instance for setting up a boot disk"""
    cmd = """compute instances create {0} \
      --boot-disk-device-name={1} \
      --subnet={2} \
      --image-family={3} \
      --boot-disk-size={4} \
      --network-tier=PREMIUM \
      --machine-type=n1-highcpu-8 \
      --accelerator="type=nvidia-tesla-k80,count=1" \
      --image-project=ubuntu-os-cloud \
      --maintenance-policy=TERMINATE \
      --boot-disk-type=pd-ssd \
      --no-boot-disk-auto-delete \
    """.format(instance, disk_name, network, config['os'], config['disk-size'])
    return run(cmd)


def setup_boot_disk(name, config):
    """Set up a boot disk using a given script"""
    # Wait for SSH access
    await_ssh(name)
    # Download and run setup script
    cmd = """compute ssh "{0}" \
    -- "curl {1} > /tmp/setup.sh && bash /tmp/setup.sh \
    """.format(name, config['setup-script-url'])
    return run(cmd)
