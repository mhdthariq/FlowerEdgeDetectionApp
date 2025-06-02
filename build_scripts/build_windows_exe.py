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
PROJECT_ROOT = SCRIPT_DIR.parent  # New: Define project root
DIST_DIR = PROJECT_ROOT / "dist"  # Changed: dist at project root
BUILD_DIR = PROJECT_ROOT / "build"  # Changed: build at project root
ASSETS_DIR = PROJECT_ROOT / "assets"  # Changed: assets at project root
ICON_PNG_PATH = ASSETS_DIR / "icons" / "app_icon.png"  # Changed
ICON_ICO_PATH = ASSETS_DIR / "icons" / "app_icon.ico"  # Changed

# Application specific
APP_NAME = "FlowerEdgeDetection"
MAIN_SCRIPT_NAME = "main.py"  # Assuming main.py is at the project root
MAIN_SCRIPT_PATH = PROJECT_ROOT / MAIN_SCRIPT_NAME

# Versioning - get from environment variable or default
APP_VERSION = os.environ.get("APP_BUILD_VERSION", "0.1.0")


def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['pyinstaller', 'Pillow', 'PyQt6']  # Added PyQt6

    for package in required_packages:
        try:
            __import__(package)
            logger.info(f"✅ {package} is installed")
        except ImportError:
            logger.error(f"❌ {package} is not installed")
            logger.info(f"Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package])
            logger.info(f"✅ {package} has been installed")


def convert_png_to_ico():
    """Convert PNG icon to ICO format for Windows"""
    if not ICON_ICO_PATH.exists():  # Changed to ICON_ICO_PATH
        try:
            from PIL import Image
            if ICON_PNG_PATH.exists():  # Changed to ICON_PNG_PATH
                logger.info(f"Converting {ICON_PNG_PATH} to ICO format...")
                img = Image.open(ICON_PNG_PATH)  # Changed to ICON_PNG_PATH
                # Ensure the icons directory exists
                (ASSETS_DIR / "icons").mkdir(parents=True, exist_ok=True)
                img.save(ICON_ICO_PATH)  # Changed to ICON_ICO_PATH
                logger.info(f"✅ Icon converted and saved to {ICON_ICO_PATH}")
            else:
                logger.warning(f"⚠️ Icon PNG file not found: {ICON_PNG_PATH}")
                return False
        except ImportError:
            logger.warning(
                "⚠️ Pillow not installed. Cannot convert PNG to ICO.")
            return False
        except Exception as e:
            logger.error(f"❌ Error converting icon: {e}")
            return False
    else:
        logger.info(f"✅ Icon file already exists: {ICON_ICO_PATH}")
    return True


def clean_build_directories():
    """Clean up previous build artifacts"""
    for directory in [DIST_DIR, BUILD_DIR]:
        if directory.exists():
            logger.info(f"Cleaning {directory}...")
            shutil.rmtree(directory)
            logger.info(f"✅ {directory} removed")


def build_executable():
    """Build the executable using PyInstaller"""
    # app_name = "FlowerEdgeDetection" # Defined globally
    # main_script = SCRIPT_DIR / "edge_detection_app.py" # Now using MAIN_SCRIPT_PATH

    logger.info(
        f"Building Windows executable for {APP_NAME} version {APP_VERSION}...")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", f"{APP_NAME}-{APP_VERSION}",  # Added version to name
        "--windowed",  # No console window
        "--onefile",   # Package everything into a single executable
        "--clean",     # Clean PyInstaller cache
        "--noconfirm",  # Replace output directory without confirmation
        # Add assets: source_path_in_project;destination_in_bundle
        "--add-data", f"{ASSETS_DIR}{os.pathsep}assets",
        # Add hooks for PyQt6 if needed, e.g., for platform plugins
        "--collect-submodules", "PyQt6.QtWebEngineCore",  # Example, adjust as needed
        "--hidden-import", "PyQt6.sip",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        # Specify output directories relative to project root
        "--distpath", str(DIST_DIR),
        "--workpath", str(BUILD_DIR),
    ]

    # Add icon if available
    if ICON_ICO_PATH.exists():  # Changed to ICON_ICO_PATH
        cmd.extend(["--icon", str(ICON_ICO_PATH)])  # Changed to ICON_ICO_PATH
    else:
        logger.warning(
            f"⚠️ No icon file found at {ICON_ICO_PATH}. Building without custom icon.")

    # Add main script
    cmd.append(str(MAIN_SCRIPT_PATH))  # Changed to MAIN_SCRIPT_PATH

    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        logger.info("✅ Executable built successfully!")
        # Path will be in DIST_DIR / (APP_NAME + "-" + APP_VERSION) / (APP_NAME + "-" + APP_VERSION + ".exe")
        # if not using --specpath for a custom spec file that changes output structure.
        # For --onefile, it's simpler:
        exe_path = DIST_DIR / f"{APP_NAME}-{APP_VERSION}.exe"
        logger.info(f"📦 Executable location: {exe_path}")
        return True
    else:
        logger.error(f"❌ Error building executable:\n{result.stderr}")
        return False


def create_windows_installer():
    """Create Windows installer using NSIS (if available)"""
    try:
        # Check if NSIS is installed
        nsis_check = subprocess.run(
            ["makensis", "/VERSION"],
            capture_output=True,
            text=True
        )

        if nsis_check.returncode != 0:
            logger.warning("⚠️ NSIS not found. Skipping installer creation.")
            return False

        logger.info(
            f"Creating Windows installer with NSIS for version {APP_VERSION}...")

        # Create NSIS script
        nsis_script_path = BUILD_DIR / "installer.nsi"  # Changed: place nsi in build dir
        # app_name = "FlowerEdgeDetection" # Defined globally
        exe_name_with_version = f"{APP_NAME}-{APP_VERSION}.exe"
        installer_name = f"{APP_NAME}-{APP_VERSION}_Setup.exe"

        with open(nsis_script_path, "w") as f:  # Changed path
            f.write(f'''\
; {APP_NAME} Installer Script
!include "MUI2.nsh"

; General
Name "{APP_NAME}"
OutFile "{DIST_DIR / installer_name}" ; Changed: Output to dist dir
InstallDir "$PROGRAMFILES\\\\{APP_NAME}"
InstallDirRegKey HKCU "Software\\\\{APP_NAME}" ""

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "{ICON_ICO_PATH}" ; Changed: Use ICON_ICO_PATH

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer
Section "Install"
  SetOutPath "$INSTDIR"
  File "{DIST_DIR / exe_name_with_version}" ; Changed: Path to versioned exe
  
  ; Include assets - copy the whole assets folder
  SetOutPath "$INSTDIR\\\\assets"
  File /r "{ASSETS_DIR}\\\\*.*"

  SetOutPath "$INSTDIR" ; Reset OutPath
  
  ; Create Start Menu shortcut
  CreateDirectory "$SMPROGRAMS\\\\{APP_NAME}"
  CreateShortCut "$SMPROGRAMS\\\\{APP_NAME}\\\\{APP_NAME}.lnk" "$INSTDIR\\\\{exe_name_with_version}" "" "$INSTDIR\\\\{exe_name_with_version}" 0 Icon "$INSTDIR\\\\{exe_name_with_version}" 0
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  
  ; Write registry keys for uninstaller
  WriteRegStr HKCU "Software\\{APP_NAME}" "" $INSTDIR
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" "DisplayName" "{APP_NAME}"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}" "UninstallString" "$INSTDIR\\Uninstall.exe"
SectionEnd

; Uninstaller
Section "Uninstall"
  Delete "$INSTDIR\\\\{exe_name_with_version}" ; Changed
  Delete "$INSTDIR\\\\Uninstall.exe"
  RMDir /r "$INSTDIR\\\\assets" ; Remove assets folder
  RMDir /r "$INSTDIR"
  
  ; Remove Start Menu shortcut
  Delete "$SMPROGRAMS\\{APP_NAME}\\{APP_NAME}.lnk"
  RMDir "$SMPROGRAMS\\{APP_NAME}"
  
  ; Remove registry keys
  DeleteRegKey HKCU "Software\\{APP_NAME}"
  DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{APP_NAME}"
SectionEnd
            ''')  # Important: use f''' for multiline string

        # Run NSIS
        result = subprocess.run(
            ["makensis", str(nsis_script_path)],  # Changed path
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT  # Run makensis from project root for relative paths in NSI
        )

        if result.returncode == 0:
            installer_path = DIST_DIR / installer_name  # Changed
            logger.info(f"✅ Windows installer created: {installer_path}")
            return True
        else:
            logger.error(f"❌ Error creating installer:\n{result.stderr}")
            return False

    except Exception as e:
        logger.error(f"❌ Error creating installer: {e}")
        return False


def main():
    """Main build process"""
    logger.info("Starting Windows build process...")

    # Check for required packages
    check_dependencies()

    # Prepare icon
    convert_png_to_ico()

    # Clean previous builds
    clean_build_directories()

    # Build executable
    if build_executable():
        # Try to create installer if executable was built successfully
        create_windows_installer()

    logger.info("Windows build process complete!")


if __name__ == "__main__":
    main()
