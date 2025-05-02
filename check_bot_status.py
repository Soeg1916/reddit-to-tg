#!/usr/bin/env python3
"""
Simple utility to check the bot's status and ensure it's running properly.
"""
import os
import time
import json
import datetime

def get_bot_status():
    """Check if the bot is running and gather status information"""
    status = {
        "bot_running": os.path.exists("/tmp/bot_running.txt"),
        "web_running": os.path.exists("/tmp/web_interface_running.txt"),
        "bot_failed": os.path.exists("/tmp/bot_failed.txt"),
        "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "uptime": None,
        "error_message": None
    }
    
    # If the bot is running, check how long it's been up
    if status["bot_running"]:
        try:
            mtime = os.path.getmtime("/tmp/bot_running.txt")
            now = time.time()
            uptime_seconds = int(now - mtime)
            uptime_str = f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"
            status["uptime"] = uptime_str
        except Exception as e:
            status["uptime"] = f"Error calculating uptime: {e}"
    
    # If the bot failed, get the error message
    if status["bot_failed"]:
        try:
            with open("/tmp/bot_failed.txt", "r") as f:
                status["error_message"] = f.read().strip()
        except Exception as e:
            status["error_message"] = f"Error reading failure file: {e}"
    
    return status

def main():
    """Display the bot status in a user-friendly format"""
    status = get_bot_status()
    
    print("\n===== MIKU BOT STATUS =====")
    print(f"Time: {status['current_time']}")
    print(f"Bot running: {'✅ YES' if status['bot_running'] else '❌ NO'}")
    print(f"Web running: {'✅ YES' if status['web_running'] else '❌ NO'}")
    print(f"Bot failed: {'❌ YES' if status['bot_failed'] else '✅ NO'}")
    
    if status["uptime"]:
        print(f"Bot uptime: {status['uptime']}")
    
    if status["error_message"]:
        print("\n==== ERROR MESSAGE ====")
        print(status["error_message"])
    
    print("\n=== ENVIRONMENT INFO ===")
    print(f"Workflow: {os.environ.get('REPL_WORKFLOW', 'Not in a workflow')}")
    print(f"Repl ID: {os.environ.get('REPL_ID', 'Unknown')}")
    print(f"Repl Owner: {os.environ.get('REPL_OWNER', 'Unknown')}")
    
    # Check for Telegram config
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN", None)
    if telegram_token:
        print(f"Telegram Token: {'✅ Configured (hidden)'}")
    else:
        print(f"Telegram Token: {'❌ Not configured'}")
        
    # Check for Reddit config
    reddit_client_id = os.environ.get("REDDIT_CLIENT_ID", None)
    reddit_client_secret = os.environ.get("REDDIT_CLIENT_SECRET", None)
    if reddit_client_id and reddit_client_secret:
        print(f"Reddit API: {'✅ Fully configured'}")
    elif reddit_client_id or reddit_client_secret:
        print(f"Reddit API: {'⚠️ Partially configured'}")
    else:
        print(f"Reddit API: {'❌ Not configured'}")
    
    # Print running processes
    print("\n=== RUNNING PROCESSES ===")
    try:
        import subprocess
        result = subprocess.run(["ps", "-ef"], capture_output=True, text=True)
        processes = result.stdout.strip().split("\n")
        
        # Filter for python and main_run_bot.py
        python_processes = []
        for proc in processes:
            if "python" in proc:
                if "main_run_bot" in proc or "bot_only" in proc:
                    python_processes.append("✅ " + proc)
                elif "flask" in proc or "gunicorn" in proc:
                    python_processes.append("🌐 " + proc)
                else:
                    python_processes.append("   " + proc)
        
        if python_processes:
            print("\n".join(python_processes))
        else:
            print("No Python processes found.")
    except Exception as e:
        print(f"Error getting process list: {e}")
        
    return status

if __name__ == "__main__":
    main()