CURRENT_PATH=$(pwd)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_times.py --files-prefix "results-machine-" \
                        --files-n "14" \
                        --path "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/LL(15,K-10)-16machines" \
                        --function "Pigo Face Detect" \
                        --fanout "15" \
                        --threshold "10" \
                        --job-duration "0.27" \
                        --with-model \
                        --model-name "M/M/1/10" \
                        -k "10"