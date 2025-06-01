from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from src.app.edge_detection_app import EdgeDetectionApp
import platform
import os
import sys

# Add project root to path to enable imports from anywhere
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))

# Import application components (EdgeDetectionApp is already imported)


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
    print(f"Warning: Asset not found at expected paths: {relative_path}")
    return os.path.join(base_dirs[0], relative_path)


def run_pyqt_app_with_splash():
    """Initialize and run the PyQt application with a splash screen"""
    # It's good practice to handle high DPI scaling for PyQt6
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(
            Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(
            Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Set application icon
    try:
        app_icon_path = get_asset_path('icons/app_icon.png')
        if os.path.exists(app_icon_path):
            app.setWindowIcon(QIcon(app_icon_path))
        else:
            print(f"Warning: Application icon not found at {app_icon_path}")
    except Exception as e:
        print(f"Warning: Could not set application icon: {e}")

    # Create and show splash screen
    # Assuming a larger icon for splash
    splash_pixmap_path = get_asset_path('icons/app_icon_large.png')
    if not os.path.exists(splash_pixmap_path):
        # Fallback to a smaller icon if large one is not found
        splash_pixmap_path = get_asset_path('icons/app_icon.png')

    if os.path.exists(splash_pixmap_path):
        splash_pix = QPixmap(splash_pixmap_path)
        # Scale pixmap if it's too large for a splash screen, e.g., max 600x400
        if not splash_pix.isNull():
            splash_pix = splash_pix.scaled(
                600, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            splash = QSplashScreen(
                splash_pix, Qt.WindowType.WindowStaysOnTopHint)
            # Optional: for non-rectangular splash
            splash.setMask(splash_pix.mask())
            splash.show()
            # Simulate loading tasks - In PyQt, this is often done by initializing parts of the main window
            # For a simple delay before showing the main window:
            # QTimer.singleShot(3000, splash.close) # Close splash after 3 seconds
            # Or, more realistically, close it after the main window is ready.
        else:
            print("Warning: Splash pixmap is null.")
            splash = None  # No splash if pixmap is bad
    else:
        print(
            f"Warning: Splash screen image not found at {splash_pixmap_path}")
        splash = None  # No splash if image not found

    # Create main application window
    main_window = EdgeDetectionApp()  # This is now a QMainWindow

    # Platform-specific window adjustments (QMainWindow handles many things)
    # platform_system = detect_platform()
    # if platform_system == "windows":
    #     # main_window.setWindowOpacity(0.98) # Example, if desired
    #     pass
    # elif platform_system == "darwin":
    #     # macOS specific QWindowFlags or attributes can be set here
    #     pass

    if splash:
        # Show a message on the splash screen
        splash.showMessage("Loading UI components...", Qt.AlignmentFlag.AlignBottom |
                           Qt.AlignmentFlag.AlignHCenter, Qt.GlobalColor.white)
        QApplication.processEvents()  # Ensure splash updates

    # Simulate some loading time or actual setup
    # time.sleep(0.8) # Example delay
    if splash:
        splash.showMessage("Initializing image processors...", Qt.AlignmentFlag.AlignBottom |
                           Qt.AlignmentFlag.AlignHCenter, Qt.GlobalColor.white)
        QApplication.processEvents()
    # time.sleep(0.7)
    if splash:
        splash.showMessage("Preparing application...", Qt.AlignmentFlag.AlignBottom |
                           Qt.AlignmentFlag.AlignHCenter, Qt.GlobalColor.white)
        QApplication.processEvents()
    # time.sleep(0.5)

    main_window.show()
    if splash:
        splash.finish(main_window)  # Close splash when main window is ready

    sys.exit(app.exec())


if __name__ == "__main__":
    run_pyqt_app_with_splash()
