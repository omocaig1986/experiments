#!/bin/sh
CURRENT_PATH=$(pwd)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python configure_discovery.py