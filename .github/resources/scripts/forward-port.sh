#!/usr/bin/env bash

usage() {
    echo "Usage: $0 [-q] <KUBEFLOW_NS> <APP_NAME> <LOCAL_PORT> <REMOTE_PORT>"
    exit 1
}

QUIET=0
while getopts "q" opt; do
    case $opt in
        q) QUIET=1 ;;
        *) usage ;;
    esac
done
shift $((OPTIND -1))

if [ $# -ne 4 ]; then
    usage
fi

KUBEFLOW_NS=$1
APP_NAME=$2
LOCAL_PORT=$3
REMOTE_PORT=$4

MAX_RETRIES=10
RETRY_DELAY=5

# First check if the pod exists
POD_NAME=$(kubectl get pods -n "$KUBEFLOW_NS" -l "app=$APP_NAME" -o jsonpath='{.items[0].metadata.name}')
if [ -z "$POD_NAME" ]; then
    echo "Error: No pod found with app=$APP_NAME in namespace $KUBEFLOW_NS"
    exit 1
fi

echo "POD_NAME=$POD_NAME"

# Kill any existing port-forward processes for this port
echo "Checking for existing port-forward processes on port $LOCAL_PORT..."
for pid in $(lsof -ti:$LOCAL_PORT); do
    echo "Killing existing process $pid on port $LOCAL_PORT"
    kill -9 $pid 2>/dev/null || true
done

# Start port forwarding
if [ $QUIET -eq 1 ]; then
    kubectl port-forward --address 0.0.0.0 -n "$KUBEFLOW_NS" "$POD_NAME" "$LOCAL_PORT:$REMOTE_PORT" > /dev/null 2>&1 &
else
    kubectl port-forward --address 0.0.0.0 -n "$KUBEFLOW_NS" "$POD_NAME" "$LOCAL_PORT:$REMOTE_PORT" &
fi

PORT_FORWARD_PID=$!
echo "Started port-forward with PID $PORT_FORWARD_PID"

# Verify the port is available with retry logic
echo "Checking if port $LOCAL_PORT is accessible..."
for i in $(seq 1 $MAX_RETRIES); do
    # Check if port forwarding process is still running
    if ! ps -p $PORT_FORWARD_PID > /dev/null; then
        echo "Port forwarding process died. Retrying..."
        if [ $QUIET -eq 1 ]; then
            kubectl port-forward --address 0.0.0.0 -n "$KUBEFLOW_NS" "$POD_NAME" "$LOCAL_PORT:$REMOTE_PORT" > /dev/null 2>&1 &
        else
            kubectl port-forward --address 0.0.0.0 -n "$KUBEFLOW_NS" "$POD_NAME" "$LOCAL_PORT:$REMOTE_PORT" &
        fi
        PORT_FORWARD_PID=$!
    fi
    
    # Try to connect to the port
    if nc -z localhost $LOCAL_PORT; then
        echo "Port $LOCAL_PORT is accessible after $i attempts!"
        # Wait a bit more to ensure the connection is stable
        sleep 2
        exit 0
    fi
    
    echo "Port $LOCAL_PORT not accessible yet. Retrying in $RETRY_DELAY seconds... (Attempt $i/$MAX_RETRIES)"
    sleep $RETRY_DELAY
done

echo "ERROR: Failed to establish port forwarding to $LOCAL_PORT after $MAX_RETRIES attempts."
exit 1
