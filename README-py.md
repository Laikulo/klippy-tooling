# Klipper-Klippy

This is a python-packaged version of the python component of [Klipper](Klipper3d.com).

## Differences from vanilla klipper
* Supports "extras" modules from other packges in the PYTHONPATH. Give a full name of the module as the type in a config file to use this.
* Supports setting group and mode on the linux mcu's pty
* Contains a tweak for the arm linker script to support building on a broader spec of newlib versions

## Commands
Klippy can be invoked as `klipper-klippy` or `klipper_klippy`.
Older versions of this used `klippy`, but that was already in use by other packages, and was renamed.
