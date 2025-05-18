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
DIST_DIR = SCRIPT_DIR / "dist"
BUILD_DIR = SCRIPT_DIR / "build"
ASSETS_DIR = SCRIPT_DIR / "Assets"
DESKTOP_FILE = BUILD_DIR / "flower-edge-detection.desktop"
ICON_PATH = ASSETS_DIR / "app_icon.png"

def check_dependencies():
    """Check if required packages are installed"""
    # Check for PyInstaller
    try:
        import PyInstaller
        logger.info("✅ PyInstaller is installed")
    except ImportError:
        logger.error("❌ PyInstaller is not installed")
        logger.info("Installing PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        logger.info("✅ PyInstaller has been installed")

    # Check for fpm
    try:
        result = subprocess.run(["fpm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ fpm is installed: {result.stdout.strip()}")
        else:
            raise FileNotFoundError
    except (FileNotFoundError, subprocess.SubprocessError):
        logger.error("❌ fpm is not installed")
        logger.info("Please install fpm using: gem install fpm")
        logger.info("You might need to install Ruby first: sudo apt-get install ruby ruby-dev")
        sys.exit(1)

def clean_build_directories():
    """Clean up previous
 build artifacts"""
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
    main_script = SCRIPT_DIR / "edge_detection_app.py"
    
    logger.info("Building Linux executable with PyInstaller...")
    
    # Create spec file
    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['{main_script}'],
    pathex=['{SCRIPT_DIR}'],
    binaries=[],
    datas=[
        ('{ASSETS_DIR}', 'Assets'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{app_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='{ICON_PATH}'
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{app_name}'
)
"""

    spec_file = SCRIPT_DIR / f"{app_name}.spec"
    with open(spec_file, "w") as f:
        f.write(spec_content)
    
    # Run PyInstaller with spec file
    result = subprocess.run(
        ["pyinstaller", "--clean", "--noconfirm", str(spec_file)],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        logger.error(f"❌ Error building executable:\n{result.stderr}")
        return False
    
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
Comment=Analyze flowers using various edge detection algorithms
Exec=/usr/bin/flower-edge-detection
Icon=/usr/share/icons/hicolor/256x256/apps/flower-edge-detection.png
Terminal=false
Categories=Graphics;Education;Science;ImageProcessing;
Keywords=image;processing;edge;detection;flower;
"""
    
    with open(DESKTOP_FILE, "w") as f:
        f.write(desktop_content)
    
    logger.info(f"✅ Desktop file created: {DESKTOP_FILE}")
    return True

def create_deb_package():
    """Create a .deb package using fpm"""
    app_name = "flower-edge-detection"
    version = "1.0.0"
    
    # Ensure dist directory exists
    DIST_DIR.mkdir(exist_ok=True)
    
    # Package paths
    bin_path = DIST_DIR / app_name / app_name
    package_path = DIST_DIR / f"{app_name}_{version}_amd64.deb"
    
    if not bin_path.exists():
        logger.error(f"❌ Binary not found: {bin_path}")
        return False
    
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
    shutil.copy2(bin_path, bin_staging / app_name)
    shutil.copy2(DESKTOP_FILE, desktop_staging / f"{app_name}.desktop")
    shutil.copy2(ICON_PATH, icon_staging / f"{app_name}.png")
    
    # Build package with fpm
    cmd = [
        "fpm",
        "-s", "dir",       # Source type is directory
        "-t", "deb",       # Target type is deb
        "-C", str(staging_dir),  # Change to this directory before packaging
        "-n", app_name,    # Package name
        "-v", version,     # Package version
        "--description", "Application for applying edge detection algorithms to flower images",
        "--url", "https://github.com/yourusername/flower-edge-detection",
        "--maintainer", "Your Name <your.email@example.com>",
        "--vendor", "Your Organization",
        "--license", "MIT",
        "--category", "graphics",
        "--depends", "python3",
        "--depends", "python3-tk",
        "--depends", "python3-pil",
        "--depends", "python3-numpy",
        "--depends", "python3-opencv",
        "--architecture", "amd64",
        "--deb-priority", "optional",
        "-p", str(package_path),  # Output file path
    ]
    
    logger.info("Creating .deb package...")
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
    version = "1.0.0"
    
    # Ensure dist directory exists
    DIST_DIR.mkdir(exist_ok=True)
    
    # Package paths
    bin_path = DIST_DIR / app_name / app_name
    package_path = DIST_DIR / f"{app_name}-{version}.x86_64.rpm"
    
    if not bin_path.exists():
        logger.error(f"❌ Binary not found: {bin_path}")
        return False
    
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
    shutil.copy2(bin_path, bin_staging / app_name)
    shutil.copy2(DESKTOP_FILE, desktop_staging / f"{app_name}.desktop")
    shutil.copy2(ICON_PATH, icon_staging / f"{app_name}.png")
    
    # Build package with fpm
    cmd = [
        "fpm",
        "-s", "dir",       # Source type is directory
        "-t", "rpm",       # Target type is rpm
        "-C", str(staging_dir),  # Change to this directory before packaging
        "-n", app_name,    # Package name
        "-v", version,     # Package version
        "--description", "Application for applying edge detection algorithms to flower images",
        "--url", "https://github.com/yourusername/flower-edge-detection",
        "--maintainer", "Your Name <your.email@example.com>",
        "--vendor", "Your Organization",
        "--license", "MIT",
        "--category", "graphics",
        "--depends", "python3",
        "--depends", "python3-tkinter",
        "--depends", "python3-pillow",
        "--depends", "python3-numpy",
        "--depends", "opencv-python",
        "--architecture", "x86_64",
        "-p", str(package_path),  # Output file path
    ]
    
    logger.info("Creating .rpm package...")
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
            logger.info("✅ DEB package built successfully! RPM package failed.")
        elif rpm_result:
            logger.info("✅ RPM package built successfully! DEB package failed.")
        else:
            logger.error("❌ Package building failed.")
    else:
        logger.error("❌ Build process failed at executable creation stage.")
    
    logger.info("Linux build process complete!")

if __name__ == "__main__":
    main()