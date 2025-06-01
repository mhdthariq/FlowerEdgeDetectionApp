# Modular Structure - Implementation Guide

This document provides a guide to the modular structure implementation for the Edge Detection Application, now using PyQt6.

## Overview

The Image Processing application has been refactored to a modular architecture and converted to use PyQt6 for its graphical user interface. This improves maintainability, readability, and extensibility. The key goals were:

1.  Separate concerns into distinct modules.
2.  Improve code organization.
3.  Enhance testability.
4.  Make the codebase more maintainable.
5.  Utilize the capabilities of the PyQt6 framework.

## Directory Structure

The application now follows this organized structure:

```plaintext
├── main.py                 # Main entry point for the application
├── src/                    # Source code directory
│   ├── app/                # Core application logic and UI
│   │   ├── __init__.py
│   │   ├── edge_detection_app.py  # Main application window (QMainWindow)
│   │   └── main.py         # PyQt6 application initialization, splash screen
│   └── utils/              # Utility functions and classes
│       ├── __init__.py
│       ├── check_dependencies.py  # Dependency checker (primarily for build)
│       ├── edge_detection.py  # Edge detection algorithms
│       └── image_processor.py  # Image processing utilities
├── assets/                 # Image assets (icons, sample images)
├── build_scripts/          # Scripts for building distributable packages
└── docs/                   # Documentation files
```

The `src/interface/` directory has been removed as UI components are now primarily managed within `src/app/edge_detection_app.py` using PyQt6 widgets.

## Module Responsibilities

### Main Entry Point (`main.py` at project root)

The root-level `main.py` serves as the primary script to launch the application. It:

- Sets up the Python path.
- Configures basic logging.
- Imports and calls `run_pyqt_app_with_splash` from `src.app.main` to start the PyQt6 application.

### App Module (`src/app/`)

Contains the core application logic and PyQt6 UI implementation.

#### `edge_detection_app.py`

This file defines the `EdgeDetectionApp` class, which is a `QMainWindow`. It is responsible for:

- Creating and managing the main user interface using PyQt6 widgets (buttons, labels, layouts, menus, etc.).
- Handling user interactions through signals and slots.
- Coordinating image loading, processing (delegating to `utils`), and display.
- Managing the display of original and processed images and their associated information (edge pixel count, density).

#### `main.py` (within `src/app/`)

This file handles the setup and launch of the PyQt6 application environment:

- Initializes `QApplication`.
- Manages and displays a splash screen (`QSplashScreen`) during startup.
- Creates an instance of `EdgeDetectionApp` (the main window).
- Shows the main window and starts the Qt event loop.

### Utils Module (`src/utils/`)

Contains utility classes and functions that provide core, non-UI-specific functionality.

#### `edge_detection.py`

The `EdgeDetector` class implements various edge detection algorithms:

- Sobel
- Prewitt
- Canny
- Laplacian

These methods take a CV2 image object and return a processed (edges) CV2 image object.

#### `image_processor.py`

The `ImageProcessor` class (if still heavily used, otherwise its functions might be simpler or integrated elsewhere) would handle:

- Loading images using OpenCV (`cv2.imread`).
- Converting image formats (e.g., BGR to RGB for display with QImage, or CV2 to QImage).
- Resizing images.

#### `check_dependencies.py`

This utility is primarily used by the build scripts (`build_scripts/build_app.py`) to verify that necessary packages for building (like PyInstaller) are available. It's less critical for runtime if the application is packaged correctly.

## Benefits of the Modular Structure (with PyQt6)

1.  **Separation of Concerns**: UI (PyQt6 in `src/app`) is distinct from processing logic (`src/utils`).
2.  **Improved Maintainability**: Changes to the UI or processing algorithms are localized.
3.  **Better Testability**: Utility modules can be tested independently of the UI.
4.  **Code Reusability**: Image processing functions can be reused.
5.  **Leverages PyQt6 Features**: Utilizes signals/slots, layouts, and a rich widget set for a modern UI.
6.  **Clearer Project Layout**: Easier for developers to navigate and understand.

## Extending the Application

To add a new edge detection algorithm:

1.  Implement the new algorithm in `src/utils/edge_detection.py` within the `EdgeDetector` class.
2.  Update the UI in `src/app/edge_detection_app.py`:
    - Add a new `QPushButton` for the method.
    - Connect its `clicked` signal to a handler that calls the new method.
    - Add a display area (e.g., `QLabel` for the image, `QLabel` for info) if it doesn't fit the existing layout.
    - Update the "Apply All Methods" functionality.
    - Update the "Process" menu.

## Future Directions

The modular structure and PyQt6 foundation facilitate future enhancements:

1.  More sophisticated UI/UX improvements using advanced Qt features.
2.  Implementing a plugin system for new algorithms or image filters.
3.  Developing a comprehensive test suite using `pytest` or `unittest`, potentially with `pytest-qt` for UI testing.
4.  Adding more image processing tools (e.g., thresholding, filtering, transformations).
5.  Integrating with a settings/preferences system (e.g., using `QSettings`).
