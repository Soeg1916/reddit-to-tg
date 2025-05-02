#!/bin/bash

# Get the current workflow name
WORKFLOW=${REPL_WORKFLOW:-"unknown"}

echo "Current workflow: $WORKFLOW"

# If it's the run_miku_bot workflow, run the standalone bot
if [ "$WORKFLOW" = "run_miku_bot" ]; then
    echo "========================================"
    echo "DETECTED BOT WORKFLOW"
    echo "Starting standalone bot without Flask"
    echo "========================================"
    exec python standalone_bot.py
else
    # Otherwise, run the regular main.py
    echo "========================================"
    echo "NORMAL WORKFLOW"
    echo "Starting combined mode (web + bot)"
    echo "========================================"
    exec python main.py
fi
