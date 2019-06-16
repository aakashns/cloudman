from __future__ import print_function
from sys import stderr
from termcolor import colored


def log(msg, error=False, prefix=False):
    """Print a message to stdout"""
    if error:
        print(colored('ERROR:', color='red'), '[cloudman]', msg, "\n", file=stderr)
    else:
        print(('[cloudman]' if prefix else '') + msg, "\n")
