#!/usr/bin/env bash

klippy_version="${1:-v0.11.0}"
klippy_upstream="${2:-http://github.com/klipper3d/klipper.git}"
if [[ -d upstream ]]; then
	rm -rf upstream
fi

git clone --depth 1 -b "${klippy_version}" "${klippy_upstream}" upstream
