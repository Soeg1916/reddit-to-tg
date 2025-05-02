#!/usr/bin/env python3
"""
Dedicated script for running ONLY the Miku bot in the run_miku_bot workflow.
This completely skips the Flask app to avoid port conflicts.
"""

import os
import sys
import signal
import logging
import time
import subprocess
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("miku_bot_runner.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("miku_bot_runner")

# Get the correct environment
os.environ["REPL_WORKFLOW"] = "run_miku_bot"

# Signal handling
def signal_handler(sig, frame):
    logger.info(f"Received signal {sig}, shutting down...")
    cleanup()
    sys.exit(0)

def cleanup():
    logger.info("Performing cleanup...")
    try:
        if os.path.exists("/tmp/bot_running.txt"):
            os.remove("/tmp/bot_running.txt")
    except Exception as e:
        logger.error(f"Error during cleanup: {e}")

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_processes():
    """Kill competing processes"""
    logger.info("Killing any competing processes...")
    try:
        subprocess.run("pkill -f 'python.*flask'", shell=True)
        subprocess.run("pkill -f 'python.*5000'", shell=True)
        time.sleep(1)
    except Exception as e:
        logger.error(f"Error killing processes: {e}")

def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("🤖 MIKU BOT RUNNER v3.0 🤖")
    logger.info("This script directly runs the Miku bot without Flask")
    logger.info("=" * 60)
    
    # Fix the port issue first
    if is_port_in_use(5000):
        logger.warning("Port 5000 is already in use, killing competing processes...")
        kill_processes()
    
    # List of possible bot scripts in order of preference
    scripts = [
        "direct_miku_bot.py",
        "final_miku_solution.py",
        "run_standalone_bot.sh",
        "direct_run_bot.sh"
    ]
    
    # Try each script until one works
    for script in scripts:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
        
        if not os.path.exists(script_path):
            logger.warning(f"Script {script} not found, trying next...")
            continue
        
        logger.info(f"Found bot script: {script}")
        
        # Make it executable
        try:
            subprocess.run(['chmod', '+x', script_path], check=True)
        except Exception as e:
            logger.warning(f"Could not make script executable: {e}")
        
        # Execute the script
        logger.info(f"Executing {script}...")
        
        try:
            if script.endswith(".sh"):
                logger.info("Running shell script...")
                os.execl("/bin/bash", "bash", script_path)
            else:
                logger.info("Running Python script...")
                os.execl(sys.executable, sys.executable, script_path)
        except Exception as e:
            logger.error(f"Error executing {script}: {e}")
    
    # If we get here, all scripts failed
    logger.error("All bot scripts failed to execute")
    return 1

if __name__ == "__main__":
    sys.exit(main())