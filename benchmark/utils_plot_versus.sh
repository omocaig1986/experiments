CURRENT_PATH=$(dirname $0)

source $CURRENT_PATH/env/bin/activate
$CURRENT_PATH/env/bin/python utils_plot_versus.py \
                                --first-file "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/LL(4,K-10)-5machines/results-machine-00.txt" \
                                --second-file "/Users/gabry3795/Cloud/Google Drive/Università/Magistrale/Thesis/Data/BladeServers/LL(15,K-10)-16machines/results-machine-00.txt" \
                                --first-title "LL(4,K-10)-5machines" \
                                --second-title "LL(15,K-10)-16machines" \
                                --x-axis "λ" \
                                --model-name "M/M/1/10" \
                                --model-k "10" \
                                --model-job-len "0.27" \
                                --out-dir ${CURRENT_PATH}"/tmp"