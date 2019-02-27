#!/bin/sh
python bench_multi_get.py -k 10 \
                    -u "http://192.168.99.100:18080/function/exponential-loop" \
                    --start-lambda "1" \
                    --end-lambda "5" \
                    --lambda-delta "0.1" \
                    --requests "200" \
                    -r


#  -p "/Users/gabry3795/Coding/p2p-fog/experiments/benchmark/blobs/family.jpg" \