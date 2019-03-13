#!/bin/sh
CURRENT_PATH=$(pwd)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python configure_scheduler.py --scheduler "PowerOfNScheduler 1 2 true 1"