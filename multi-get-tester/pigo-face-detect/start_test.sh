#!/bin/sh
python multi_get.py -m "0.33" \
                    -k 8 \
                    -u "http://192.168.99.100:18080/function/pigo-face-detector" \
                    -p "/home/gabrielepmattia/Coding/p2p-fog/experiments/multi-get-tester/pigo-face-detect/blobs/family.jpg" \
                    --start-ro 1 \
                    --end-ro "0"