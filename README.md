# cloudman

Command line tool for managing single-purpose cloud VMs. Currently works with GCP.

![cloudman-start-demo](https://i.imgur.com/g2DEBgN.gif)

Features:

1. Single command to provision cloud-based disk images with Ubuntu, NVIDIA drivers, Anaconda, PyTorch, FastAI and more..

2. Single command to attach a disk image, launch a cloud VM instance with any configuration of CPUs, RAM and GPU, and start Jupyter notebook.

## Installation

Install the `cloudman` package using `pip`.

```
pip install cloudman
```

`cloudman` requires the `gcloud` command line tool to be installed. Make sure to complete these steps before moving forward.

1. Install `gcloud` CLI using this link: https://cloud.google.com/sdk/docs/downloads-interactive

2. Make sure the `gcloud` command is added to your PATH.

3. Connect the `gcloud` tool your GCP account by running:

   `gcloud init`

4. (Optional) Create a GCP project by running:

   `gcloud projects create PROJECT_ID`

Replace PROJECT_ID with a unique name e.g. kitten-puppies-999
You can also use an existing project.

5. Activate a project by running:

   `gcloud config set project PROJECT_ID`

6. Open the cloud console by running:

   `cloudman console`

7. Enable billing to start creating cloud VMs.

## Usage

`cloudman` allows you to crate standalone boot disks which can be flexibly attached to any type of machine & GPU configuration.

### Create a boot disk

Running the `cloudman create` will create a boot disk of the given size, then install Ubuntu, NVIDIA CUDA libraries, Anaconda, Pytorch and FastAI deep learning libraries. By default, a 50 GB disk is created.

Here are some examples:

```
# Using default disk size of 50GB
cloudman create freesound-2019
```

```
# Custom disk size
cloudman create freesound-2019 --disk=100GB
```

Note that `cloudman` creates a temporary VM instance to install all the required packages, and then deletes the VM, but retains the disk. It uses [this shell script](https://raw.githubusercontent.com/aakashns/cloudman/master/cloudman/setup-scripts/gcp-ubutnu-nvidia410-fastai.sh) for setup.

### Start an instance

You can launch an instance with the boot disk attached using the `cloudman start` command. You can choose any combination of GPUs and machine types. You can also launch a CPU-only instance, which is the default. Also, you can choose whether you want a preemptible instance (enabled by default, to save cost), or a dedicated instance.

Here are some examples:

```
# CPU-only, preemptible
cloudman start jigsaw-ulmfit

# Same as the above command, but explicit
cloudman start jigsaw-ulmfit --gpu=nogpu --machine=auto --spot

# K80 GPU, dedicated
cloudman start jigsaw-ulmfit --gpu=k80 --nospot

```

Valid GPU types are: `'nogpu', 't4', 'v100', 'p100', 'p4', 'k80'`
Valid machine types can be found here: https://cloud.google.com/compute/docs/machine-types
If machine type is set to 'auto', the tool automatically picks a reasonable machine type to match the GPU's RAM & cores. You can see the mapping [here](https://github.com/aakashns/cloudman/blob/master/cloudman/gcp/constants.py).

Once started, you can use the link to access the Jupyter server. Sometimes it may take a minute or two for the Jupyter server to start.

### Stop an instance

Use the `cloudman stop` command to stop a running instance. Example:

```
cloudman stop jigsaw-ulmfit
```

### List disks and running instances

To see the available boot disks and running instances, run

```
cloudman list
```

### Delete a boot disk

To delete a boot disk, run

```
cloudman delete jigsaw-ulmfit
```

This will stop any running instances and delte the boot disk complete. All your data will be lost, so be careful while using this.
