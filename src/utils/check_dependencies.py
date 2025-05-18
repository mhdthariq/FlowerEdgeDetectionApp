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
        import tkinter as tk
        print(f"Tkinter {tk.TkVersion}")
    except ImportError:
        missing_packages.append("tkinter")
        
    try:
        import ttkbootstrap
        print(f"ttkbootstrap {ttkbootstrap.__version__}")
        print(f"Available themes: {len(ttkbootstrap.Style().theme_names())}")
    except ImportError:
        missing_packages.append("ttkbootstrap")
    except Exception as e:
        print(f"ttkbootstrap is installed but encountered an error: {e}")
    
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
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
        print(f"\nScreen resolution: {screen_width}x{screen_height}")
    except:
        pass

if __name__ == "__main__":
    check_dependencies()