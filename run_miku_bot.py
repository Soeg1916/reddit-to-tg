#!/usr/bin/env python3
"""
Start only the Miku bot in standalone mode. 
This script is designed to be run by the run_miku_bot workflow.
It ONLY starts the bot without any web interface to avoid port conflicts.
"""

import os
import sys
import time
import signal
import socket
import logging
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("miku_bot.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("miku_bot_runner")

# Check if a port is in use
def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# Signal handling for graceful shutdown
def signal_handler(sig, frame):
    """Handle signals gracefully"""
    logger.info(f"Received signal {sig}, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# Wait for internet connectivity
def wait_for_internet():
    """Wait for internet connectivity"""
    connected = False
    logger.info("Waiting for internet connectivity...")
    for _ in range(30):  # Try for up to 30 seconds
        try:
            # Try to connect to Telegram servers
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect(("api.telegram.org", 443))
            s.close()
            connected = True
            break
        except (socket.error, socket.timeout):
            time.sleep(1)
    
    if connected:
        logger.info("Internet connectivity confirmed.")
    else:
        logger.warning("Could not confirm internet connectivity, but continuing anyway.")

def main():
    try:
        # Create marker file to indicate workflow
        with open(".run_miku_bot", "w") as f:
            f.write("1")
        
        # Set the correct environment variable
        os.environ["REPL_WORKFLOW"] = "run_miku_bot"
        
        # Handle port conflicts
        if is_port_in_use(5000):
            logger.warning("Port 5000 already in use, killing competing processes...")
            subprocess.run("pkill -f 'python.*flask'", shell=True)
            subprocess.run("pkill -f 'python.*5000'", shell=True)
            time.sleep(1)
        
        # Wait for internet
        wait_for_internet()
        
        # Initialize Telegram bot
        logger.info("=" * 60)
        logger.info("🚀 INITIALIZING MIKU BOT IN STANDALONE MODE")
        logger.info("=" * 60)
        
        # Create a marker file to indicate the bot is running
        with open("/tmp/bot_running.txt", "w") as f:
            f.write("1")
        
        # Run the direct_miku_bot.py script which contains the complete bot implementation
        direct_bot_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "direct_miku_bot.py")
        
        if os.path.exists(direct_bot_path):
            logger.info(f"Executing direct bot script: {direct_bot_path}")
            subprocess.run(["chmod", "+x", direct_bot_path], check=True)
            os.execl(sys.executable, sys.executable, direct_bot_path)
        else:
            logger.error(f"Direct bot script not found: {direct_bot_path}")
            return 1
        
    except Exception as e:
        logger.error(f"Error in run_miku_bot.py: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())