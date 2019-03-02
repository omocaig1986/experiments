#!/bin/sh
python bench_multi_get.py -k 10 \
                    -u "http://192.168.99.100:18080/function/pigo-face-detector" \
                    -p "/home/gabrielepmattia/Coding/p2p-fog/experiments/benchmark/blobs/family.jpg" \
                    --start-lambda "1" \
                    --end-lambda "10" \
                    --lambda-delta "0.1" \
                    -t "200" \
                    -r


#  -p "/Users/gabry3795/Coding/p2p-fog/experiments/multi-get-tester/pigo-face-detect/blobs/family.jpg" \