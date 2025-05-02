#!/bin/bash
# This script is meant to be used by the run_miku_bot workflow
# It runs a process that keeps the bot alive

echo "================================================================"
echo "WORKFLOW-SPECIFIC MIKU BOT LAUNCHER"
echo "Using keep_alive.py to maintain bot process"
echo "================================================================"

# Clean up any previous runs
rm -f /tmp/bot_keeper.lock /tmp/bot_running.txt /tmp/bot_failed.txt

# Set the workflow name explicitly in the environment
export REPL_WORKFLOW="run_miku_bot"

# Start the keeper process in the background
exec python keep_alive.py