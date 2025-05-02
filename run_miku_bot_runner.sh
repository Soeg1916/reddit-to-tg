#!/bin/bash

# This is a special script for the run_miku_bot workflow
# It bypasses the flask app completely to avoid port conflicts

echo "========================================"
echo "MIKU BOT STANDALONE LAUNCHER ACTIVATED!"
echo "This will run WITHOUT Flask to avoid port conflicts"
echo "========================================"

# Kill any existing bot processes
pkill -f "python main_run_bot.py" || true
pkill -f "python main_bot_only.py" || true
pkill -f "python run_standalone.py" || true

# Clean up lock files
rm -f /tmp/bot_running.txt
rm -f /tmp/web_interface_running.txt
rm -f /tmp/bot_failed.txt

# Run the standalone bot directly
python main_run_bot.py