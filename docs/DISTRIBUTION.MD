\

````markdown
<!-- filepath: /home/renhoshizora/Learning/ImageProcessing/docs/DISTRIBUTION.md -->

# Flower Edge Detection App - Distribution Guide

This guide explains how to build and distribute the application for Windows, Linux, and macOS platforms. The application now uses PyQt6 for its interface.

## Prerequisites

Before building the application, ensure the following are installed:

- Python 3.7 or higher
- pip (Python package installer)
- Required system packages depending on platform (see platform-specific sections)
- PyQt6 and its dependencies (OpenCV, NumPy, Pillow)

## Quick Start

To build the application for your current platform:

```bash
python build_scripts/build_app.py
```

The universal build script will detect your platform and use the appropriate build method. Output files will be placed in the `dist/` directory.

## Windows (.exe)

### Building on Windows

1. Install required tools:

   ```bash
   pip install pyinstaller pillow numpy opencv-python PyQt6
   ```

2. Run the Windows build script:

   ```bash
   python build_scripts/build_windows_exe.py
   ```

3. Output:
   - Standalone executable: `dist/FlowerEdgeDetection.exe`
   - (Installer creation might require additional tools like NSIS, to be configured in the script)

### NSIS Installer (Optional)

To create a Windows installer, install NSIS (Nullsoft Scriptable Install System):

1. Download and install NSIS from [nsis.sourceforge.io](https://nsis.sourceforge.io/Download)
2. Ensure `makensis` is in your PATH
3. The `build_windows_exe.py` script would need to be updated to integrate NSIS for installer creation.

### Windows Distribution

- Share the standalone `.exe` file for simple distribution.
- If an installer is created, share that for a more professional installation experience.

## Linux (.deb, .rpm)

### Building on Linux

1. Install system requirements:

   ```bash
   # Debian/Ubuntu
   sudo apt-get update
   sudo apt-get install -y python3-dev python3-pip ruby ruby-dev build-essential libxcb-xinerama0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0 libgl1-mesa-glx
   sudo gem install fpm

   # Fedora/RHEL
   sudo dnf install -y python3-devel python3-pip ruby ruby-devel gcc make rpm-build xcb-util-wm xcb-util-image xcb-util-keysyms xcb-util-renderutil libxkbcommon-x11 mesa-libGL
   sudo gem install fpm
   ```

2. Install Python requirements:

   ```bash
   pip install pyinstaller pillow numpy opencv-python PyQt6
   ```

3. Run the Linux build script:

   ```bash
   python build_scripts/build_linux_packages.py
   ```

4. Output:
   - DEB package: `dist/flower-edge-detection_1.0.0_amd64.deb`
   - RPM package: `dist/flower-edge-detection-1.0.0-1.x86_64.rpm` (Note: versioning for RPM might differ slightly)

### Linux Distribution

For Debian-based distributions (Ubuntu, Debian, etc.):

```bash
sudo dpkg -i dist/flower-edge-detection_1.0.0_amd64.deb
sudo apt-get install -f  # To resolve any dependencies (e.g., PyQt6 system libraries if not bundled fully)
```

For RPM-based distributions (Fedora, RHEL, CentOS):

```bash
sudo rpm -i dist/flower-edge-detection-1.0.0-1.x86_64.rpm
# Dependencies might need to be handled by the system package manager or ensured they are bundled.
```

## macOS (.app, .dmg)

### Building on macOS

1. Install requirements:

   ```bash
   pip install pyinstaller pillow numpy opencv-python PyQt6
   ```

2. For better DMG creation (optional):

   ```bash
   brew install create-dmg
   ```

3. Run the macOS build script:

   ```bash
   python build_scripts/build_macos_app.py
   ```

4. Output:
   - App bundle: `dist/FlowerEdgeDetection.app`
   - DMG installer: `dist/FlowerEdgeDetection.dmg` (if `create-dmg` is used and script supports it)

### macOS Distribution

- Share the `.app` bundle for simple distribution.
- Share the `.dmg` file for a professional installation experience.

## Cross-Platform Building

It's generally recommended to build on the target platform for best compatibility, especially with GUI frameworks like PyQt6 that may have platform-specific dependencies or behaviors.

If you need to build for multiple platforms, consider using CI/CD platforms like GitHub Actions or setting up virtual machines for each target OS.

## Common Issues with PyQt6 Distribution

### Missing Libraries/Plugins

PyQt6 applications might require specific platform plugins (e.g., for windowing system integration, image formats) to be bundled correctly by PyInstaller.

- Ensure PyInstaller hooks for PyQt6 are active or add them manually if needed (`--hidden-import=PyQt6.sip`, `--add-data PyQt6/Qt6/plugins/*:PyQt6/Qt6/plugins`). The Linux build script has been updated to include some of these.
- **Windows:** May need Visual C++ Redistributable. PyInstaller usually bundles necessary DLLs, but issues can arise.
- **Linux:** Ensure system libraries that PyQt6 links against (like XCB, GL, etc.) are available on the target system if not fully bundled. The `fpm` package dependencies should cover common ones.
- **macOS:** Similar to Linux, ensure necessary frameworks are bundled or available.

### Icon Issues

- Ensure icons are correctly specified in the PyInstaller spec file or command and are in the appropriate format (`.ico` for Windows, `.icns` for macOS, various PNGs for Linux).
- For PyQt6, setting the window icon is done via `app.setWindowIcon(QIcon('path/to/icon.png'))`.

### Packaging Errors

- Ensure all Python dependencies (`PyQt6`, `opencv-python`, `numpy`, `Pillow`) are installed in the environment used by PyInstaller.
- Check PyInstaller logs for specific errors related to PyQt6 or its components.

## Customizing the Build

Edit the build scripts (`build_windows_exe.py`, `build_linux_packages.py`, `build_macos_app.py`) and any associated PyInstaller `.spec` files to customize:

- Application name, version, author, etc.
- Icons and other assets.
- Bundled data files and hidden imports for PyInstaller.
- `fpm` package metadata (dependencies, description, etc.).

## Support

If you encounter issues with the build process:

1. Verify Python and all package versions (`PyQt6`, `PyInstaller`, etc.).
2. Check system requirements and necessary development tools for your platform.
3. Examine the detailed build logs from PyInstaller and `fpm`.
4. Consult PyInstaller and PyQt6 documentation for platform-specific bundling advice.
````
