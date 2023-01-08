#!python3
# We use relative here, so we can work in envs
# This is meant to be executed in a seperate process to avoid importing anything from klippy into the main buld

import logging

import klippy.chelper .builder as builder

builder.build_chelper()
builder.build_hub_ctrl()

