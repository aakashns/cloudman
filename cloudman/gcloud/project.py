import webbrowser
from cloudman.utils.logger import log
from cloudman.gcloud.utils import run
from cloudman.utils.misc import attr


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
    run('projects create ' + name)
    # Set project as active
    activate_project(name)
    # Log success
    log('GCP project ' + name + ' created and activate successfully!', prefix=True)


def open_console(project):
    """Open the GCP console for selected project"""
    project = get_active_project() if not project else project
    url = 'https://console.cloud.google.com/compute?project='+project
    log('Opening ' + url)
    webbrowser.open(url)
