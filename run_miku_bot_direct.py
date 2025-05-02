#!/usr/bin/env python3
"""
Direct execution script for the run_miku_bot workflow.
This script is standalone and does not use Flask or any web components.
"""

import os
import sys
import time
import logging
import signal
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("miku_bot_direct.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("miku_bot_direct")

# Signal handling for graceful shutdown
def signal_handler(sig, frame):
    logger.info(f"Received signal {sig}, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    """Main entry point - directly run the bot with no Flask"""
    
    logger.info("=" * 60)
    logger.info("🚀 DIRECT MIKU BOT LAUNCHER 🚀")
    logger.info("This bypasses main.py and Flask to avoid port conflicts")
    logger.info("=" * 60)
    
    # Force the workflow environment
    os.environ["REPL_WORKFLOW"] = "run_miku_bot"
    
    # Kill any competing processes
    try:
        logger.info("Killing any competing processes...")
        subprocess.run("pkill -f 'python.*flask'", shell=True)
        subprocess.run("pkill -f 'python.*5000'", shell=True)
        time.sleep(1)
    except Exception as e:
        logger.error(f"Error killing processes: {e}")
    
    # Find the direct_miku_bot.py script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "direct_miku_bot.py")
    
    if os.path.exists(script_path):
        logger.info(f"Found bot script: {script_path}")
        
        # Make it executable
        try:
            subprocess.run(['chmod', '+x', script_path], check=True)
        except Exception as e:
            logger.warning(f"Could not make script executable: {e}")
        
        # Execute the script directly
        logger.info("Executing direct_miku_bot.py...")
        os.execl(sys.executable, sys.executable, script_path)
    else:
        logger.error(f"Bot script not found: {script_path}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())