import os
import sys
import platform
import subprocess
import logging
import shutil
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
DIST_DIR = SCRIPT_DIR / "dist"
BUILD_DIR = SCRIPT_DIR / "build"
ASSETS_DIR = SCRIPT_DIR / "Assets"

# Build scripts
WINDOWS_SCRIPT = SCRIPT_DIR / "build_windows_exe.py"
LINUX_SCRIPT = SCRIPT_DIR / "build_linux_packages.py"
MACOS_SCRIPT = SCRIPT_DIR / "build_macos_app.py"

def detect_platform():
    """Detect the current operating system"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "linux":
        return "linux"
    elif system == "darwin":
        return "macos"
    else:
        return "unknown"

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        logger.error(f"❌ Python version {version.major}.{version.minor}.{version.micro} is not supported.")
        logger.error("Please use Python 3.7 or higher.")
        return False
    logger.info(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check and install required packages"""
    required_packages = ['pyinstaller', 'pillow', 'opencv-python', 'numpy', 'ttkbootstrap']
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} is installed")
        except ImportError:
            logger.warning(f"⚠️ {package} is not installed")
            try:
                logger.info(f"Installing {package}...")
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                logger.info(f"✅ {package} has been installed")
            except subprocess.SubprocessError:
                logger.error(f"❌ Could not install {package}")
                return False
    return True

def clean_build_directories():
    """Clean up previous build artifacts"""
    for directory in [DIST_DIR, BUILD_DIR]:
        if directory.exists():
            logger.info(f"Cleaning {directory}...")
            shutil.rmtree(directory)
        directory.mkdir(exist_ok=True)
        logger.info(f"✅ Created {directory}")

def build_windows():
    """Build Windows executable and installer"""
    if not WINDOWS_SCRIPT.exists():
        logger.error(f"❌ Windows build script not found: {WINDOWS_SCRIPT}")
        return False
        
    logger.info("🔧 Building Windows application...")
    return run_script(WINDOWS_SCRIPT)

def build_linux():
    """Build Linux packages (DEB and RPM)"""
    if not LINUX_SCRIPT.exists():
        logger.error(f"❌ Linux build script not found: {LINUX_SCRIPT}")
        return False
        
    logger.info("🔧 Building Linux packages...")
    return run_script(LINUX_SCRIPT)

def build_macos():
    """Build macOS app bundle and DMG"""
    if not MACOS_SCRIPT.exists():
        logger.error(f"❌ macOS build script not found: {MACOS_SCRIPT}")
        return False
        
    logger.info("🔧 Building macOS application...")
    return run_script(MACOS_SCRIPT)

def run_script(script_path):
    """Execute a build script and return result"""
    try:
        subprocess.run([sys.executable, str(script_path)], check=True)
        return True
    except subprocess.SubprocessError as e:
        logger.error(f"❌ Build script failed: {e}")
        return False

def main():
    """Main build process"""
    logger.info("=" * 60)
    logger.info("🚀 Flower Edge Detection - Application Builder")
    logger.info("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Detect platform
    platform_name = detect_platform()
    logger.info(f"🖥️ Detected platform: {platform_name}")
    
    # Check dependencies
    if not check_dependencies():
        logger.error("❌ Dependency check failed. Please install required packages.")
        return
    
    # Clean build directories
    clean_build_directories()
    
    # Build according to platform
    if platform_name == "windows":
        success = build_windows()
    elif platform_name == "linux":
        success = build_linux()
    elif platform_name == "macos":
        success = build_macos()
    else:
        logger.error("❌ Unsupported platform. Cannot build application.")
        return
    
    if success:
        logger.info("=" * 60)
        logger.info("✅ Build completed successfully!")
        logger.info(f"📦 Output files are in: {DIST_DIR}")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("❌ Build failed. See log above for details.")
        logger.error("=" * 60)

if __name__ == "__main__":
    main()