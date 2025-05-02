#!/bin/bash
# Special bypass script for run_miku_bot workflow
# This completely bypasses the main.py execution and any port conflicts

echo "================================================================"
echo "MIKU BOT DIRECT EXECUTION - BYPASSING MAIN.PY COMPLETELY"
echo "================================================================"

# Kill any existing bot processes
pkill -f "python.*direct_miku_bot.py" || true
pkill -f "python.*workflow_bot.py" || true

# Remove any lock files
rm -f /tmp/bot_*.txt /tmp/workflow_*.lock

# Set the environment variable explicitly
export REPL_WORKFLOW="run_miku_bot"

# Run the direct bot script
echo "Starting Miku Bot directly..."
exec python direct_miku_bot.py