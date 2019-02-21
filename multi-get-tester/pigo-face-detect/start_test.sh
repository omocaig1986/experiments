#!/bin/sh
python multi_get.py -k 20 \
                    -u "http://192.168.99.100:18080/function/pigo-face-detector" \
                    -p "/Users/gabry3795/Coding/p2p-fog/experiments/multi-get-tester/pigo-face-detect/blobs/family.jpg" \
                    --start-lambda "1" \
                    --end-lambda "40" \
                    --lambda-delta "1.0"