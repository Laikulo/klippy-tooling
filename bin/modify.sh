#!/usr/bin/env bash
klippy_dir=${1:-klippy}
./bin/make-package.py "$klippy_dir"
pushd "$klippy_dir"
cp chelper/__init__.py chelper/stock_pkginit.py
for i in ../patches/*.patch; do
	patch -p1 < "$i"
done
popd
