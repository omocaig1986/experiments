#!/bin/bash
CURRENT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate
"$CURRENT_PATH"/env/bin/python bench_single_machine.py \
                    --host "192.168.99.100:18080" \
                    --function-url "function/pigo-face-detector" \
                    --payload "$CURRENT_PATH/blobs/family.jpg" \
                    --start-lambda "1" \
                    --end-lambda "10" \
                    --lambda-delta "0.1" \
                    --requests "200" \
                    --poisson


#  -p "/Users/gabry3795/Coding/p2p-fog/experiments/benchmark/blobs/family.jpg" \