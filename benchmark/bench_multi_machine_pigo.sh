#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python bench_multi_machine.py \
        --hosts-file "$CURRENT_PATH/hosts.txt" \
        --function-url "function/pigo-face-detector" \
        --payload "$CURRENT_PATH/blobs/family.jpg" \
        --requests "200" \
        --start-lambda "0.1" \
        --end-lambda "3.8" \
        --lambda-delta "0.05" \
        --poisson
