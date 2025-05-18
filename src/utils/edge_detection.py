import cv2
import numpy as np


class EdgeDetector:
    """A utility class for various edge detection algorithms"""

    @staticmethod
    def apply_sobel(image):
        """Apply Sobel edge detection to an image

        Parameters:
        - image: Input image (numpy array)

        Returns:
        - Edge detected image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(
            image.shape) > 2 else image

        # Apply Sobel in x and y directions
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

        # Compute the magnitude
        magnitude = np.sqrt(np.square(sobelx) + np.square(sobely))

        # Normalize to 0-255
        normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        result = normalized.astype(np.uint8)

        return result

    @staticmethod
    def apply_prewitt(image):
        """Apply Prewitt edge detection to an image

        Parameters:
        - image: Input image (numpy array)

        Returns:
        - Edge detected image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(
            image.shape) > 2 else image

        # Define Prewitt kernels
        kernelx = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
        kernely = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])

        # Apply kernels
        prewittx = cv2.filter2D(gray, -1, kernelx)
        prewitty = cv2.filter2D(gray, -1, kernely)

        # Compute the magnitude - convert to float for the calculation
        prewittx_float = prewittx.astype(np.float64)
        prewitty_float = prewitty.astype(np.float64)
        magnitude = np.sqrt(np.square(prewittx_float) +
                            np.square(prewitty_float))

        # Normalize to 0-255
        normalized = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        result = normalized.astype(np.uint8)

        return result

    @staticmethod
    def apply_canny(image, threshold1=100, threshold2=200):
        """Apply Canny edge detection to an image

        Parameters:
        - image: Input image (numpy array)
        - threshold1: First threshold for hysteresis procedure
        - threshold2: Second threshold for hysteresis procedure

        Returns:
        - Edge detected image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(
            image.shape) > 2 else image

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Canny edge detector
        edges = cv2.Canny(blurred, threshold1, threshold2)

        return edges

    @staticmethod
    def apply_laplacian(image):
        """Apply Laplacian edge detection to an image

        Parameters:
        - image: Input image (numpy array)

        Returns:
        - Edge detected image
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(
            image.shape) > 2 else image

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Laplacian operator
        laplacian = cv2.Laplacian(blurred, cv2.CV_64F)

        # Convert back to uint8
        laplacian = np.absolute(laplacian)
        laplacian = np.uint8(np.clip(laplacian, 0, 255))

        return laplacian
