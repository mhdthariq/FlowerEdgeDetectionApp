import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

def load_sample_image():
    """
    Load a sample image or create a test pattern if no image is available
    """
    # Try to find a sample image
    sample_paths = [
        "sample_flower.jpg",
        "../sample_flower.jpg",
        "test_image.jpg",
        "../test_image.jpg"
    ]
    
    for path in sample_paths:
        if os.path.exists(path):
            print(f"Using existing image: {path}")
            return cv2.imread(path)
    
    # If no image is found, create a synthetic test pattern
    print("Creating synthetic test pattern")
    size = 512
    img = np.zeros((size, size, 3), dtype=np.uint8)
    
    # Create a flower-like pattern
    center = (size // 2, size // 2)
    for r in range(20, 200, 20):
        color = np.random.randint(0, 255, 3).tolist()
        cv2.circle(img, center, r, color, -1)
    
    # Add some "petals"
    for angle in range(0, 360, 45):
        rad = np.radians(angle)
        pt1 = (int(center[0] + 100 * np.cos(rad)), int(center[1] + 100 * np.sin(rad)))
        pt2 = (int(center[0] + 230 * np.cos(rad)), int(center[1] + 230 * np.sin(rad)))
        color = np.random.randint(150, 255, 3).tolist()
        cv2.ellipse(img, center, (230, 100), angle, 0, 45, color, -1)
    
    # Save the synthetic image
    cv2.imwrite("sample_flower.jpg", img)
    return img



def apply_sobel(gray):
    """Apply Sobel edge detection"""
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    result = cv2.magnitude(sobelx, sobely)
    # Normalize to 0-255
    return cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

def apply_prewitt(gray):
    """Apply Prewitt edge detection"""
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
    prewittx = cv2.filter2D(gray, -1, kernelx)
    prewitty = cv2.filter2D(gray, -1, kernely)
    result = cv2.magnitude(prewittx.astype(np.float64), prewitty.astype(np.float64))
    return cv2.normalize(result, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

def apply_canny(gray):
    """Apply Canny edge detection"""
    return cv2.Canny(gray, 100, 200)

def apply_laplacian(gray):
    """Apply Laplacian edge detection"""
    result = cv2.Laplacian(gray, cv2.CV_64F)
    return np.uint8(np.absolute(result))

def calculate_metrics(edge_image):
    """Calculate edge pixel count and density"""
    # Calculate edge pixel count and density
    edge_pixels = np.count_nonzero(edge_image)
    total_pixels = edge_image.size
    edge_density = (edge_pixels / total_pixels) * 100
    
    return edge_pixels, edge_density

def save_result_images(original, methods_dict, base_name="flower"):
    """Save all processed images with method name prefix"""
    # Create results directory if it doesn't exist
    results_dir = "results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    
    # Save original image
    cv2.imwrite(os.path.join(results_dir, f"Original_{base_name}.png"), original)
    
    # Save method results
    for method_name, img in methods_dict.items():
        output_path = os.path.join(results_dir, f"{method_name}_{base_name}.png")
        cv2.imwrite(output_path, img)
        print(f"Saved: {output_path}")
    
    return results_dir

def main():
    # Load or create sample image
    image = load_sample_image()
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection methods
    sobel_edges = apply_sobel(gray)
    prewitt_edges = apply_prewitt(gray)
    canny_edges = apply_canny(gray)
    laplacian_edges = apply_laplacian(gray)
    
    # Store all processed images
    methods = {
        "Sobel": sobel_edges,
        "Prewitt": prewitt_edges,
        "Canny": canny_edges,
        "Laplacian": laplacian_edges
    }
    
    # Save all result images
    base_name = "sample_flower"
    results_dir = save_result_images(image, methods, base_name)
    print(f"All images saved to {results_dir} directory")
    
    # Print metrics
    print("\nEdge Detection Metrics:")
    print("-" * 40)
    print(f"{'Method':<12} {'Edge Pixels':<12} {'Density (%)':<12}")
    print("-" * 40)
    
    for name, img in methods.items():
        pixels, density = calculate_metrics(img)
        print(f"{name:<12} {pixels:<12} {density:<12.2f}")
    
    # Create figure for display
    plt.figure(figsize=(15, 10))
    
    # Display original and edge detection results
    plt.subplot(231), plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    
    plt.subplot(232), plt.imshow(sobel_edges, cmap='gray')
    plt.title('Sobel Edge Detection'), plt.xticks([]), plt.yticks([])
    
    plt.subplot(233), plt.imshow(prewitt_edges, cmap='gray')
    plt.title('Prewitt Edge Detection'), plt.xticks([]), plt.yticks([])
    
    plt.subplot(234), plt.imshow(canny_edges, cmap='gray')
    plt.title('Canny Edge Detection'), plt.xticks([]), plt.yticks([])
    
    plt.subplot(235), plt.imshow(laplacian_edges, cmap='gray')
    plt.title('Laplacian Edge Detection'), plt.xticks([]), plt.yticks([])
    
    # Remove ground truth display
    
    # Save comparison image
    plt.tight_layout()
    comparison_path = os.path.join(results_dir, 'edge_detection_comparison.png')
    plt.savefig(comparison_path)
    plt.show()
    
    print(f"\nComparison image saved as '{comparison_path}'")

if __name__ == "__main__":
    main()