# Flower Edge Detection App - Distribution Guide

This guide explains how to build and distribute the application for Windows, Linux, and macOS platforms.

## Prerequisites

Before building the application, ensure the following are installed:

- Python 3.7 or higher
- pip (Python package installer)
- Required system packages depending on platform (see platform-specific sections)

## Quick Start

To build the application for your current platform:

```bash
python build_app.py
```

The universal build script will detect your platform and use the appropriate build method. Output files will be placed in the `dist/` directory.

## Windows (.exe)

### Building on Windows

1. Install required tools:
   ```
   pip install pyinstaller pillow numpy opencv-python ttkbootstrap
   ```

2. Run the Windows build script:
   ```
   python build_windows_exe.py
   ```

3. Output:
   - Standalone executable: `dist/FlowerEdgeDetection.exe`
   - Installer (if NSIS is installed): `dist/FlowerEdgeDetection_Setup.exe`

### NSIS Installer (Optional)

To create a Windows installer, install NSIS (Nullsoft Scriptable Install System):
1. Download and install NSIS from [nsis.sourceforge.io](https://nsis.sourceforge.io/Download)
2. Ensure `makensis` is in your PATH
3. Run the build script again

### Distribution

- Share the standalone `.exe` file for simple distribution
- Share the installer `.exe` for a professional installation experience

## Linux (.deb, .rpm)

### Building on Linux

1. Install system requirements:
   ```bash
   # Debian/Ubuntu
   sudo apt-get install python3-dev python3-tk ruby ruby-dev build-essential
   sudo gem install fpm
   
   # Fedora/RHEL
   sudo dnf install python3-devel python3-tkinter ruby ruby-devel gcc make rpm-build
   sudo gem install fpm
   ```

2. Install Python requirements:
   ```bash
   pip install pyinstaller pillow numpy opencv-python ttkbootstrap
   ```

3. Run the Linux build script:
   ```bash
   python build_linux_packages.py
   ```

4. Output:
   - DEB package: `dist/flower-edge-detection_1.0.0_amd64.deb`
   - RPM package: `dist/flower-edge-detection-1.0.0.x86_64.rpm`

### Distribution

For Debian-based distributions (Ubuntu, Debian, etc.):
```bash
sudo dpkg -i dist/flower-edge-detection_1.0.0_amd64.deb
sudo apt-get install -f  # To resolve any dependencies
```

For RPM-based distributions (Fedora, RHEL, CentOS):
```bash
sudo rpm -i dist/flower-edge-detection-1.0.0.x86_64.rpm
```

## macOS (.app, .dmg)

### Building on macOS

1. Install requirements:
   ```bash
   pip install pyinstaller pillow numpy opencv-python ttkbootstrap
   ```

2. For better DMG creation (optional):
   ```bash
   brew install create-dmg
   ```

3. Run the macOS build script:
   ```bash
   python build_macos_app.py
   ```

4. Output:
   - App bundle: `dist/FlowerEdgeDetection.app`
   - DMG installer: `dist/FlowerEdgeDetection.dmg`

### Distribution

- Share the `.app` bundle for simple distribution
- Share the `.dmg` file for a professional installation experience

## Cross-Platform Building

While it's possible to build for other platforms from a single OS, it's generally recommended to build on the target platform for best compatibility.

If you need to build for multiple platforms, consider using CI/CD platforms like GitHub Actions or setting up virtual machines for each target OS.

## Common Issues

### Missing Libraries

If the app fails to run with missing library errors:

- **Windows:** Install Visual C++ Redistributable
- **Linux:** Install required packages: `opencv`, `tkinter`, etc.
- **macOS:** Install XQuartz for X11 dependencies

### Icon Issues

If custom icons don't appear:
- Windows: Ensure `.ico` file is in the correct format
- macOS: Create a proper `.icns` file with multiple resolutions
- Linux: Provide PNG icons in various sizes

### Packaging Errors

If the packaging process fails:
- Ensure all dependencies are installed
- Check for permissions issues in the output directory
- Look for conflicting files from previous builds

## Customizing the Build

Edit the build scripts to customize:

- Application name and version
- Icons and branding
- Dependencies
- File associations

## Support

If you encounter issues with the build process, check:
1. Python and dependency versions
2. System requirements
3. Build logs in the terminal output