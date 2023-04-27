#!/bin/bash

#We can assume we are already in the workspace
bin/get-sources.sh
bin/modify.sh
pyproject-build
