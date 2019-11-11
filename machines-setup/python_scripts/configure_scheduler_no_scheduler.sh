#!/bin/sh
CURRENT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python $CURRENT_PATH/configure_scheduler.py --scheduler "NoScheduler true"