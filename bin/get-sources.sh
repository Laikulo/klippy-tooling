#!/usr/bin/env bash

klippy_version="${1:-v0.11.0}"
klippy_upstream="${2:-https://github.com/Klipper3d/klipper.git}"
if [[ -d upstream ]]; then
	rm -rf upstream
fi

mkdir upstream
cd upstream
git init
git fetch --depth 1 "${klippy_upstream}" "${klippy_version}"
git checkout FETCH_HEAD
