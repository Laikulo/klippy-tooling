#!/usr/bin/env bash
./bin/make-package.sh
pushd klippy
for i in ../patches/*.patch; do
	patch -p1 < "$i"
done
popd
if [[ $1 != "nomods" ]]; then
cp -v mods/chelper/* klippy/chelper
fi
