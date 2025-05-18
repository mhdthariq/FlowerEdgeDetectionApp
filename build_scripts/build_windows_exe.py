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
ICON_PATH = ASSETS_DIR / "app_icon.ico"

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

def convert_png_to_ico():
    """Convert PNG icon to ICO format for Windows"""
    if not ICON_PATH.exists():
        try:
            from PIL import Image
            png_path = ASSETS_DIR / "app_icon.png"
            if png_path.exists():
                logger.info(f"Converting {png_path} to ICO format...")
                img = Image.open(png_path)
                img.save(ICON_PATH)
                logger.info(f"✅ Icon converted and saved to {ICON_PATH}")
            else:
                logger.warning(f"⚠️ Icon file not found: {png_path}")
                return False
        except ImportError:
            logger.warning("⚠️ Pillow not installed. Cannot convert PNG to ICO.")
            return False
        except Exception as e:
            logger.error(f"❌ Error converting icon: {e}")
            return False
    else:
        logger.info(f"✅ Icon file already exists: {ICON_PATH}")
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
    app_name = "FlowerEdgeDetection"
    main_script = SCRIPT_DIR / "edge_detection_app.py"
    
    logger.info("Building Windows executable with PyInstaller...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name", app_name,
        "--windowed",  # No console window
        "--onefile",   # Package everything into a single executable
        "--clean",     # Clean PyInstaller cache
        "--noconfirm",  # Replace output directory without confirmation
        "--add-data", f"{ASSETS_DIR};Assets",  # Include asset files
    ]
    
    # Add icon if available
    if ICON_PATH.exists():
        cmd.extend(["--icon", str(ICON_PATH)])
    else:
        logger.warning("⚠️ No icon file found. Building without custom icon.")
    
    # Add main script
    cmd.append(str(main_script))
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("✅ Executable built successfully!")
        exe_path = DIST_DIR / f"{app_name}.exe"
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
            
        logger.info(f"Creating Windows installer with NSIS...")
        
        # Create NSIS script
        nsis_script = SCRIPT_DIR / "installer.nsi"
        app_name = "FlowerEdgeDetection"
        exe_file = f"{app_name}.exe"
        
        with open(nsis_script, "w") as f:
            f.write(f"""
; Flower Edge Detection Installer Script
!include "MUI2.nsh"

; General
Name "{app_name}"
OutFile "dist\\{app_name}_Setup.exe"
InstallDir "$PROGRAMFILES\\{app_name}"
InstallDirRegKey HKCU "Software\\{app_name}" ""

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "{ICON_PATH}"

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
  File "dist\\{exe_file}"
  File /r "Assets\\*.*"
  
  ; Create Start Menu shortcut
  CreateDirectory "$SMPROGRAMS\\{app_name}"
  CreateShortCut "$SMPROGRAMS\\{app_name}\\{app_name}.lnk" "$INSTDIR\\{exe_file}" "" "$INSTDIR\\{exe_file}" 0
  
  ; Create uninstaller
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  
  ; Write registry keys for uninstaller
  WriteRegStr HKCU "Software\\{app_name}" "" $INSTDIR
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" "DisplayName" "{app_name}"
  WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}" "UninstallString" "$INSTDIR\\Uninstall.exe"
SectionEnd

; Uninstaller
Section "Uninstall"
  Delete "$INSTDIR\\{exe_file}"
  Delete "$INSTDIR\\Uninstall.exe"
  RMDir /r "$INSTDIR"
  
  ; Remove Start Menu shortcut
  Delete "$SMPROGRAMS\\{app_name}\\{app_name}.lnk"
  RMDir "$SMPROGRAMS\\{app_name}"
  
  ; Remove registry keys
  DeleteRegKey HKCU "Software\\{app_name}"
  DeleteRegKey HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{app_name}"
SectionEnd
            """)
            
        # Run NSIS
        result = subprocess.run(
            ["makensis", str(nsis_script)],
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            installer_path = DIST_DIR / f"{app_name}_Setup.exe"
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