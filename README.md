# Flower Edge Detection Application

A Python-based GUI application with a modern interface that allows users to load flower images and apply different edge detection algorithms (Sobel, Canny, Prewitt, and Laplacian) for comparison.

## Features

- Modern, attractive UI built with Python and **PyQt6**
- Support for multiple edge detection methods:
  - Sobel
  - Prewitt
  - Canny
  - Laplacian
- Side-by-side comparison of all methods
- Edge pixel count and density metrics
- Ability to save processed images with method names
- Uniform image sizing for better comparison
- Distributable packages for Windows, Linux, and macOS (requires build script updates for PyQt6)
- Modular architecture for better code organization and extensibility

## Project Structure

The application follows a modular architecture:

```plaintext
├── main.py                 # Main entry point
├── src/                    # Source code directory
│   ├── app/                # Application logic
│   │   ├── edge_detection_app.py  # Main application class (QMainWindow)
│   │   └── main.py         # Application initialization and splash screen
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
- OpenCV (`opencv-python`)
- NumPy
- Pillow
- PyQt6

## Installation

### Method 1: From Source

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd flower-edge-detection-app # Or your project directory name
   ```
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
5. Run the application:
   ```bash
   python main.py
   ```

### Method 2: Using Build Scripts

The repository includes build scripts.

- **Windows**: `build_scripts/build_windows_exe.py`
- **Linux**: `build_scripts/build_linux_packages.py`
- **macOS**: `build_scripts/build_macos_app.py`

See [docs/DISTRIBUTION.md](docs/DISTRIBUTION.md) for general build concepts (will also need updating for PyQt6).

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Click "Upload Image" to select a flower image.
3. Apply edge detection using individual method buttons or "Apply All Methods".
4. Toggle the "Show Edge Pixel Count/Density" checkbox to view metrics.
5. Click "Save Results" to save processed images (e.g., `Sobel_ImageName.png`).
6. Compare the results side by side in the UI.

## Image Processing Methods

- **Sobel**: Calculates the gradient of the image intensity at each pixel.
- **Prewitt**: Similar to Sobel but uses a different kernel, often less sensitive to noise.
- **Canny**: Multi-stage algorithm that detects edges with noise suppression.
- **Laplacian**: Highlights regions of rapid intensity change using the Laplacian operator.

## Example

After loading an image, you'll see a display with:

- Original image
- Sobel edge detection result
- Prewitt edge detection result
- Canny edge detection result
- Laplacian edge detection result

Each processed image display can show the number of edge pixels detected and the edge density percentage.

## Building Distributable Packages

The project includes scripts to create installable packages.

```bash
# Main build script (needs update)
python build_scripts/build_app.py

# Platform-specific build scripts (need update)
python build_scripts/build_windows_exe.py    # For Windows
python build_scripts/build_linux_packages.py  # For Linux
python build_scripts/build_macos_app.py      # For macOS
```

The goal of these scripts (once updated) would be to create:

- **Windows**: An `.exe` installer.
- **Linux**: `.deb` and `.rpm` packages (or AppImage).
- **macOS**: A `.app` bundle and `.dmg` installer.

Refer to [docs/DISTRIBUTION.md](docs/DISTRIBUTION.md).
