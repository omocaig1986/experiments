#!/bin/sh
python multi_get.py -m "0.6" \
                    -k 8 \
                    -u "http://192.168.99.100:8080/function/pigo-face-detector" \
                    -p "/home/gabrielepmattia/Coding/p2p-fog/experiments/multi-get-tester/pigo-face-detect/blobs/family.jpg" \
                    --start-ro "0.65" \
                    --end-ro "1.50"