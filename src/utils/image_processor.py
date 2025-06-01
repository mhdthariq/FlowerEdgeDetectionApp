import os
import cv2
import numpy as np
from PIL import Image  # Removed ImageTk
from PyQt6.QtGui import QImage, QPixmap  # Added QImage and QPixmap imports


class ImageProcessor:
    """A utility class for image processing operations"""

    def __init__(self):
        """Initialize the image processor"""
        self.current_image = None
        self.original_image = None

    def load_image(self, image_path):
        """Load an image from the given path

        Parameters:
        - image_path: Path to the image file

        Returns:
        - OpenCV image (numpy array) or None if failed
        """
        if not os.path.exists(image_path):
            return None

        try:
            image = cv2.imread(image_path)
            self.original_image = image.copy()
            self.current_image = image
            return image
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    def resize_for_display(self, image, display_size):
        """Resize an image for display purposes while maintaining aspect ratio

        Parameters:
        - image: OpenCV image (numpy array)
        - display_size: Tuple (width, height) for target size

        Returns:
        - Resized image
        """
        if image is None:
            return None

        # Get original dimensions
        h, w = image.shape[:2]
        target_w, target_h = display_size

        # Calculate aspect ratio
        aspect = w / h

        # Determine new dimensions based on aspect ratio
        if w > h:
            new_w = target_w
            new_h = int(new_w / aspect)
            if new_h > target_h:
                new_h = target_h
                new_w = int(new_h * aspect)
        else:
            new_h = target_h
            new_w = int(new_h * aspect)
            if new_w > target_w:
                new_w = target_w
                new_h = int(new_w / aspect)

        # Resize the image
        resized = cv2.resize(image, (new_w, new_h),
                             interpolation=cv2.INTER_AREA)

        return resized

    def convert_to_qpixmap(self, image):
        """Convert an OpenCV image to a QPixmap for display in PyQt.

        Parameters:
        - image: OpenCV image (numpy array)

        Returns:
        - QPixmap object or None if failed
        """
        if image is None:
            return None

        try:
            # OpenCV images are typically BGR. Convert to RGB.
            if len(image.shape) == 3 and image.shape[2] == 3:  # Color image
                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h,
                                  bytes_per_line, QImage.Format.Format_RGB888)
            elif len(image.shape) == 2:  # Grayscale image
                h, w = image.shape
                bytes_per_line = w
                qt_image = QImage(image.data, w, h, bytes_per_line,
                                  QImage.Format.Format_Grayscale8)
            else:
                print("Unsupported image format for QPixmap conversion.")
                return None

            return QPixmap.fromImage(qt_image)
        except Exception as e:
            print(f"Error converting image to QPixmap: {e}")
            return None

    def save_image(self, image, save_path):
        """Save an image to the specified path

        Parameters:
        - image: OpenCV image (numpy array)
        - save_path: Path to save the image

        Returns:
        - Boolean indicating success/failure
        """
        if image is None:
            return False

        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Save the image
            result = cv2.imwrite(save_path, image)
            return result
        except Exception as e:
            print(f"Error saving image: {e}")
            return False
