#!/bin/sh
python bench_multi_machine.py \
        -f /home/gabrielepmattia/Coding/p2p-fog/experiments/benchmark/bench_multi_machine_lines.txt \
        --start-lambda "1.0" \
        --end-lambda "1.1" \
        --lambda-delta "0.1"
