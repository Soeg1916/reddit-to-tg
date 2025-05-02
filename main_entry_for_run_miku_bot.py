#!/usr/bin/env python3
"""
This is the ONLY entry point for the run_miku_bot workflow.
It doesn't import anything from other modules to avoid conflicts.
"""
import os
import sys
import subprocess

def main():
    print("=" * 70)
    print("🤖 MIKU BOT WORKFLOW ENTRY POINT 🤖")
    print("✅ Reddit posting interval: every 3 minutes with no duplicates")
    print("✅ Running completely independent bot script")
    print("=" * 70)
    
    # Force set the workflow environment variable
    os.environ['REPL_WORKFLOW'] = 'run_miku_bot'
    
    # Get the path to our dedicated launcher script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_miku_workflow_launcher.py")
    
    if not os.path.exists(script_path):
        print(f"❌ ERROR: Launcher script not found: {script_path}")
        return 1
    
    print(f"✅ Found launcher script: {script_path}")
    
    # Make it executable
    try:
        subprocess.run(['chmod', '+x', script_path], check=True)
    except Exception as e:
        print(f"⚠️ Warning: Could not make script executable: {e}")
    
    # Execute the launcher script directly
    try:
        print("🚀 Launching Miku Bot...")
        os.execv(sys.executable, [sys.executable, script_path])
    except Exception as e:
        print(f"❌ ERROR: Failed to launch bot: {e}")
        return 1
    
    # Should never reach here
    return 0

if __name__ == "__main__":
    sys.exit(main())