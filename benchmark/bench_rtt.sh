#!/bin/sh
CURRENT_PATH=$(pwd)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python benh_rtt.py \
                    --host "192.168.99.100:18080" \
                    --function-url "function/pigo-face-detector" \
                    --payload "$CURRENT_PATH/blobs/family.jpg" \
                    --requests "200"
