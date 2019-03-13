CURRENT_PATH=$(pwd)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
                        --files-n "14" \
                        --path "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/LL(1,K-2)-14machines" \
                        --function "Pigo Face Detect" \
                        --fanout "1" \
                        --threshold "2" \
                        --job-duration "0.27" \
                        --with-model \
                        --model-name "M/M/1/10" \
                        -k "10"