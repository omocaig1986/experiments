#!/bin/sh
CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_times_distribution.py --files-prefix "req-times-" \
                        --path "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/SingleNode/Loop/NS(K10)-heat/_test_multi_get-03302019-114919" \
                        --function "Loop" \
                        --fanout "1" \
                        --threshold "10" \
                        --job-duration "1.02" \
                        -k "10" \
                        --start-lambda "0.1" \
                        --end-lambda "3.0" \
                        --lambda-delta "0.1" \
                        --bins "30" \
                        --machine-id "0" \
                        --data-files "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/MultiNode/Loop/LL(1,K-2)-16machines-heat/_test_multi_machine-03302019-163137:/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/SingleNode/Loop/NS(K10)-heat/_test_multi_get-03302019-114919"