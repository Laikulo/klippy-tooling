#!/usr/bin/env bash
./bin/make-package.py "$1"
pushd "$1"
cp chelper/__init__.py chelper/stock_pkginit.py
for i in ../patches/*.patch; do
	patch -p1 < "$i"
done
popd
if [[ $2 != "nomods" ]]; then
cp -v mods/chelper/* "$1"/chelper
fi
