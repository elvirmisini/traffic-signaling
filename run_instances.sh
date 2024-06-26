#!/bin/bash

run_instance() {
    local instance_name=$1
    nohup python3 experiment.py $instance_name &
}

input_dir="./input1"

pids=()

for file in $input_dir/*
do
    filename=$(basename "$file")
    for version in {1..2}
    do
        run_instance $filename 
        pids+=($!)

        if [ ${#pids[@]} -ge 10 ]; then

            for pid in "${pids[@]}"; do
                wait $pid
            done

            pids=()
        fi
    done
done

for pid in "${pids[@]}"; do
    wait $pid
done

echo "All instances have been executed."
