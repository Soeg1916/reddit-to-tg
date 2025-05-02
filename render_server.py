"""
Special server file for Render deployment.
This ensures the app binds to the PORT environment variable.
"""

import os
from main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting server on port {port}")
    app.run(host="0.0.0.0", port=port)
