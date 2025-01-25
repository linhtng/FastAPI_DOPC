#!/bin/bash

# Check if locust is installed
check_locust() {
    if ! command -v locust &> /dev/null; then
        echo "Error: Locust is not installed"
        echo "Install it using: pip install locust"
        exit 1
    fi
}

# Run check before starting test
check_locust

# This script runs a performance test using Locust in a headless mode to simulate:

# 3 users accessing the DOPC application concurrently.
# A spawn rate of 1 user per second.
# A run time of 10 seconds.
# A request rate of 2 requests per second.
# The test configuration can be modified by changing the variables below.

# Test Configuration
USERS=3
SPAWN_RATE=1
RUN_TIME=10s
REQUEST_RATE=2  # requests per second

echo "Starting load test..."
echo "Configuration:"
echo "- Users: $USERS"
echo "- Spawn rate: $SPAWN_RATE"
echo "- Run time: $RUN_TIME"
echo "- Host: $HOST"
echo "- Request rate: $REQUEST_RATE/sec"

# Create results directory if not exists
mkdir -p load_test_results

# Run test with reduced load
locust -f locustfile.py \
    --headless \
    --users $USERS \
    --spawn-rate $SPAWN_RATE \
    --run-time $RUN_TIME \
    --csv=load_test_results/load_test_$(date +%Y%m%d_%H%M%S) \
    --only-summary | tee load_test_results/latest_run.log

echo "Test complete. Results saved in load_test_results/"