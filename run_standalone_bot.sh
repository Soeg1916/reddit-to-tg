#!/bin/bash
# This script is specifically designed for the run_miku_bot workflow
# It directly runs the standalone bot script that doesn't rely on main.py

echo "================================================================"
echo "STANDALONE MIKU BOT LAUNCHER"
echo "This script runs the bot on port 8080 with 3-minute Reddit posts"
echo "================================================================"

# Kill any existing processes
pkill -f "python.*standalone_workflow_bot.py" || true
pkill -f "python.*direct_miku_bot.py" || true

# Clean up any lock files
rm -f /tmp/miku_bot.pid /tmp/miku_bot_running.txt /tmp/miku_bot_error.txt

# Set the environment variable explicitly
export REPL_WORKFLOW="run_miku_bot"

# Run the bot
echo "Starting standalone Miku Bot..."
exec python standalone_workflow_bot.py