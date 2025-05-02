"""
Main entry point that routes between bot-only mode and web-only mode.
"""

import sys
import os

# Check for the run_miku_bot workflow by looking for marker file
IS_RUN_MIKU_BOT = os.path.exists('.run_miku_bot')
# Check for Gunicorn
IS_GUNICORN = 'gunicorn' in ' '.join(sys.argv)

# Import our app
from app_simple import app as flask_app

# Export the app for Gunicorn to use
app = flask_app  

# If we're in the run_miku_bot workflow and not under Gunicorn
if IS_RUN_MIKU_BOT and not IS_GUNICORN:
    print("✅ MIKU BOT WORKFLOW DETECTED")
    print("✅ EXECUTING DIRECT SCRIPT WITH 3-MINUTE REDDIT POSTS")
    
    # Kill any competing processes
    print("Killing any competing processes...")
    os.system("pkill -f 'python.*flask'")
    
    # Run the dedicated bot script
    print("Running direct runner: direct_miku_bot.py")
    os.system(f"python direct_miku_bot.py")

# When run directly outside of Gunicorn
if __name__ == '__main__' and not IS_GUNICORN:
    # Run the Flask app if not in the bot workflow
    if not IS_RUN_MIKU_BOT:
        print("Starting web server in standalone mode...")
        port = int(os.environ.get("PORT", 5000))
        flask_app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
