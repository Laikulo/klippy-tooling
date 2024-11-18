#!/bin/bash

GIT_WORK_TREE=upstream GIT_DIR=upstream/.git git describe --always --tags --long > klippy/.version
