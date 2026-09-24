import os
import sys

# Add the main project folder to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import your Flask app from app.py
from app import app