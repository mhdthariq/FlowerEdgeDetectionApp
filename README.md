# Flower Edge Detection Application

A Python-based GUI application with a modern interface that allows users to load flower images and apply different edge detection algorithms (Sobel, Canny, Prewitt, and Laplacian) for comparison.

## Features

- Modern, attractive UI built with Tkinter and ttkbootstrap
- Support for multiple edge detection methods:
  - Sobel
  - Prewitt
  - Canny
  - Laplacian
- Side-by-side comparison of all methods
- Edge pixel count and density metrics
- Ability to save processed images with method names
- Uniform image sizing for better comparison
- Distributable packages for Windows, Linux, and macOS
- Modular architecture for better code organization and extensibility

## Project Structure

The application follows a modular architecture:

```plaintext
├── main.py                 # Main entry point
├── src/                    # Source code directory
│   ├── app/                # Application logic
│   │   ├── edge_detection_app.py  # Main application class
│   │   └── main.py         # Application initialization
│   ├── interface/          # User interface components
│   │   ├── splash_screen.py  # Splash screen implementation
│   │   └── themes.py       # Theme management
│   └── utils/              # Utility functions and classes
│       ├── check_dependencies.py  # Dependency checker
│       ├── edge_detection.py  # Edge detection algorithms
│       └── image_processor.py  # Image processing utilities
├── assets/                 # Image assets and resources
├── docs/                   # Documentation
└── tests/                  # Test files
```

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy
- PIL (Pillow)
- Tkinter
- ttkbootstrap

## Installation

### Method 1: From Source

1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
   Note: Tkinter comes with most Python installations.
5. Run the application:
   ```bash
   python main.py
   ```

### Method 2: Using Build Scripts

The repository includes build scripts to create installable packages:

- **Windows**: Use `build_windows_exe.py` to create an `.exe` installer
- **Linux**: Use `build_linux_packages.py` to create `.deb` and `.rpm` packages
- **macOS**: Use `build_macos_app.py` to create a `.app` bundle and `.dmg` installer

See [DISTRIBUTION.md](docs/DISTRIBUTION.md) for detailed build instructions.

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Click "Upload Image" to select a flower image
3. Apply edge detection using individual buttons or "Apply All Methods"
4. Toggle edge pixel count display using the checkbox
5. Click "Save Results" to save processed images as "MethodName_ImageName.png"
6. Compare the results side by side

## Image Processing Methods

- **Sobel**: Calculates the gradient of the image intensity at each pixel
- **Prewitt**: Similar to Sobel but uses a different kernel, often less sensitive to noise
- **Canny**: Multi-stage algorithm that detects edges with noise suppression
- **Laplacian**: Highlights regions of rapid intensity change using the Laplacian operator

## Example

After loading an image, you'll see a display with:

- Original image (top left)
- Sobel edge detection (top center)
- Prewitt edge detection (top right)
- Canny edge detection (bottom left)
- Laplacian edge detection (bottom center)

Each processed image displays the number of edge pixels detected and the edge density percentage.

## Building Distributable Packages

The project includes scripts to create installable packages for distribution. These are located in the `build_scripts` directory:

```bash
# Main build script that detects your platform and runs the appropriate script
python build_scripts/build_app.py

# Platform-specific build scripts
python build_scripts/build_windows_exe.py    # For Windows
python build_scripts/build_linux_packages.py  # For Linux
python build_scripts/build_macos_app.py      # For macOS
```

The build scripts will create:

- **Windows**: An `.exe` installer
- **Linux**: `.deb` and `.rpm` packages
- **macOS**: A `.app` bundle and `.dmg` installer

See [DISTRIBUTION.md](docs/DISTRIBUTION.md) for detailed build instructions.
