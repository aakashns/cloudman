from __future__ import print_function
from distutils.spawn import find_executable


def cmd_exists(name):
    """Check whether `name` is an executable on PATH."""
    return find_executable(name) is not None


def attr(obj, *path, **kwargs):
    """Safely get a nested attribute from an dictionary"""
    default = kwargs.get('default')
    if obj is None:
        return default

    res = obj
    for p in path:
        if p not in res:
            return default
        res = res[p]
    return res
