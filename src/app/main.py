from src.interface.splash_screen import SplashScreen
from src.app.edge_detection_app import EdgeDetectionApp
import tkinter as tk
import ttkbootstrap as ttk
import threading
import time
import platform
import os
import sys

# Add project root to path to enable imports from anywhere
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))

# Import application components


def detect_platform():
    """Detect the current operating system platform"""
    return platform.system().lower() if platform.system() else "unknown"


def get_asset_path(relative_path):
    """Get the absolute path to an asset file

    Parameters:
    - relative_path: The path relative to the assets directory

    Returns:
    - Absolute path to the asset
    """
    # Try both the assets and Assets directories (for backward compatibility)
    base_dirs = [
        os.path.join(os.path.dirname(os.path.dirname(
            os.path.dirname(__file__))), 'assets'),
        os.path.join(os.path.dirname(os.path.dirname(
            os.path.dirname(__file__))), 'Assets')
    ]

    for base_dir in base_dirs:
        asset_path = os.path.join(base_dir, relative_path)
        if os.path.exists(asset_path):
            return asset_path

    # If not found, return a path from the first base_dir (will likely fail later)
    return os.path.join(base_dirs[0], relative_path)


def run_app_with_splash():
    """Initialize and run the application with a splash screen"""
    # Create main window but keep it hidden
    root = ttk.Window(themename="darkly", title="Flower Edge Detection")
    root.withdraw()

    # Set window icon if possible
    try:
        icon_path = get_asset_path('icons/app_icon.png')
        root.iconphoto(True, tk.PhotoImage(file=icon_path))
    except Exception as e:
        print(f"Warning: Could not set icon: {e}")

    # Platform-specific window adjustments
    platform_system = detect_platform()
    if platform_system == "windows":
        # Windows-specific adjustments
        root.attributes("-alpha", 0.98)  # Slight transparency for modern look
    elif platform_system == "darwin":
        # macOS-specific adjustments
        try:
            root.tk.call('::tk::unsupported::MacWindowStyle',
                         'style', root._w, 'document', 'modified')
        except:
            pass

    # Create splash screen
    icon_path = get_asset_path('icons/app_icon.png')
    splash = SplashScreen(root, image_path=icon_path, timeout=3000)
    splash.show()

    # Create app instance
    app = EdgeDetectionApp(root)

    # Simulate loading tasks
    def loading_tasks():
        time.sleep(0.8)
        splash.update_message("Loading UI components...")
        time.sleep(0.7)
        splash.update_message("Initializing image processors...")
        time.sleep(0.7)
        splash.update_message("Preparing application...")
        time.sleep(0.5)

    # Run loading tasks in background thread
    threading.Thread(target=loading_tasks).start()

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    run_app_with_splash()
