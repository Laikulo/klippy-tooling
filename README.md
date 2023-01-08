This repo contains scripts to turn klippy into a proper python package with precompiled extensions.
This is meant to make redistribution of klippy and klipper much easier.

Requiremets:
* Working gcc
* libusb and apropriated headers
* Python 3.8 or newer

USAGE:
From the root of this repo:
1. run `bin/get-sources.sh` to download klipper sources, and extract klippy from them
2. run `bin/modify.sh` to replace the chelper logic, and apply import patches
3. run `python -m build` to build the wheel and sdist in an isolated environment.

Note that the wheel contains an archetecture dependant library and binary. Since libusb is dynamically linked into hubctl, and the c helper is not static, this is NOT distro portable.

*DO NOT* That means these packages WILL NOT follow the assumptions that manylinux makes.

Current steps:
* replace imports for klippy components with rellative imports
* adjust importlib invocations
* create `__init__` in main klipper package
* update deps from `scripts/klippy-reqirements.txt`
* repalce c helper with nerfed one
* call origional c helper to build 

TODO:
* Create a script to progmatically replace imports
* Create a script to build the c helper at buildtime, integrate same with poetry/setuptools
* create a test for running --import-test in klippy
