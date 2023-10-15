#!/usr/bin/env bash

# This script makes a directory that is as if it were a real project.

dest_dir="${1:-./pub}"
if [[ ! -d $dest_dir ]]; then
	mkdir "${dest_dir}"
fi
cp -r klippy pyproject.toml testcases hub-ctrl compile.py setup.py README-py.md test_klippy.py COPYING "$dest_dir"
cp README-repo.md "$dest_dir/README.md"
