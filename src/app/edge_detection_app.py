import os
import cv2
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QFileDialog, QMessageBox, QFrame, QGridLayout, QCheckBox, QMenuBar)
from PyQt6.QtGui import QPixmap, QImage, QAction, QIcon
from PyQt6.QtCore import Qt, QSize
import platform

# Import from modular structure
# Unused Tkinter imports removed
from src.utils.edge_detection import EdgeDetector
from src.utils.image_processor import ImageProcessor


class EdgeDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flower Edge Detection App")
        self.setGeometry(100, 100, 1280, 900)  # x, y, width, height

        # Platform-specific adjustments (can be adapted if needed)
        self.platform = platform.system().lower()
        self.apply_platform_adjustments()

        # Initialize components
        self.image_processor = ImageProcessor()
        self.edge_detector = EdgeDetector()

        # Variables
        self.image_path = None
        self.original_image = None
        self.original_image_qimage = None  # For PyQt display
        self.processed_images = {}
        self.display_size = QSize(256, 256)  # Standard display size for PyQt

        # Create GUI components
        self.create_widgets()
        self.create_menu()

        # Central widget
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

        # Apply a modern stylesheet (example)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E2E2E;
            }
            QLabel {
                color: #FFFFFF;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #A0A0A0;
                color: #D0D0D0;
            }
            QFrame#imageFrame {
                border: 1px solid #555555;
                border-radius: 5px;
            }
            QLabel#titleLabel {
                font-size: 12pt;
                font-weight: bold;
                color: #FFFFFF;
                padding-bottom: 5px;
            }
            QCheckBox {
                color: #FFFFFF;
            }
            QMenuBar {
                background-color: #383838;
                color: #FFFFFF;
            }
            QMenuBar::item {
                background-color: #383838;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
            QMenu {
                background-color: #383838;
                color: #FFFFFF;
                border: 1px solid #555555;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
        """)

    def apply_platform_adjustments(self):
        """Apply platform-specific UI adjustments"""
        # PyQt handles many platform specifics automatically.
        # Custom adjustments can be added here if needed.
        # For example, font settings:
        # font = self.font()
        # if self.platform == "darwin":  # macOS
        #     font.setFamily("SF Pro")
        # elif self.platform == "windows":
        #     font.setFamily("Segoe UI")
        # self.setFont(font)
        pass

    def create_widgets(self):
        self.main_layout = QVBoxLayout()

        # Top frame for buttons
        self.top_frame_layout = QHBoxLayout()
        top_widget = QWidget()
        top_widget.setLayout(self.top_frame_layout)
        self.main_layout.addWidget(top_widget)

        # Button to upload image
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)
        self.top_frame_layout.addWidget(self.upload_btn)

        # Process buttons
        self.process_btn_sobel = QPushButton("Apply Sobel")
        self.process_btn_sobel.clicked.connect(
            lambda: self.process_image("Sobel"))
        self.process_btn_sobel.setEnabled(False)
        self.top_frame_layout.addWidget(self.process_btn_sobel)

        self.process_btn_prewitt = QPushButton("Apply Prewitt")
        self.process_btn_prewitt.clicked.connect(
            lambda: self.process_image("Prewitt"))
        self.process_btn_prewitt.setEnabled(False)
        self.top_frame_layout.addWidget(self.process_btn_prewitt)

        self.process_btn_canny = QPushButton("Apply Canny")
        self.process_btn_canny.clicked.connect(
            lambda: self.process_image("Canny"))
        self.process_btn_canny.setEnabled(False)
        self.top_frame_layout.addWidget(self.process_btn_canny)

        self.process_btn_laplacian = QPushButton("Apply Laplacian")
        self.process_btn_laplacian.clicked.connect(
            lambda: self.process_image("Laplacian"))
        self.process_btn_laplacian.setEnabled(False)
        self.top_frame_layout.addWidget(self.process_btn_laplacian)

        self.process_btn_all = QPushButton("Apply All Methods")
        self.process_btn_all.clicked.connect(self.process_all)
        self.process_btn_all.setEnabled(False)
        self.top_frame_layout.addWidget(self.process_btn_all)

        self.top_frame_layout.addStretch()  # Pushes buttons to the left

        # Edge pixel count checkbox
        self.show_pixel_count_checkbox = QCheckBox(
            "Show Edge Pixel Count/Density")
        self.show_pixel_count_checkbox.setChecked(True)
        self.show_pixel_count_checkbox.stateChanged.connect(
            self.update_displays)
        self.top_frame_layout.addWidget(self.show_pixel_count_checkbox)

        # Save Images button
        self.save_btn = QPushButton("Save Results")
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setEnabled(False)
        self.top_frame_layout.addWidget(self.save_btn)

        # Frame for image displays
        self.images_grid_layout = QGridLayout()
        images_widget = QWidget()
        images_widget.setLayout(self.images_grid_layout)
        self.main_layout.addWidget(images_widget, 1)  # Add with stretch factor

        self.image_labels = {}
        self.info_labels = {}

        positions = {
            "Original": (0, 0), "Sobel": (0, 1), "Prewitt": (0, 2),
            # Add an empty cell (1,2) for balance or future use
            "Canny": (1, 0), "Laplacian": (1, 1)
        }

        for name, pos in positions.items():
            frame = QFrame()
            frame.setObjectName("imageFrame")  # For styling
            frame_layout = QVBoxLayout()
            frame.setLayout(frame_layout)

            title_label = QLabel(name)
            title_label.setObjectName("titleLabel")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            frame_layout.addWidget(title_label)

            img_label = QLabel()
            img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            img_label.setFixedSize(self.display_size)  # Ensure consistent size
            # Placeholder background
            img_label.setStyleSheet(
                "background-color: #404040; border-radius: 3px;")
            frame_layout.addWidget(img_label)
            self.image_labels[name] = img_label

            info_label = QLabel("")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setWordWrap(True)
            frame_layout.addWidget(info_label)
            self.info_labels[name] = info_label

            self.images_grid_layout.addWidget(frame, pos[0], pos[1])

        # Configure grid weights for responsiveness
        for i in range(2):  # 2 rows
            self.images_grid_layout.setRowStretch(i, 1)
        for i in range(3):  # 3 columns
            self.images_grid_layout.setColumnStretch(i, 1)

        # Status bar
        self.status_bar = self.statusBar()  # QMainWindow has a built-in status bar
        self.status_bar.setStyleSheet(
            "background-color: #383838; color: #FFFFFF; padding: 3px;")
        self.status_bar.showMessage("Ready")

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "",
            "Image files (*.jpg *.jpeg *.png *.bmp *.gif);;All files (*.*)"
        )

        if not file_path:
            return

        try:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path)

            if self.original_image is None:
                raise ValueError("Could not read the image")

            # Convert from BGR to RGB for display
            rgb_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.original_image_qimage = self.convert_cv_to_qimage(rgb_image)

            self.display_qimage("Original", self.original_image_qimage)
            self.enable_buttons(True)
            self.status_bar.showMessage(
                f"Image loaded: {os.path.basename(file_path)}")
            # Clear previous results
            self.processed_images = {}
            for method in ["Sobel", "Prewitt", "Canny", "Laplacian"]:
                if method in self.image_labels:
                    self.image_labels[method].clear()
                    self.image_labels[method].setText(
                        " ")  # Placeholder to keep size
                    self.image_labels[method].setStyleSheet(
                        "background-color: #404040; border-radius: 3px;")
                if method in self.info_labels:
                    self.info_labels[method].setText("")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Could not load image: {str(e)}")
            self.status_bar.showMessage("Error loading image")

    def convert_cv_to_qimage(self, cv_img):
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        q_img = QImage(cv_img.data, width, height,
                       bytes_per_line, QImage.Format.Format_RGB888)
        return q_img.copy()  # Important to copy, otherwise data might go out of scope

    def display_qimage(self, name, q_image):
        if name not in self.image_labels:
            return

        pixmap = QPixmap.fromImage(q_image)
        self.image_labels[name].setPixmap(
            pixmap.scaled(self.display_size, Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )
        if name != "Original" and name in self.processed_images:
            self.update_info_label(name)

    def enable_buttons(self, enabled):
        self.process_btn_sobel.setEnabled(enabled)
        self.process_btn_prewitt.setEnabled(enabled)
        self.process_btn_canny.setEnabled(enabled)
        self.process_btn_laplacian.setEnabled(enabled)
        self.process_btn_all.setEnabled(enabled)
        self.save_btn.setEnabled(enabled and bool(self.processed_images))

    def process_image(self, method):
        if self.original_image is None:
            QMessageBox.warning(
                self, "Warning", "Please upload an image first")
            return

        try:
            self.status_bar.showMessage(f"Processing with {method}...")
            QApplication.processEvents()  # Update UI

            if method == "Sobel":
                result = self.edge_detector.apply_sobel(self.original_image)
            elif method == "Prewitt":
                result = self.edge_detector.apply_prewitt(self.original_image)
            elif method == "Canny":
                result = self.edge_detector.apply_canny(self.original_image)
            elif method == "Laplacian":
                result = self.edge_detector.apply_laplacian(
                    self.original_image)
            else:
                raise ValueError(f"Unknown method: {method}")

            self.processed_images[method] = result
            # Convert grayscale to QImage for display
            # Grayscale QImage needs Format_Grayscale8
            height, width = result.shape
            bytes_per_line = width
            gray_qimage = QImage(result.data, width, height,
                                 bytes_per_line, QImage.Format.Format_Grayscale8)

            self.display_qimage(method, gray_qimage)
            self.status_bar.showMessage(f"{method} edge detection completed")
            self.enable_buttons(True)  # Re-check save button state

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Processing error with {method}: {str(e)}")
            self.status_bar.showMessage(f"Error during {method} processing")

    def process_all(self):
        if self.original_image is None:
            QMessageBox.warning(
                self, "Warning", "Please upload an image first")
            return
        self.status_bar.showMessage("Applying all edge detection methods...")
        QApplication.processEvents()
        methods = ["Sobel", "Prewitt", "Canny", "Laplacian"]
        for method in methods:
            self.process_image(method)  # This will update UI for each
        self.status_bar.showMessage("All edge detection methods applied")

    def update_info_label(self, name):
        if name not in self.info_labels:
            return

        if name == "Original" or name not in self.processed_images:
            self.info_labels[name].setText("")
            return

        info_text = ""
        if self.show_pixel_count_checkbox.isChecked():
            edge_pixels = np.count_nonzero(self.processed_images[name])
            total_pixels = self.processed_images[name].size
            edge_density = (edge_pixels / total_pixels) * \
                100 if total_pixels > 0 else 0
            info_text = f"Edge Pixels: {edge_pixels:,}\\nDensity: {edge_density:.2f}%"

        self.info_labels[name].setText(info_text)

    def update_displays(self):
        # This is called when the checkbox state changes
        if "Original" in self.info_labels:  # Check if original label exists
            self.info_labels["Original"].setText(
                "")  # Original has no edge info
        for name in self.processed_images.keys():
            if name in self.info_labels:  # Check if label exists for method
                self.update_info_label(name)

    def save_results(self):
        if not self.processed_images:
            QMessageBox.warning(self, "Warning", "No processed images to save")
            return

        save_dir = QFileDialog.getExistingDirectory(
            self, "Select Directory to Save Images")
        if not save_dir:
            return

        try:
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]
            saved_files_count = 0

            # Save original image (optional, but good for comparison)
            if self.original_image is not None:
                original_save_path = os.path.join(
                    save_dir, f"Original_{base_name}.png")
                cv2.imwrite(original_save_path, self.original_image)
                saved_files_count += 1

            for method, img_data in self.processed_images.items():
                save_path = os.path.join(save_dir, f"{method}_{base_name}.png")
                # img_data is the raw cv2 image
                cv2.imwrite(save_path, img_data)
                saved_files_count += 1

            QMessageBox.information(
                self, "Success", f"Saved {saved_files_count} images to:\\n{save_dir}")
            self.status_bar.showMessage(f"Images saved to {save_dir}")

        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Error saving images: {str(e)}")
            self.status_bar.showMessage("Error saving images")

    def create_menu(self):
        menu_bar = self.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&File")
        open_action = QAction(QIcon.fromTheme(
            "document-open"), "&Open Image...", self)  # Example icon
        open_action.triggered.connect(self.upload_image)
        file_menu.addAction(open_action)

        save_action = QAction(QIcon.fromTheme(
            "document-save"), "&Save Results...", self)
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)

        file_menu.addSeparator()
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Process menu
        process_menu = menu_bar.addMenu("&Process")
        actions_data = [
            ("Sobel", "Apply &Sobel"), ("Prewitt", "Apply &Prewitt"),
            ("Canny", "Apply &Canny"), ("Laplacian", "Apply &Laplacian")
        ]
        for method, text in actions_data:
            action = QAction(text, self)
            # Need to use a lambda that captures method by value
            action.triggered.connect(
                lambda checked=False, m=method: self.process_image(m))
            process_menu.addAction(action)

        process_menu.addSeparator()
        apply_all_action = QAction("Apply &All Methods", self)
        apply_all_action.triggered.connect(self.process_all)
        process_menu.addAction(apply_all_action)

        # Help menu
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_about(self):
        QMessageBox.about(
            self,
            "About Edge Detection App",
            """<b>Flower Edge Detection Application</b><br><br>
            A modern application for applying and comparing
            different edge detection algorithms on images.<br><br>
            Built with OpenCV and PyQt6.<br><br>
            © 2025 Muhammad Thariq Arya Putra Sembiring"""
        )

# The ThemeSelector and SplashScreen from Tkinter will need to be
# re-implemented or adapted for PyQt if their functionality is still desired.
# For now, they are commented out or will raise errors if not handled.


# Main execution (if this file is run directly)
# This __main__ block is not strictly necessary here if app/main.py is the primary entry point.
# However, it can be useful for testing this component independently.
# Consider removing if app/main.py is always used.
if __name__ == '__main__':
    import sys
    # It's good practice to handle high DPI scaling
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(
            Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(
            Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    main_window = EdgeDetectionApp()
    main_window.show()
    sys.exit(app.exec())
