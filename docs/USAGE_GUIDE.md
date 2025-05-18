# Edge Detection Application - Usage Guide

## Introduction

This guide covers how to use the Flower Edge Detection Application, a tool that allows you to apply and compare different edge detection algorithms to your images.

## Basic Usage

### 1. Loading an Image

1. Launch the application by running `python main.py` from the project root
2. Click the "Upload Image" button in the top toolbar
3. Select a flower image (JPG, PNG, or other common formats)
4. The original image will appear in the top-left panel

### 2. Applying Edge Detection

You can apply edge detection in two ways:

- **Individual Methods**: Click on any of these buttons:

  - "Apply Sobel"
  - "Apply Prewitt"
  - "Apply Canny"
  - "Apply Laplacian"

- **All Methods at Once**: Click "Apply All Methods" to process the image with all four algorithms simultaneously

### 3. Viewing Edge Detection Results

After processing, you'll see:

- Original image (top left)
- Sobel edge detection (top center)
- Prewitt edge detection (top right)
- Canny edge detection (bottom left)
- Laplacian edge detection (bottom center)

### 4. Edge Pixel Metrics

Toggle the "Show Edge Pixel Count" checkbox to display:

- **Edge Pixel Count**: The number of pixels identified as edges
- **Edge Density**: The percentage of the image covered by edges

These metrics help you compare the sensitivity of different edge detection methods.

### 5. Saving Results

To save your processed images:

1. Click the "Save Results" button
2. Select a directory where you want to save the images
3. Click "Save" or "OK"

All images will be saved with the naming pattern: `MethodName_ImageName.png`

For example, if you processed "flower.jpg", you'll get these files:

- `Original_flower.png`
- `Sobel_flower.png`
- `Prewitt_flower.png`
- `Canny_flower.png`
- `Laplacian_flower.png`

## Understanding Edge Detection Methods

### Sobel

- Calculates image intensity gradients at each pixel
- Detects edges by finding areas with high spatial frequency
- Good for detecting strong, directional edges

### Prewitt

- Similar to Sobel but uses a different kernel
- Often less sensitive to noise
- Can be better for images with subtle gradients

### Canny

- Multi-stage algorithm that includes:
  - Noise reduction
  - Gradient calculation
  - Non-maximum suppression
  - Hysteresis thresholding
- Often provides the cleanest and most precise edges

### Laplacian

- Detects edges by finding zero crossings after filtering with a Laplacian filter
- Highlights regions of rapid intensity change
- Can be sensitive to noise

## Tips for Best Results

- Use clear, well-lit images with good contrast
- Compare multiple edge detection methods to find the best one for your specific image
- Use edge density to quantify the differences between methods
- Save your results for documentation or further processing
