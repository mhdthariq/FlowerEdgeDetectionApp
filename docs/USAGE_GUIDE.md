# Edge Detection Application - Usage Guide

## Introduction

This guide covers how to use the Flower Edge Detection Application, a tool that allows you to apply and compare different edge detection algorithms to your images. This version uses PyQt6 for its graphical user interface.

## Launching the Application

1. Ensure you have Python and the required libraries installed (see `requirements.txt`).
2. Navigate to the project root directory in your terminal.
3. Run the application using: `python main.py` or `python -m src.app.main`

## Main Interface Overview

The application window consists of:

- **Menu Bar**: Located at the top, providing access to File, Process, and Help options.
- **Toolbar**: Below the menu bar, containing main action buttons:
  - **Upload Image**: To load an image for processing.
  - **Apply Sobel, Prewitt, Canny, Laplacian**: To apply individual edge detection algorithms.
  - **Apply All Methods**: To apply all available algorithms at once.
  - **Show Edge Pixel Count/Density**: A checkbox to toggle the display of metrics below processed images.
  - **Save Results**: To save the original and all processed images.
- **Image Display Area**: A grid layout showing the original image and the results of different edge detection methods.
- **Status Bar**: At the bottom, displaying messages about application status and actions.

## Basic Usage

### 1. Loading an Image

1. Click the "Upload Image" button in the toolbar (or select File > Open Image... from the menu).
2. A file dialog will appear. Select an image file (e.g., JPG, PNG, BMP, GIF).
3. The original image will be displayed in the top-left panel, labeled "Original".
4. Once an image is loaded, the processing buttons will become active.

### 2. Applying Edge Detection

You can apply edge detection algorithms in two ways:

- **Individual Methods**: Click on the specific button for the desired method in the toolbar (e.g., "Apply Sobel", "Apply Canny") or select the corresponding action from the "Process" menu.
- **All Methods at Once**: Click the "Apply All Methods" button in the toolbar or select "Apply All Methods" from the "Process" menu. This will process the image with Sobel, Prewitt, Canny, and Laplacian algorithms sequentially.

### 3. Viewing Edge Detection Results

Processed images will appear in their respective panels:

- **Original Image**: Top-left
- **Sobel Edges**: Top-center
- **Prewitt Edges**: Top-right
- **Canny Edges**: Bottom-left
- **Laplacian Edges**: Bottom-center

Each panel is titled with the method name.

### 4. Edge Pixel Metrics

- Ensure the "Show Edge Pixel Count/Density" checkbox in the toolbar is checked (it is by default).
- Below each processed edge image, you will see:
  - **Edge Pixel Count**: The total number of pixels identified as edges.
  - **Edge Density**: The percentage of the image area that consists of edge pixels.
- Unchecking the checkbox will hide these metrics.

### 5. Saving Results

1. After processing images, click the "Save Results" button in the toolbar (or select File > Save Results... from the menu).
2. A directory selection dialog will appear. Choose a folder where you want to save the images.
3. The application will save:
   - The original uploaded image (e.g., `Original_filename.png`).
   - Each processed edge image (e.g., `Sobel_filename.png`, `Canny_filename.png`).
4. A confirmation message will indicate the number of saved files and the location.

## Menu Bar Options

- **File Menu**:
  - **Open Image...**: Same as the "Upload Image" button.
  - **Save Results...**: Same as the "Save Results" button.
  - **Exit**: Closes the application.
- **Process Menu**:
  - **Apply Sobel, Prewitt, Canny, Laplacian**: Apply individual methods.
  - **Apply All Methods**: Apply all methods.
- **Help Menu**:
  - **About**: Displays information about the application.

## Understanding Edge Detection Methods

(This section remains largely the same as it describes the algorithms, not the UI)

### Sobel

- Calculates image intensity gradients at each pixel.
- Detects edges by finding areas with high spatial frequency.
- Good for detecting strong, directional edges.

### Prewitt

- Similar to Sobel but uses a different kernel.
- Often less sensitive to noise.
- Can be better for images with subtle gradients.

### Canny

- Multi-stage algorithm that includes:
  - Noise reduction
  - Gradient calculation
  - Non-maximum suppression
  - Hysteresis thresholding
- Often provides the cleanest and most precise edges.

### Laplacian

- Detects edges by finding zero crossings after filtering with a Laplacian filter.
- Highlights regions of rapid intensity change.
- Can be sensitive to noise.

## Tips for Best Results

- Use clear, well-lit images with good contrast.
- Compare multiple edge detection methods to find the best one for your specific image.
- Use edge density to quantify the differences between methods.
- Save your results for documentation or further processing.
