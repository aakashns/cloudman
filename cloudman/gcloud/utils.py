import webbrowser
import subprocess
import time
import json
from cloudman.utils.misc import cmd_exists
from cloudman.utils.logger import log
from cloudman.gcloud.constants import GCLOUD_SDK_URL, POST_INSTALL_MSG


class GCPError(Exception):
    """Class to capture all errors related to the `gcloud` tool"""
    pass


def has_gcloud():
    """Check if gcloud CLI exists on sytem PATH"""
    return cmd_exists('gcloud')


def install_gcloud(force=False, automatic=False, browser=True):
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
    if browser:
        log('Opening link in browser...')
        time.sleep(2)
        webbrowser.open(GCLOUD_SDK_URL)


def _c(cmd):
    """Helper function to construct commands for the `gcloud` tool"""
    return 'gcloud ' + cmd + ' --format=json'


def _e(cmd, rc, out):
    """Helper functon to show errors for failed GCP commands"""
    return "[cloudman] GCP command '" + _c(cmd) + "'\nfailed with return code '" + str(rc) + "' and output: " + out + "\n"


def run(cmd, safe=False):
    """Run a gcloud command"""
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
        return None if out == '' else json.loads(out), rc
    # Raise error if required
    if rc != 0:
        raise GCPError(_e(cmd, rc, out))
    # Return successful result
    return json.loads(out)


def await_ssh(name, max_tries=200, sleep=2):
    """Wait for SSH access to an instance"""
    log('Waiting for SSH access to ' + name + '...', prefix=True)
    cmd = 'compute ssh ' + name + """ -- "echo 'SSH is ready'"""
    for i in range(max_tries):
        _, rc = run(cmd, safe=True)
        if rc == 0:
            return
        time.sleep(sleep)
        log('Trying again (' + str(i+1) + ')...', prefix=True)
    raise GCPError('Failed to SSH to instance ' + name)


def get_gpu(name):
    """Get full GPU name from a valid shorthand.

    See https://cloud.google.com/compute/docs/gpus/#introduction for a full list.
    """
    valid_names = ['t4', 'v100', 'p100', 'p4', 'k80']
    if name in valid_names:
        return "nvidia-tesla-" + name
    raise GCPError("Invalid GPU type '" + name +
                   "'. Choose one of:\n\t't4', 'v100', 'p100', 'p4', 'k80'\n\n" +
                   "See https://cloud.google.com/compute/docs/gpus/#introduction " +
                   "for more details about available GPUs.")
