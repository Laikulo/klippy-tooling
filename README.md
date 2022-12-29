This repo contains scripts to turn klippy into a proper python package with precompiled extensions.
This is meant to make redistribution of klippy and klipper much easier.

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
