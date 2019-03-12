#!/bin/sh
python bench_multi_machine.py \
        --hosts-file "/Users/gabry3795/Coding/p2p-fog/experiments/benchmark/bench_multi_machine_lines.txt" \
        --function-url "function/pigo-face-detector" \
        --payload "/Users/gabry3795/Coding/p2p-fog/experiments/benchmark/blobs/family.jpg" \
        --requests "200" \
        --start-lambda "1.0" \
        --end-lambda "10.0" \
        --lambda-delta "0.1" \
        --poisson
