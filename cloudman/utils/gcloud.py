import webbrowser
import time
import json
import subprocess
from cloudman.utils.logger import log
from cloudman.utils.misc import cmd_exists, attr

GCLOUD_SDK_URL = 'https://cloud.google.com/sdk/docs/downloads-interactive'

POST_INSTALL_MSG = """After installation:

1. Make sure the `gloud` command is added to your PATH.

2. Connect the `gcloud` tool your GCP account by running:
    gcloud init

3. (Optional) Create a GCP project by running: 
    gcloud projects create PROJECT_ID

    (replace PROJECT_ID with a unique name e.g. kitten-puppies-999)

4. Activate a project by running:
    gcloud config set project PROJECT_ID

5. Open the cloud console by running:
    cloudman console

6. Enable billing to start creating cloud VMs.
"""


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


def run(cmd):
    """Run a gcloud command"""
    # Create a child process
    task = subprocess.Popen(_c(cmd), shell=True, stdout=subprocess.PIPE)
    # Get the output
    out, _ = task.communicate()
    # Parse and return
    if out == '':
        return None
    return json.loads(out)


def get_config():
    """Get the gcloud config"""
    return run('config list')


def get_active_project():
    cfg = get_config()
    return attr(cfg, 'core', 'project', default='')


def activate_project(name):
    """Set a project as active"""
    return run('config set project ' + name)


def create_project(name):
    """Create a project"""
    # Attempt to create the project
    res = run('projects create ' + name)
    # Exit if there's an error
    if res is None:
        return
    # Set project as active
    res = activate_project(name)
    if res is None:
        return
    # Log success
    log('GCP project ' + name + ' created and activate successfully!', prefix=True)


def open_console(project):
    """Open the GCP console for selected project"""
    project = get_active_project() if not project else project
    url = 'https://console.cloud.google.com/compute?project='+project
    log('Opening ' + url)
    webbrowser.open(url)
