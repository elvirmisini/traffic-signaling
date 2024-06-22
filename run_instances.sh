#!/bin/bash

# Function to execute main.py with the given parameters
run_instance() {
    local instance_name=$1
    local variant=$2
    local version=$3
    nohup python3 main.py -i $instance_name -va $variant -ve $version &
}

# Directory containing input files
input_dir="./input"

# Array to keep track of running PIDs
pids=()

# Loop through each file in the input directory
for file in $input_dir/*
do
    filename=$(basename "$file")
    for version in {1..5}
    do
        # Run the instance and save the PID
        run_instance $filename 1 $version
        pids+=($!)

        # Check if we have reached the limit of 30 concurrent processes
        if [ ${#pids[@]} -ge 30 ]; then
            # Wait for all processes to finish
            for pid in "${pids[@]}"; do
                wait $pid
            done
            # Clear the PID array
            pids=()
        fi
    done
done

# Wait for any remaining processes to finish
for pid in "${pids[@]}"; do
    wait $pid
done

echo "All instances have been executed."
