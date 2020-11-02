#!/bin/bash
#
# P2PFaaS - A framework for FaaS Load Balancing
# Copyright (c) 2020. Gabriele Proietti Mattia <pm.gabriele@outlook.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#
# Bench multiple values of the threshold, from $1 to $2
#
CURRENT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

BLOB_PATH="$CURRENT_PATH/blobs"
BLOB_NAME="family"
BLOB_EXT="jpg"

BLOBS_SIZES=(
  500000
  1000000
  5000000
  8000000
  10000000
  13000000
  15000000
  20000000
)
BLOBS_SIZES_LEN=${#BLOBS_SIZES[@]}

echo "=== Set scheduler to LL(1,6)"
"$CURRENT_PATH"/../machines-setup/python_scripts/configure_pwr_n_scheduler.sh 6

echo "=== Starting loop for blob sizes ==="
for ((i = 0; i < BLOBS_SIZES_LEN; i++)); do
  BLOB_FULL_PATH="$BLOB_PATH/${BLOB_NAME}_${BLOBS_SIZES[i]}bytes.$BLOB_EXT"
  echo "=> Starting test with blob $BLOB_FULL_PATH"

  if test -f "$BLOB_FULL_PATH"; then
    echo "==> Payload exists"
    "$CURRENT_PATH"/bench_multi_machine_blob_f-pigo.sh "$BLOB_FULL_PATH"
  fi

  sleep 30
done
