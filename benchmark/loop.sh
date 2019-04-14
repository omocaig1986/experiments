#!/bin/bash
for i in {0..9}
do
   ../machines-setup/python_scripts/configure_scheduler.sh $i
   ./bench_multi_machine_pigo.sh
done