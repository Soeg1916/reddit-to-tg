#!/bin/bash

echo "==============================================="
echo "✅ DIRECT BOT EXECUTION SHELL SCRIPT"
echo "This script bypasses the main.py entry point"
echo "==============================================="

# Remove any lock files
for file in /tmp/bot_running.txt /tmp/web_interface_running.txt /tmp/bot_failed.txt
do
  if [ -f "$file" ]; then
    echo "Removing lock file: $file"
    rm "$file"
  fi
done

# Run the direct bot runner
python direct_bot_runner.py