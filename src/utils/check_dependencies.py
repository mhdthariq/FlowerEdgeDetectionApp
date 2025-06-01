import sys
import platform


def check_dependencies():
    """Check if all required dependencies are installed and report their versions."""
    missing_packages = []

    # Check Python version
    print(f"Python {sys.version.split()[0]}")

    # OS Information
    print(f"Platform: {platform.system()} {platform.release()}")

    print("\n--- Core Libraries ---")
    try:
        import cv2
        print(f"OpenCV {cv2.__version__}")
    except ImportError:
        missing_packages.append("opencv-python")

    try:
        import numpy as np
        print(f"NumPy {np.__version__}")
    except ImportError:
        missing_packages.append("numpy")

    try:
        from PIL import Image, ImageTk
        print(f"PIL {Image.__version__}")
    except ImportError:
        missing_packages.append("Pillow")

    print("\n--- UI Libraries ---")
    try:
        from PyQt6.QtCore import QT_VERSION_STR
        from PyQt6.QtWidgets import QApplication
        print(f"PyQt6 {QT_VERSION_STR}")
        # Check if QApplication can be initialized (basic check for Qt platform plugins)
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        print("PyQt6 QApplication initialized successfully.")
    except ImportError:
        missing_packages.append("PyQt6")
    except Exception as e:
        print(f"PyQt6 is installed but encountered an error: {e}")
        missing_packages.append("PyQt6 (runtime error)")

    # Check threading support
    print("\n--- Additional Features ---")
    try:
        import threading
        print(f"Threading is available")
    except ImportError:
        missing_packages.append("threading")

    # Check for image saving functionality
    try:
        import os
        print(f"OS module is available for file operations")
    except ImportError:
        missing_packages.append("os")

    if missing_packages:
        print("\nMissing packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall required packages using:")
        print("pip install -r requirements.txt")
    else:
        print("\nAll dependencies are installed!")

    # Display screen resolution info if tkinter is available
    try:
        # root = tk.Tk() # Removed Tkinter code
        # screen_width = root.winfo_screenwidth() # Removed Tkinter code
        # screen_height = root.winfo_screenheight() # Removed Tkinter code
        # root.destroy() # Removed Tkinter code
        # print(f"\\nScreen resolution: {screen_width}x{screen_height}") # Removed Tkinter code
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        screen = app.primaryScreen()
        if screen:
            geometry = screen.geometry()
            print(
                f"\\nScreen resolution: {geometry.width()}x{geometry.height()}")
        else:
            print("\\nCould not determine screen resolution using PyQt6.")
    except Exception as e:  # More generic exception handling
        print(f"\\nCould not determine screen resolution: {e}")
        pass


if __name__ == "__main__":
    check_dependencies()
