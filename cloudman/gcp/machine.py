from cloudman.gcp.utils import run, GCPError
from cloudman.gcp.constants import MACHINE_TYPES, GPU_TYPES, GPU_DEFAULT_MACHINE


def get_gpu(name):
    """Get full GPU name from a valid shorthand.

    See https://cloud.google.com/compute/docs/gpus/#introduction for a full list.
    """
    if name == 'nogpu':
        return name
    if name in GPU_TYPES:
        return "nvidia-tesla-" + name
    raise GCPError("Invalid GPU type '" + name +
                   "'! Choose one of:\n\t" + ', '.join(GPU_TYPES) + "\n\n" +
                   "See https://cloud.google.com/compute/docs/gpus/#introduction " +
                   "for more details about available GPUs.")


def get_machine(gpu, machine):
    """Get the full machine type from a valid gpu+machine shorthand

    See https://cloud.google.com/compute/docs/machine-types for a full list.
    """
    # Manually specified machine
    if machine != 'auto':
        if machine in MACHINE_TYPES:
            return machine
        # Show error message with machine types
        raise GCPError("Invalid machine type '" + machine + "'! " +
                       "See https://cloud.google.com/compute/docs/machine-types " +
                       "for a list of valid machine types.")
    # Automatic choice
    if gpu in GPU_TYPES:
        return GPU_DEFAULT_MACHINE[gpu]

    # Show error message with GPU types
    raise GCPError("Invalid GPU type '" + gpu +
                   "'! Choose one of:\n\t" + ', '.join(GPU_TYPES) + "\n\n" +
                   "See https://cloud.google.com/compute/docs/gpus/#introduction " +
                   "for more details about available GPUs.")


def resolve_gpu_machine(gpu, machine):
    """Translate the gpu and machine shorthand to GCP types"""
    gpu_str = get_gpu(gpu)
    machine_str = get_machine(gpu, machine)
    return gpu_str, machine_str
