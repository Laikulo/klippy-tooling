#!/usr/bin/env bash

cp -r upstream/lib/hub-ctrl ./hub-ctrl
cp -r upstream/test ./testcases
cp -r upstream/klippy ./
cp -r upstream/docs ./klippy/docs
cp -r upstream/config ./klippy/config
cp upstream/scripts/klippy-requirements.txt upstream-requirements.txt
cp upstream/scripts/test_klippy.py test_klippy.py
