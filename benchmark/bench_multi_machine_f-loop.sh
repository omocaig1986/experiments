#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/bin/activate
"$CURRENT_PATH"/env/bin/python bench_multi_machine.py \
  --hosts-file "$CURRENT_PATH/hosts.txt" \
  --function-url "function/exponential-loop" \
  --requests "200" \
  --start-lambda "0.1" \
  --end-lambda "1.0" \
  --lambda-delta "0.05" \
  --poisson

