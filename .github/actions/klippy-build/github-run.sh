#!/bin/bash
set -e
TARGET_REF="$(git ls-remote https://github.com/Laikulo/klipper.git laikulo-devel | cut -f 1)"
bin/prepare.sh "$TARGET_REF"
pyproject-build --sdist
