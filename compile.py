#!python3
# We use relative here, so we can work in envs
# This is meant to be executed in a seperate process

import logging

import klippy.chelper .builder as builder

logging.basicConfig(level=logging.DEBUG)

builder.build_chelper()
builder.build_hub_ctrl()

