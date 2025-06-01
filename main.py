#!/usr/bin/env python3
"""
Edge Detection Application
-------------------------
Main entry point for the Flower Edge Detection Application.
"""

import os
import sys
import logging

# Add the project root directory to the Python path
# This allows imports from the src package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('edge_detection')


def main():
    """Main entry point for the application"""
    try:
        # Import the main app module
        from src.app.main import run_pyqt_app_with_splash

        # Run the application
        logger.info("Starting Edge Detection Application")
        run_pyqt_app_with_splash()
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        print(f"Error: Failed to import required modules: {e}")
        print("Make sure you have installed all the required dependencies.")
        print("Try running: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting application: {e}", exc_info=True)
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
