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
    'disk': '50GB',
    'os': "ubuntu-1804-lts",
    'setup-script-url': "https://raw.githubusercontent.com/arunoda/fastai-shell/master/setup-gce.sh"
}

MACHINE_TYPES = [
    "f1-micro",
    "g1-small",
    "n1-highcpu-16",
    "n1-highcpu-2",
    "n1-highcpu-32",
    "n1-highcpu-4",
    "n1-highcpu-64",
    "n1-highcpu-8",
    "n1-highcpu-96",
    "n1-highmem-16",
    "n1-highmem-2",
    "n1-highmem-32",
    "n1-highmem-4",
    "n1-highmem-64",
    "n1-highmem-8",
    "n1-highmem-96",
    "n1-megamem-96",
    "n1-standard-1",
    "n1-standard-16",
    "n1-standard-2",
    "n1-standard-32",
    "n1-standard-4",
    "n1-standard-64",
    "n1-standard-8",
    "n1-standard-96",
    "n1-ultramem-160",
    "n1-ultramem-40",
    "n1-ultramem-80"
]

GPU_TYPES = ['nogpu', 't4', 'v100', 'p100', 'p4', 'k80']

GPU_DEFAULT_MACHINE = {
    't4': 'n1-standard-16',
    'v100': 'n1-standard-8',
    'p100': 'n1-standard-8',
    'p4': 'n1-standard-4',
    'k80': 'n1-standard-4',
    'nogpu': 'n1-standard-4'
}
