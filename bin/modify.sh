#!/usr/bin/env bash
patch -p0 < klippy-patches.patch
if [[ $1 != "nomods" ]]; then
cp -v mods/chelper/* klippy/chelper
fi
