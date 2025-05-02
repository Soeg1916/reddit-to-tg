#!/usr/bin/env python3
"""
CRITICAL: This script runs ONLY in the run_miku_bot workflow.
It does not import any Flask modules and runs on a different port.
"""
import os
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('miku_workflow')

def run_direct_command():
    """Run the direct bot command without any Flask or port conflicts"""
    logger.info("=" * 70)
    logger.info("🚀 STARTING MIKU BOT IN WORKFLOW MODE 🚀")
    logger.info("=" * 70)
    
    # Force the environment variable
    os.environ['REPL_WORKFLOW'] = 'run_miku_bot'
    logger.info("✅ Set REPL_WORKFLOW=run_miku_bot")
    
    # Execute the direct bot script
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "direct_miku_bot.py")
    
    if not os.path.exists(script_path):
        logger.error(f"❌ Bot script not found: {script_path}")
        return 1
    
    logger.info(f"✅ Found bot script: {script_path}")
    logger.info("🔄 Executing bot directly...")
    
    # Make the script executable
    try:
        subprocess.run(['chmod', '+x', script_path], check=True)
    except Exception as e:
        logger.warning(f"⚠️ Could not make script executable: {e}")
    
    # Use execv to replace the current process
    # This ensures we don't create child processes that can be orphaned
    logger.info("🤖 Bot starting now - direct execution")
    os.execv(sys.executable, [sys.executable, script_path])
    
    # Should never reach here
    return 0

if __name__ == "__main__":
    # Check if we're in the run_miku_bot workflow
    workflow = os.environ.get('REPL_WORKFLOW', '')
    
    if workflow != 'run_miku_bot':
        logger.warning(f"⚠️ Not in run_miku_bot workflow (current: {workflow})")
        logger.info("🔄 Setting workflow environment variable...")
        os.environ['REPL_WORKFLOW'] = 'run_miku_bot'
    
    sys.exit(run_direct_command())