<!-- filepath: /home/renhoshizora/Learning/ImageProcessing/docs/CODE_EXPLANATION.md -->

# Edge Detection Application - Code Explanation

## Architecture Overview

The Edge Detection Application follows a modular architecture to improve maintainability, readability, and extensibility. The code is organized into distinct modules with clear responsibilities, and the application is structured around a main `EdgeDetectionApp` class that handles the GUI interface and coordinates the image processing functionality. It utilizes **PyQt6** for a modern user interface.

## Project Structure

The application is organized into the following directory structure:

```text
├── main.py                 # Main entry point
├── src/                    # Source code directory
│   ├── app/                # Application logic
│   │   ├── __init__.py
│   │   ├── edge_detection_app.py  # Main application class (PyQt6 based)
│   │   └── main.py         # Application initialization (PyQt6 based)
│   └── utils/              # Utility functions and classes
│       ├── __init__.py
│       ├── check_dependencies.py  # Dependency checker
│       ├── edge_detection.py  # Edge detection algorithms
│       └── image_processor.py  # Image processing utilities
├── assets/                 # Image assets and resources
│   └── ...
└── docs/                   # Documentation
    └── ...
```

(Note: The `src/interface/` directory was removed as UI components are now integrated within `src/app/` using PyQt6.)

## Key Components

### 1. Main Application Class (`EdgeDetectionApp`)

The `EdgeDetectionApp` class (now using PyQt6) serves as the core container for all application functionality:

- Initializes the GUI with PyQt6 widgets and layouts.
- Manages image loading and processing.
- Handles display of processed images.
- Calculates and displays metrics (edge pixel count and density).
- Saves processed images to disk.
- Implements a basic dark theme using QSS (Qt Style Sheets).

### 2. GUI Structure (PyQt6)

The GUI is organized using PyQt6 layouts and widgets:

```text
QMainWindow
├── Central Widget (QWidget)
│   ├── Main Layout (QVBoxLayout)
│   │   ├── Top Button Layout (QHBoxLayout)
│   │   │   ├── Upload Button (QPushButton)
│   │   │   ├── Process Buttons (QPushButton for each algorithm)
│   │   │   ├── Save Results Button (QPushButton)
│   │   │   └── Theme Toggle (QCheckBox - if implemented, or handled by system theme)
│   │   ├── Images Grid Layout (QGridLayout)
│   │   │   ├── Original Image Area (QGroupBox)
│   │   │   │   ├── Image Label (QLabel)
│   │   │   │   └── Info Label (QLabel)
│   │   │   ├── Sobel Image Area (QGroupBox)
│   │   │   │   ├── Image Label (QLabel)
│   │   │   │   └── Info Label (QLabel)
│   │   │   └── [Other Edge Detection Areas]
│   │   └── Status Bar (QStatusBar - part of QMainWindow)
```

The application uses PyQt6's layout managers (e.g., `QVBoxLayout`, `QHBoxLayout`, `QGridLayout`) for organizing UI elements.

### 3. Image Processing Workflow

The processing workflow remains largely the same, with UI interactions handled by PyQt6:

1. Load an image using a `QFileDialog` and OpenCV.
2. Convert to grayscale for edge detection.
3. Apply the selected edge detection algorithm (Sobel, Canny, Prewitt, Laplacian).
4. Convert the OpenCV image (NumPy array) to a `QPixmap` for display in a `QLabel`.
5. Calculate and show metrics (edge pixel count and density).
6. Optionally save processed results to disk using `QFileDialog`.

### 4. Edge Detection Methods

The underlying edge detection algorithms (Sobel, Prewitt, Canny, Laplacian) implemented in `src/utils/edge_detection.py` remain unchanged. Their integration with the UI is now through PyQt6 signals and slots.

#### Sobel Edge Detection

- Uses `cv2.Sobel()` function.
- Combines gradients using magnitude calculation.
- Normalizes results to 0-255 range for display.

#### Prewitt Edge Detection

- Implemented using custom kernels and `cv2.filter2D()`.
- Combines X and Y components using magnitude calculation.

#### Canny Edge Detection

- Uses OpenCV’s `cv2.Canny()`.
- Applies Gaussian blur, gradient calculation, non-maximum suppression, and hysteresis thresholding.
- Parameters (100, 200) control the lower and upper thresholds for hysteresis.

#### Laplacian Edge Detection

- Implements `cv2.Laplacian()`.
- Computes second derivative of the image.
- Takes absolute value to handle both positive and negative changes.

## Code Breakdown (PyQt6 specific)

### Initialization and Setup

The `__init__` method of `EdgeDetectionApp` initializes the `QMainWindow`, sets up variables, applies a basic stylesheet, and calls methods to create widgets and layouts.

### Widget Creation

Methods like `initUI`, `create_top_buttons`, `create_image_display_areas`, etc., construct all GUI components using PyQt6 widgets (`QPushButton`, `QLabel`, `QGroupBox`, etc.) and arrange them using layouts.

### Image Handling

- **Loading**: `upload_image` uses `QFileDialog.getOpenFileName` and then `cv2.imread`.
- **Display**: `display_image` converts the OpenCV image (NumPy array) to `QImage` and then `QPixmap` to set on a `QLabel`.
- **Saving**: `save_results` uses `QFileDialog.getSaveFileName` and `cv2.imwrite`.
- **Event Handling**: Button clicks are connected to methods (slots) using `button.clicked.connect(self.method_name)`.

### Processing and Metrics

The calculation of edge pixel count and edge density remains the same, with results displayed in `QLabel` widgets.

## Integration Between Components

- **OpenCV to QPixmap Conversion**: The application uses OpenCV for image processing. Results (NumPy arrays) are converted to `QImage` and then `QPixmap` for display in PyQt6 `QLabel`s.
- **Signal-Slot Mechanism**: PyQt6's signal-slot mechanism is used for event handling (e.g., button clicks triggering processing methods).
- **Standardized Image Size**: Images are typically resized for consistent display, though this can be made more dynamic with PyQt6 layouts.
- **Styling**: Basic styling is applied using QSS. `QMessageBox` styling has been updated to adapt to system light/dark themes.

## Saving Functionality

The `save_results` method:

- Uses `QFileDialog.getSaveFileName` for selecting the destination.
- Saves images using `cv2.imwrite`.
- Provides feedback via the status bar or `QMessageBox`.

## Potential Extensions

The code, now using PyQt6, can be extended:

- Adding more edge detection algorithms is still straightforward.
- UI for algorithm parameters can be added using various PyQt6 input widgets.
- Advanced theming and styling capabilities with QSS.
- Better responsive design using PyQt6's layout system.
- Batch processing and other features can be integrated.
- Ensuring proper asset bundling (e.g., icons) for distribution, potentially using `sys._MEIPASS` for PyInstaller.
