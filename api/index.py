import os
import sys

# Ensure the root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except ImportError:
    from exp import app

# Vercel's WSGI bridge automatically looks for the 'app' instance
