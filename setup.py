import setuptools
import re

MODULE_DIR = 'cloudman'
VERSIONFILE = "./" + MODULE_DIR + "/_version.py"


verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)

if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

with open("README.md", "rb") as fh:
    long_description = fh.read().decode('utf-8', errors='ignore')

setuptools.setup(
    name='cloudman',
    version=verstr,
    author="SwiftAce Inc.",
    author_email="opensource@swiftace.ai",
    entry_points={
        'console_scripts': ['cloudman=cloudman.cli:main'],
    },
    description='Command line tool for managing single-purpose cloud VMs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aakashns/cloudman",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=['fire', 'termcolor']
)
