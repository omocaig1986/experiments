#!/bin/bash
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

# shellcheck disable=SC1090
source "$CURRENT_PATH"/env/Scripts/activate
"$CURRENT_PATH"/env/Scripts/python sync_machines.py docker ./hosts.txt
