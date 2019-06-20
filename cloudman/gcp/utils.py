import subprocess
import time
import json
from cloudman.utils.misc import cmd_exists
from cloudman.utils.logger import log
from cloudman.gcp.constants import GCLOUD_SDK_URL, POST_INSTALL_MSG


class GCPError(Exception):
    """Class to capture all errors related to the `gcloud` tool"""
    pass


def has_gcloud():
    """Check if gcloud CLI exists on sytem PATH"""
    return cmd_exists('gcloud')


def _c(cmd, json_out=True):
    """Helper function to construct commands for the `gcloud` tool"""
    return 'gcloud ' + cmd + (' --format=json' if json_out else '')


def _e(cmd, rc, out):
    """Helper functon to show errors for failed GCP commands"""
    return "[cloudman] GCP command '" + _c(cmd) + "'\nfailed with return code '" + str(rc) + "' and output: " + out + "\n"


def run_plain(cmd):
    # Log the command
    log("$ " + cmd, prefix=True)
    # Create a child process
    task = subprocess.Popen(cmd, shell=True)
    # Get the return code
    _, _ = task.communicate()
    rc = task.returncode
    return rc


def run(cmd, safe=False, json_out=True):
    """Run a gcloud command"""
    # Log the command
    log("$ " + _c(cmd, json_out), prefix=True)
    # Create a child process
    task = subprocess.Popen(_c(cmd), shell=True, stdout=subprocess.PIPE)
    # Get the output & return code
    out, _ = task.communicate()
    rc = task.returncode
    # Handle empty outputs (special return code)
    if out == '':
        rc = -9999
    # Return with code in safe mode
    if safe:
        return None if out == '' else (json.loads(out) if json_out else out), rc
    # Raise error if required
    if rc != 0:
        raise GCPError(_e(cmd, rc, out))
    # Return successful result
    return json.loads(out) if json_out else out


def await_ssh(name, max_tries=200, sleep=2):
    """Wait for SSH access to an instance"""
    log('Waiting for SSH access to ' + name + '...', prefix=True)
    cmd = 'gcloud compute ssh --zone=us-west1-b ' + \
        name + """ -- "echo 'SSH is ready'" """
    for i in range(max_tries):
        rc = run_plain(cmd)
        if rc == 0:
            return
        time.sleep(sleep)
        log('Trying again (' + str(i+1) + ')...', prefix=True)
    raise GCPError('Failed to SSH to instance ' + name)


def derive_names(name):
    """Get name of network, firewall & boot instance from boot disk"""
    network = name + '-network'
    firewall = name + '-firewall-allow-all'
    boot = name
    return network, firewall, boot
