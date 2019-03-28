#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python bench_multi_machine.py \
        --hosts-file "$CURRENT_PATH/bench_multi_machine_lines.txt" \
        --function-url "function/pigo-face-detector" \
        --payload "$CURRENT_PATH/blobs/family.jpg" \
        --requests "200" \
        --start-lambda "1.0" \
        --end-lambda "10.0" \
        --lambda-delta "0.1" \
        --poisson