#!/usr/bin/env python
"""
Django startup script with proper path handling
Run this instead of: python manage.py runserver
"""

import os
import sys
import django
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Add project directory to Python path
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django
django.setup()

# Now run the development server
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    
    print("\n" + "="*70)
    print("  Flood Risk Dashboard - Django Development Server")
    print("="*70)
    print("\nServer starting...")
    print("Access at: http://localhost:8000/\n")
    
    # Run with default settings
    sys.argv = ['manage.py', 'runserver', '0.0.0.0:8000']
    execute_from_command_line(sys.argv)
