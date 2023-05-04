#!/usr/bin/env bash


if [[ $1 ]]; then
	klippy_only=1
	outdir="$1"
else
	outdir=klippy
fi

if [[ -d $outdir ]]; then
	rm -rf $outdir
fi

cp -r upstream/klippy ./"${outdir}"
cp -r upstream/docs ./"${outdir}"/docs
cp -r upstream/config ./"${outdir}"/config

if [[ ! $klippy_only ]]; then
	cp -r upstream/lib/hub-ctrl ./hub-ctrl
	cp -r upstream/test ./testcases
	cp upstream/scripts/klippy-requirements.txt upstream-requirements.txt
	cp upstream/scripts/test_klippy.py test_klippy.py
fi
