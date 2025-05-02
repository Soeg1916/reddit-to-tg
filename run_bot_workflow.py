#!/usr/bin/env python3
"""
DEDICATED STANDALONE SCRIPT FOR run_miku_bot WORKFLOW
This script does NOT import Flask or any web components.
"""
import os
import sys
import time
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("=============================================")
    print("✅ MIKU BOT STANDALONE MODE ACTIVATED!")
    print("This will run WITHOUT Flask to avoid port conflicts")
    print("=============================================")
    
    # Clean up existing lock files
    for file_path in ['/tmp/bot_running.txt', '/tmp/web_interface_running.txt', '/tmp/bot_failed.txt']:
        if os.path.exists(file_path):
            print(f"Removing lock file: {file_path}")
            os.remove(file_path)
    
    # Set the marker file that the bot is running
    with open('/tmp/bot_running.txt', 'w') as f:
        f.write('1')
        
    try:
        # Import bot components directly
        from api_clients import initialize_reddit_client
        from reddit_tracker import initialize_last_post_ids
        from bot import setup_bot
        
        # Initialize the Reddit client
        reddit = initialize_reddit_client()
        
        # Initialize Reddit tracking
        initialize_last_post_ids()
        
        # Set up and start the bot
        updater = setup_bot()
        
        if updater:
            print("Bot started successfully!")
            # Keep the bot running
            updater.idle()
        else:
            print("Failed to start bot. Check your TELEGRAM_BOT_TOKEN.")
            
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        import traceback
        traceback.print_exc()
        
        # Create error marker
        with open('/tmp/bot_failed.txt', 'w') as f:
            f.write(str(e))
        
        # Keep the process alive even after an error
        while True:
            logger.error("Error running bot. Waiting 60 seconds before retry...")
            time.sleep(60)
    finally:
        # Clean up our marker file when the bot exits
        if os.path.exists('/tmp/bot_running.txt'):
            os.remove('/tmp/bot_running.txt')