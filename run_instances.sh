#!/bin/bash

run_instance() {
    local instance_name=$1
    local variant=$2
    local version=$3
    nohup python3 ils_ssga.py -i $instance_name -va $variant -ve $version &
}

input_dir="./input"

pids=()

for file in $input_dir/*
do
    filename=$(basename "$file")
    for version in {1..5}
    do
        run_instance $filename 7 $version
        pids+=($!)

        if [ ${#pids[@]} -ge 50 ]; then

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
