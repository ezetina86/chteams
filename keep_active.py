"""Convenience wrapper script to run the chteams utility.

This script ensures the 'src' directory is in the Python path and executes
 the main entry point of the package.
"""
import sys
import os

# Add src to path so we can import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chteams.main import main

if __name__ == "__main__":
    main()