#!/usr/bin/env python3
"""
This is a Python wrapper that completely bypasses main.py
It's specifically designed for the run_miku_bot workflow
"""
import os
import sys
import subprocess

if __name__ == "__main__":
    print("=" * 60)
    print("MIKU BOT DIRECT LAUNCHER")
    print("Bypassing main.py and all Flask dependencies")
    print("=" * 60)
    
    # Remove any existing lock files
    for file_path in ['/tmp/bot_running.txt', '/tmp/web_interface_running.txt', '/tmp/bot_failed.txt']:
        if os.path.exists(file_path):
            print(f"Removing lock file: {file_path}")
            os.remove(file_path)
    
    # Check if we're in the run_miku_bot workflow
    workflow = os.environ.get('REPL_WORKFLOW', '')
    print(f"Current workflow: {workflow}")
    
    # Execute the direct bot script
    try:
        # Use subprocess to run the bot directly to completely isolate from this process
        print("Launching direct_bot_only.py...")
        subprocess.call(["python", "direct_bot_only.py"])
    except Exception as e:
        print(f"Error launching bot: {e}")
        sys.exit(1)