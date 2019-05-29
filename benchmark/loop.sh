#!/bin/bash
for i in {0..10}
do
   ../machines-setup/python_scripts/configure_scheduler.sh $i
   sleep 30
   ./bench_multi_machine_pigo.sh
   sleep 300
done