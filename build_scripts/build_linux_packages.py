import os
import sys
import subprocess
import shutil
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# Project paths
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent  # Added to correctly locate main.py and src
DIST_DIR = PROJECT_ROOT / "dist"  # Changed to be in project root
BUILD_DIR = PROJECT_ROOT / "build"  # Changed to be in project root
ASSETS_DIR = PROJECT_ROOT / "assets"  # Changed to correctly locate assets
DESKTOP_FILE = BUILD_DIR / "flower-edge-detection.desktop"
# Try to find a suitable icon, prefer .png
ICON_CANDIDATES = [
    ASSETS_DIR / "icons/app_icon.png",
    ASSETS_DIR / "icons/app_icon_small.png",
    ASSETS_DIR / "icons/app_icon_tiny.png"
]
ICON_PATH = next((p for p in ICON_CANDIDATES if p.exists()),
                 ASSETS_DIR / "icons/app_icon.png")  # Default if none found

APP_NAME = "FlowerEdgeDetection"
# Name of the executable created by PyInstaller
APP_EXECUTABLE_NAME = "FlowerEdgeDetection"
# Get version from environment variable or use a default
APP_VERSION = os.environ.get("APP_BUILD_VERSION", "0.1.0")
APP_DESCRIPTION = "An application for detecting edges in flower images using various algorithms."


def get_architecture():
    """Determine the system architecture for RPM packaging."""
    # For simplicity and consistency with current fpm command in create_rpm_package
    # which hardcodes x86_64. A more robust check could be platform.machine().
    # Common values: x86_64, aarch64, etc.
    return "x86_64"


def check_dependencies():
    """Check if required packages are installed"""
    # Check for PyInstaller
    try:
        import PyInstaller
        logger.info("✅ PyInstaller is installed")
    except ImportError:
        logger.error("❌ PyInstaller is not installed")
        logger.info("Installing PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip",
                           "install", "pyinstaller"], check=True)
            logger.info("✅ PyInstaller has been installed")
        except subprocess.SubprocessError:
            logger.error(
                "❌ Could not install PyInstaller. Please install it manually.")
            sys.exit(1)

    # Check for fpm
    try:
        result = subprocess.run(["fpm", "--version"],
                                capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ fpm is installed: {result.stdout.strip()}")
        else:
            raise FileNotFoundError
    except (FileNotFoundError, subprocess.SubprocessError):
        logger.error("❌ fpm is not installed")
        logger.info("Please install fpm using: gem install fpm")
        logger.info(
            "You might need to install Ruby first: sudo apt-get install ruby ruby-dev")
        sys.exit(1)


def clean_build_directories():
    """Clean up previous build artifacts"""
    for directory in [DIST_DIR, BUILD_DIR]:
        if directory.exists() and directory.is_dir():
            logger.info(f"Cleaning {directory}...")
            shutil.rmtree(directory)

        # Recreate directories
        directory.mkdir(exist_ok=True)
        logger.info(f"✅ Created {directory}")


def build_executable():
    """Build the executable using PyInstaller"""
    app_name = "flower-edge-detection"
    # Main script is now main.py in the project root
    main_script_path = PROJECT_ROOT / "main.py"

    logger.info("Building Linux executable with PyInstaller...")

    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        str(main_script_path),
        "--name", app_name,
        "--onefile",  # Creates a single executable file
        "--windowed",  # Use for GUI applications, no console
        # Add assets: PyInstaller will copy these into the _MEIPASS folder at runtime
        # The path in the code should be relative to sys._MEIPASS
        f"--add-data", f"{ASSETS_DIR}{os.pathsep}assets",
        # Add other necessary PyQt6 data if needed (e.g., plugins)
        # Example: --add-data \"path/to/PyQt6/Qt/plugins/platforms{os.pathsep}PyQt6/Qt/plugins/platforms\"
        # This often requires knowing the PyQt6 installation path.
        # A more robust way is to use PyInstaller hooks for PyQt6 if available or create custom ones.
        "--hidden-import", "PyQt6.sip",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtWidgets",
        # Add any other specific hidden imports your app might need
        "--icon", str(ICON_PATH),
        "--distpath", str(DIST_DIR),
        # Intermediate files
        "--workpath", str(BUILD_DIR / "pyinstaller_build"),
        "--specpath", str(BUILD_DIR),  # Where to put the .spec file
        "--clean",  # Clean PyInstaller cache and remove temporary files before building
        "--noconfirm"  # Overwrite output directory without asking
    ]

    logger.info(
        f"Running PyInstaller with command: {' '.join(pyinstaller_cmd)}")

    result = subprocess.run(pyinstaller_cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(
            f"❌ Error building executable with PyInstaller:\\n--- STDOUT ---\\n{result.stdout}\\n--- STDERR ---\\n{result.stderr}")
        return False

    logger.info(f"✅ PyInstaller STDOUT:\\n{result.stdout}")
    if result.stderr:
        logger.warning(f"⚠️ PyInstaller STDERR:\\n{result.stderr}")

    logger.info("✅ Executable built successfully!")
    return True


def create_desktop_file():
    """Create a .desktop file for Linux integration"""
    BUILD_DIR.mkdir(exist_ok=True)

    desktop_content = """
[Desktop Entry]
Version=1.0
Type=Application
Name=Flower Edge Detection
Comment=Analyze flowers using various edge detection algorithms with PyQt6
Exec=/usr/bin/flower-edge-detection
Icon=/usr/share/icons/hicolor/256x256/apps/flower-edge-detection.png
Terminal=false
Categories=Graphics;Education;Science;ImageProcessing;Qt;
Keywords=image;processing;edge;detection;flower;pyqt;
"""

    with open(DESKTOP_FILE, "w") as f:
        f.write(desktop_content)

    logger.info(f"✅ Desktop file created: {DESKTOP_FILE}")
    return True


def create_deb_package():
    """Create a .deb package using fpm"""
    app_name = "flower-edge-detection"
    version = APP_VERSION  # Use the dynamic APP_VERSION

    # Ensure dist directory exists
    DIST_DIR.mkdir(exist_ok=True)

    # Path to the PyInstaller-built executable
    # PyInstaller puts it directly in distpath
    executable_path = DIST_DIR / app_name

    if not executable_path.exists():
        logger.error(
            f"❌ Executable not found at: {executable_path}. Run PyInstaller build first.")
        return False

    package_path = DIST_DIR / f"{app_name}_{version}_amd64.deb"

    # Prepare directories
    staging_dir = BUILD_DIR / "deb_staging"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)

    bin_staging = staging_dir / "usr/bin"
    desktop_staging = staging_dir / "usr/share/applications"
    icon_staging = staging_dir / "usr/share/icons/hicolor/256x256/apps"

    for directory in [bin_staging, desktop_staging, icon_staging]:
        directory.mkdir(parents=True, exist_ok=True)

    # Copy files to staging
    # Use the PyInstaller output
    shutil.copy2(executable_path, bin_staging / app_name)
    shutil.copy2(DESKTOP_FILE, desktop_staging / f"{app_name}.desktop")
    if ICON_PATH.exists():
        shutil.copy2(ICON_PATH, icon_staging / f"{app_name}.png")
    else:
        logger.warning(
            f"Icon not found at {ICON_PATH}, package will not have an icon.")

    # Build package with fpm
    cmd = [
        "fpm",
        "-s", "dir",       # Source type is directory
        "-t", "deb",       # Target type is deb
        "-C", str(staging_dir),  # Change to this directory before packaging
        "-n", app_name,    # Package name
        "-v", version,     # Package version
        "--description", "Application for applying edge detection algorithms to flower images (PyQt6 version)",
        "--url", "https://github.com/yourusername/flower-edge-detection",  # Update this
        "--maintainer", "Your Name <your.email@example.com>",  # Update this
        "--vendor", "Your Organization",  # Update this
        "--license", "MIT",  # Or your chosen license
        "--category", "graphics",
        # Dependencies for a PyQt6 app are usually bundled by PyInstaller.
        # System-level dependencies might still be needed for the OS itself,
        # but the Python ones (PyQt6, numpy, opencv) should be in the executable.
        # Common system libs that might be needed by Qt:
        "--depends", "libc6 >= 2.17",
        "--depends", "libxext6",
        "--depends", "libxrender1",
        "--depends", "libxinerama1",
        "--depends", "libxrandr2",
        "--depends", "libxfixes3",
        "--depends", "libxcursor1",
        "--depends", "libgl1",  # Or libgl1-mesa-glx
        "--depends", "libfontconfig1",
        "--architecture", "amd64",
        "--deb-priority", "optional",
        "-p", str(package_path),  # Output file path
        # Add post-install/pre-remove scripts if needed
    ]

    logger.info(f"Creating .deb package with command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        logger.info(f"✅ .deb package created: {package_path}")
        return True
    else:
        logger.error(f"❌ Error creating .deb package:\n{result.stderr}")
        return False


def create_rpm_package():
    """Create a .rpm package using fpm"""
    app_name = "flower-edge-detection"
    version = APP_VERSION  # Use the dynamic APP_VERSION
    arch = get_architecture()

    DIST_DIR.mkdir(exist_ok=True)
    executable_path = DIST_DIR / app_name

    if not executable_path.exists():
        logger.error(
            f"❌ Executable not found at: {executable_path}. Run PyInstaller build first.")
        return False

    # RPM naming convention
    package_path = DIST_DIR / f"{app_name}-{version}-1.x86_64.rpm"

    # Prepare directories
    staging_dir = BUILD_DIR / "rpm_staging"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)

    bin_staging = staging_dir / "usr/bin"
    desktop_staging = staging_dir / "usr/share/applications"
    icon_staging = staging_dir / "usr/share/icons/hicolor/256x256/apps"

    for directory in [bin_staging, desktop_staging, icon_staging]:
        directory.mkdir(parents=True, exist_ok=True)

    # Copy files to staging
    shutil.copy2(executable_path, bin_staging / app_name)
    shutil.copy2(DESKTOP_FILE, desktop_staging / f"{app_name}.desktop")
    if ICON_PATH.exists():
        shutil.copy2(ICON_PATH, icon_staging / f"{app_name}.png")
    else:
        logger.warning(
            f"Icon not found at {ICON_PATH}, package will not have an icon.")

    # Build package with fpm
    cmd = [
        "fpm",
        "-s", "dir",
        "-t", "rpm",
        "-C", str(staging_dir),
        "-n", app_name,
        "-v", version,
        "--iteration", "1",  # RPM iteration
        "--description", "Application for applying edge detection algorithms to flower images (PyQt6 version)",
        "--url", "https://github.com/yourusername/flower-edge-detection",  # Update this
        "--maintainer", "Your Name <your.email@example.com>",  # Update this
        "--vendor", "Your Organization",  # Update this
        "--license", "MIT",  # Or your chosen license
        "--category", "Applications/Graphics",  # RPM category
        # Similar to .deb, Python dependencies should be bundled.
        # System dependencies for Qt:
        "--depends", "glibc >= 2.17",
        "--depends", "libXext",
        "--depends", "libXrender",
        "--depends", "libXinerama",
        "--depends", "libXrandr",
        "--depends", "libXfixes",
        "--depends", "libXcursor",
        "--depends", "mesa-libGL",  # Or libGL
        "--depends", "fontconfig",
        "--architecture", "x86_64",
        "-p", str(package_path),
    ]

    logger.info(f"Creating .rpm package with command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        logger.info(f"✅ .rpm package created: {package_path}")
        return True
    else:
        logger.error(f"❌ Error creating .rpm package:\n{result.stderr}")
        return False


def main():
    """Main build process"""
    logger.info("Starting Linux package build process...")

    # Check for required tools
    check_dependencies()

    # Clean previous builds
    clean_build_directories()

    # Build executable
    if build_executable():
        # Create desktop file for Linux integration
        create_desktop_file()

        # Create packages
        deb_result = create_deb_package()
        rpm_result = create_rpm_package()

        if deb_result and rpm_result:
            logger.info("✅ All packages built successfully!")
        elif deb_result:
            logger.info(
                "✅ DEB package built successfully! RPM package failed.")
        elif rpm_result:
            logger.info(
                "✅ RPM package built successfully! DEB package failed.")
        else:
            logger.error("❌ Package building failed.")
    else:
        logger.error("❌ Build process failed at executable creation stage.")

    logger.info("Linux build process complete!")


if __name__ == "__main__":
    main()
