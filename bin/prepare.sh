#!/usr/bin/env bash

set -e

workdir="$(dirname $0)"

cd "$workdir/../"

set -x
./bin/get-sources.sh "$1" "$2"
./bin/relocate.sh
./bin/extract-git-version.sh
./bin/modify.sh
