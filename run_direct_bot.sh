#!/bin/bash

# DIRECT BOT EXECUTION SCRIPT
# This script is designed to be executed directly by the run_miku_bot workflow

echo "===================================================="
echo "🤖 Miku Bot 3.0 - Direct Execution 🤖"
echo "===================================================="

# Kill competing processes
echo "Killing any competing processes..."
pkill -f 'python.*5000' || true
pkill -f 'python.*flask' || true
sleep 1

# Force workflow identification
export REPL_WORKFLOW="run_miku_bot"

# Create marker file to help with identification
touch .run_miku_bot

# Run the bot directly
echo "Starting the bot directly..."
python run_miku_bot.py