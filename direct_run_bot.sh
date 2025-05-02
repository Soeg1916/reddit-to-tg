#!/bin/bash
# Direct script to run the Miku bot without ANY Python module imports

echo "========================================================"
echo "🤖 DIRECT MIKU BOT LAUNCHER SCRIPT 🤖"
echo "========================================================"
echo "This script explicitly runs the bot with:"
echo "- 3-minute Reddit posting interval"
echo "- Strict duplicate prevention"
echo "- NO port conflicts"
echo "========================================================"

# Kill any running processes
pkill -f "python.*direct_miku_bot.py" || true
pkill -f "python.*flask" || true
sleep 1

# Force the environment variable
export REPL_WORKFLOW="run_miku_bot"

# Make our scripts executable
chmod +x direct_miku_bot.py
chmod +x run_standalone_bot.sh
chmod +x run_miku_workflow_launcher.py

# Run the bot directly
echo "Starting Miku Bot..."
exec python direct_miku_bot.py