#!/bin/bash

# Default to 1 if WEB_CONCURRENCY is not set
NUM_INSTANCES=${WEB_CONCURRENCY:-3}

# Define a function to run the CLI tool
run_cli_tool() {
    INSTANCE_ID=$1
    python3 src/entrypoint.py create-load-balancer --nginx-port=$((PORT + INSTANCE_ID)) --heroku-api-key=$HEROKU_API_KEY --pipeline-identifier=$PIPELINE_IDENTIFIER
    mv nginx.conf /etc/nginx/nginx-${INSTANCE_ID}.conf
}

# Export the function so GNU Parallel can use it
export -f run_cli_tool

# Run the function in parallel instances
parallel -j $NUM_INSTANCES run_cli_tool ::: $(seq 0 $((NUM_INSTANCES - 1)))

# Concatenate all Nginx configuration files into one
cat /etc/nginx/nginx-*.conf > /etc/nginx/nginx.conf

# Start Nginx in the foreground
nginx -g 'daemon off;'
