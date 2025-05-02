#!/usr/bin/env python3
"""
FINAL MIKU BOT SOLUTION
This script is completely independent and runs without any imports from other files initially.
It sets up a bot with 3-minute Reddit posting and strict duplicate prevention.
"""

import os
import sys
import time
import signal
import socket
import logging
import random
import json
from datetime import datetime
import subprocess

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler("miku_bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("final_miku_solution")

# Set environment variables
os.environ['REPL_WORKFLOW'] = 'run_miku_bot'

# Constants
HISTORY_FILE = "post_history.json"
PID_FILE = "/tmp/final_miku_bot.pid"
LOCK_FILE = "/tmp/final_miku_bot.lock"

def signal_handler(sig, frame):
    """Handle exit signals"""
    logger.info(f"Received signal {sig}, shutting down...")
    cleanup()
    sys.exit(0)

def cleanup():
    """Clean up temp files"""
    for file in [PID_FILE, LOCK_FILE]:
        if os.path.exists(file):
            try:
                os.remove(file)
            except Exception as e:
                logger.error(f"Error removing {file}: {e}")

def create_lock():
    """Create a lock file"""
    try:
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
    except Exception as e:
        logger.error(f"Error creating lock file: {e}")

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_flask_servers():
    """Kill any running Flask servers to avoid port conflicts"""
    try:
        # Find and kill processes using port 5000
        if is_port_in_use(5000):
            logger.info("Port 5000 is in use, attempting to free it...")
            subprocess.run("pkill -f 'python.*flask'", shell=True)
            subprocess.run("pkill -f 'python.*5000'", shell=True)
            time.sleep(1)
            
            if is_port_in_use(5000):
                logger.warning("Could not free port 5000")
            else:
                logger.info("Successfully freed port 5000")
    except Exception as e:
        logger.error(f"Error killing Flask servers: {e}")
  
def run_bot_script():
    """Run the direct bot script"""
    try:
        # Find the direct bot script
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "direct_miku_bot.py")
        
        if not os.path.exists(script_path):
            logger.error(f"Bot script not found: {script_path}")
            return False
            
        logger.info(f"Found bot script: {script_path}")
        
        # Make it executable
        try:
            subprocess.run(['chmod', '+x', script_path], check=True)
        except Exception as e:
            logger.warning(f"Could not make script executable: {e}")
        
        # Run the bot
        logger.info("Starting the bot...")
        os.execl(sys.executable, sys.executable, script_path)
        
        # This should never be reached
        return True
    except Exception as e:
        logger.error(f"Error running bot script: {e}")
        return False

def main():
    """Main function"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Clean up any existing files
        cleanup()
        
        # Create a lock file
        create_lock()
        
        # Create a PID file
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))
        
        # Kill any Flask servers that might be using port 5000
        kill_flask_servers()
        
        # Banner
        logger.info("=" * 50)
        logger.info("🤖 FINAL MIKU BOT SOLUTION 🤖")
        logger.info("✅ 3-minute Reddit posting")
        logger.info("✅ Strict duplicate prevention")
        logger.info("✅ Port conflict resolution")
        logger.info("=" * 50)
        
        # Run the bot
        success = run_bot_script()
        
        if not success:
            logger.error("Failed to start bot")
            return 1
            
        return 0
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        return 1
        
    finally:
        cleanup()

if __name__ == "__main__":
    sys.exit(main())