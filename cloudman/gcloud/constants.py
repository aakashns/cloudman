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

DEFAULT_BOOT_CONFIG = {
    'disk-size': '50GB',
    'os': "ubuntu-1804-lts",
    'setup-script-url': "https://raw.githubusercontent.com/arunoda/fastai-shell/master/setup-gce.sh"
}
