import os
import sys
import subprocess
import shutil
import logging
import plistlib
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
ICON_PATH = ASSETS_DIR / "app_icon.png"
ICNS_PATH = BUILD_DIR / "app_icon.icns"

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['pyinstaller']
    
    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} is installed")
        except ImportError:
            logger.error(f"❌ {package} is not installed")
            logger.info(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package])
            logger.info(f"✅ {package} has been installed")

def convert_png_to_icns():
    """Convert PNG icon to ICNS format for macOS"""
    if not ICNS_PATH.exists():
        try:
            # First check if iconutil is available (macOS only)
            subprocess.run(["which", "iconutil"], check=True, capture_output=True)
            logger.info("✅ iconutil is available")
            
            # Create temporary iconset directory
            iconset_path = BUILD_DIR / "app_icon.iconset"
            if iconset_path.exists():
                shutil.rmtree(iconset_path)
            iconset_path.mkdir(parents=True, exist_ok=True)
            
            # Check if source PNG exists
            if not ICON_PATH.exists():
                logger.error(f"❌ Source icon not found: {ICON_PATH}")
                return False
                
            # Need to create multiple sizes for iconset
            from PIL import Image
            img = Image.open(ICON_PATH)
            
            # Create various sizes required for .icns
            icon_sizes = [16, 32, 64, 128, 256, 512, 1024]
            for size in icon_sizes:
                # Regular resolution
                resized = img.resize((size, size), Image.LANCZOS)
                resized.save(iconset_path / f"icon_{size}x{size}.png")
                
                # Retina resolution (2x)
                if size * 2 <= 1024:  # Don't exceed 1024
                    retina_size = size * 2
                    retina_resized = img.resize((retina_size, retina_size), Image.LANCZOS)
                    retina_resized.save(iconset_path / f"icon_{size}x{size}@2x.png")
            
            # Convert iconset to icns using iconutil
            subprocess.run(["iconutil", "-c", "icns", str(iconset_path)], check=True)
            
            # Clean up iconset
            shutil.rmtree(iconset_path)
            
            logger.info(f"✅ ICNS icon created: {ICNS_PATH}")
            return True
            
        except subprocess.CalledProcessError:
            logger.warning("⚠️ iconutil not available. This script should be run on macOS.")
            return False
        except ImportError:
            logger.warning("⚠️ PIL not installed. Cannot convert PNG to ICNS.")
            return False
        except Exception as e:
            logger.error(f"❌ Error converting icon: {e}")
            return False
    else:
        logger.info(f"✅ ICNS icon already exists: {ICNS_PATH}")
        return True

def clean_build_directories():
    """Clean up previous build artifacts"""
    for directory in [DIST_DIR, BUILD_DIR]:
        if directory.exists():
            logger.info(f"Cleaning {directory}...")
            shutil.rmtree(directory)
        directory.mkdir(exist_ok=True)
        logger.info(f"✅ Created {directory}")

def create_info_plist():
    """Create Info.plist file for macOS app bundle"""
    plist_path = BUILD_DIR / "Info.plist"
    
    info_plist = {
        'CFBundleDevelopmentRegion': 'English',
        'CFBundleDisplayName': 'Flower Edge Detection',
        'CFBundleExecutable': 'flower-edge-detection',
        'CFBundleIconFile': 'app_icon.icns',
        'CFBundleIdentifier': 'com.example.floweredgedetection',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleName': 'FlowerEdgeDetection',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'LSMinimumSystemVersion': '10.13.0',
        'NSHighResolutionCapable': True,
        'NSHumanReadableCopyright': 'Copyright © 2023, Your Name',
        'NSPrincipalClass': 'NSApplication',
        'NSRequiresAquaSystemAppearance': False,
    }
    
    with open(plist_path, 'wb') as fp:
        plistlib.dump(info_plist, fp)
    
    logger.info(f"✅ Info.plist created at {plist_path}")
    return plist_path

def build_macos_app():
    """Build the macOS .app bundle using PyInstaller"""
    app_name = "FlowerEdgeDetection"
    main_script = SCRIPT_DIR / "edge_detection_app.py"
    
    logger.info("Building macOS application bundle with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", "flower-edge-detection",
        "--windowed",  # No console window
        "--noconfirm",  # Replace output directory without confirmation
        "--add-data", f"{ASSETS_DIR}:Assets",  # Include asset files
        "--osx-bundle-identifier", "com.example.floweredgedetection",
        "--target-architecture", "universal2",  # For both Intel and Apple Silicon
    ]
    
    # Add icon if available
    if ICNS_PATH.exists():
        cmd.extend(["--icon", str(ICNS_PATH)])
    else:
        logger.warning("⚠️ No ICNS icon file found. Building without custom icon.")
    
    # Add main script
    cmd.append(str(main_script))
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("✅ macOS app bundle built successfully!")
        
        # Rename and move the app bundle
        built_app = DIST_DIR / "flower-edge-detection.app"
        final_app = DIST_DIR / f"{app_name}.app"
        
        if built_app.exists():
            if final_app.exists():
                shutil.rmtree(final_app)
            shutil.move(built_app, final_app)
            
        logger.info(f"📦 App bundle location: {final_app}")
        return final_app
    else:
        logger.error(f"❌ Error building app bundle:\n{result.stderr}")
        return None

def create_dmg_installer(app_path):
    """Create a DMG installer for macOS app"""
    if app_path is None or not app_path.exists():
        logger.error("❌ App bundle not found. Cannot create DMG.")
        return False
        
    app_name = app_path.stem
    dmg_path = DIST_DIR / f"{app_name}.dmg"
    
    try:
        # First check if create-dmg or hdiutil is available
        try:
            # Try create-dmg first (better looking DMG)
            subprocess.run(["which", "create-dmg"], check=True, capture_output=True)
            logger.info("✅ create-dmg is available, using it for DMG creation")
            
            cmd = [
                "create-dmg",
                "--volname", app_name,
                "--window-pos", "200", "100",
                "--window-size", "800", "500",
                "--icon-size", "100",
                "--icon", app_name, "200", "200",
                "--app-drop-link", "600", "200",
                "--no-internet-enable",
                str(dmg_path),
                str(app_path)
            ]
            
        except subprocess.CalledProcessError:
            # Fall back to hdiutil
            logger.info("⚠️ create-dmg not found, falling back to hdiutil")
            
            temp_dmg = DIST_DIR / "temp.dmg"
            if temp_dmg.exists():
                os.remove(temp_dmg)
                
            cmd = [
                "hdiutil", "create",
                "-volname", app_name,
                "-srcfolder", str(app_path),
                "-ov", "-format", "UDBZ",
                str(dmg_path)
            ]
        
        # Run the chosen command
        logger.info(f"Creating DMG installer for {app_name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"✅ DMG installer created: {dmg_path}")
            return True
        else:
            logger.error(f"❌ Error creating DMG:\n{result.stderr}")
            return False
            
    except subprocess.CalledProcessError:
        logger.warning("⚠️ Neither create-dmg nor hdiutil are available. This script should be run on macOS.")
        return False
    except Exception as e:
        logger.error(f"❌ Error creating DMG: {e}")
        return False

def main():
    """Main build process"""
    logger.info("Starting macOS build process...")
    
    # Check for required packages
    check_dependencies()
    
    # Clean previous builds
    clean_build_directories()
    
    # Prepare icon
    icon_result = convert_png_to_icns()
    
    # Create Info.plist
    create_info_plist()
    
    # Build macOS app bundle
    app_path = build_macos_app()
    
    # Create DMG installer if app was built successfully
    if app_path:
        create_dmg_installer(app_path)
    
    logger.info("macOS build process complete!")

if __name__ == "__main__":
    main()