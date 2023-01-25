#!/usr/bin/env bash

klippy_version="0.11.0"
if [[ ! -f klipper-${klippy_version}.tar.gz ]]; then 
	curl -L https://github.com/Klipper3d/klipper/archive/refs/tags/v${klippy_version}.tar.gz -o klipper-${klippy_version}.tar.gz
fi

tar xvf klipper-${klippy_version}.tar.gz --strip-components 1 \
	--transform 's:lib/hub-ctrl:hub-ctrl:' \
	--transform 's:scripts/klippy-requirements\.txt:upstream-requirements.txt:' \
	--transform 's:test/klippy:testcases:' \
	klipper-${klippy_version}/lib/hub-ctrl/ \
	klipper-${klippy_version}/klippy \
	klipper-${klippy_version}/scripts/klippy-requirements.txt \
	klipper-${klippy_version}/test/klippy
