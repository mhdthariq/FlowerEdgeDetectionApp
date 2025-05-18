import os
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import threading
import time
import platform

# Import from modular structure
from src.interface.themes import ThemeSelector
from src.interface.splash_screen import SplashScreen
from src.utils.edge_detection import EdgeDetector
from src.utils.image_processor import ImageProcessor


class EdgeDetectionApp:
    def detect_platform(self):
        """Detect the current operating system platform"""
        return platform.system().lower()

    def apply_platform_adjustments(self):
        """Apply platform-specific UI adjustments"""
        if self.platform == "darwin":  # macOS
            # Use macOS-specific font and scaling
            default_font = "SF Pro"
            self.display_size = (300, 300)  # Larger images for Retina displays
        elif self.platform == "windows":
            # Windows-specific settings
            default_font = "Segoe UI"
            # Add window drop shadow if available
            try:
                self.root.attributes("-transparentcolor", "")
            except:
                pass
        else:
            # Linux and other platforms
            default_font = ""

    def __init__(self, root):
        self.root = root
        self.root.title("Flower Edge Detection App")
        self.root.geometry("1280x900")
        self.style = ttk.Style(theme="darkly")

        # Platform-specific adjustments
        self.platform = self.detect_platform()
        self.apply_platform_adjustments()

        # Initialize components
        self.image_processor = ImageProcessor()
        self.edge_detector = EdgeDetector()

        # Variables
        self.image_path = None
        self.original_image = None
        self.original_image_rgb = None
        self.processed_images = {}
        self.display_size = (256, 256)  # Standard display size

        # Theme selector
        self.theme_selector = ThemeSelector(
            self.root, callback=self.on_theme_change)

        # Create GUI components
        self.create_widgets()

        # Create menu
        self.create_menu()

    def create_widgets(self):
        # Top frame for buttons
        self.top_frame = ttk.Frame(self.root, padding=12)
        self.top_frame.pack(fill=tk.X, padx=15, pady=12)

        # Button to upload image
        self.upload_btn = ttk.Button(
            self.top_frame,
            text="Upload Image",
            command=self.upload_image,
            bootstyle=SUCCESS
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5)

        # Process buttons
        self.process_btn_sobel = ttk.Button(
            self.top_frame,
            text="Apply Sobel",
            command=lambda: self.process_image("Sobel"),
            state=tk.DISABLED,
            bootstyle=PRIMARY
        )
        self.process_btn_sobel.pack(side=tk.LEFT, padx=5)

        self.process_btn_prewitt = ttk.Button(
            self.top_frame,
            text="Apply Prewitt",
            command=lambda: self.process_image("Prewitt"),
            state=tk.DISABLED,
            bootstyle=PRIMARY
        )
        self.process_btn_prewitt.pack(side=tk.LEFT, padx=5)

        self.process_btn_canny = ttk.Button(
            self.top_frame,
            text="Apply Canny",
            command=lambda: self.process_image("Canny"),
            state=tk.DISABLED,
            bootstyle=PRIMARY
        )
        self.process_btn_canny.pack(side=tk.LEFT, padx=5)

        self.process_btn_laplacian = ttk.Button(
            self.top_frame,
            text="Apply Laplacian",
            command=lambda: self.process_image("Laplacian"),
            state=tk.DISABLED,
            bootstyle=PRIMARY
        )
        self.process_btn_laplacian.pack(side=tk.LEFT, padx=5)

        self.process_btn_all = ttk.Button(
            self.top_frame,
            text="Apply All Methods",
            command=self.process_all,
            state=tk.DISABLED,
            bootstyle=INFO
        )
        self.process_btn_all.pack(side=tk.LEFT, padx=5)

        # Edge pixel count checkbox
        self.show_pixel_count = tk.BooleanVar(value=True)
        self.pixel_count_check = ttk.Checkbutton(
            self.top_frame,
            text="Show Edge Pixel Count",
            variable=self.show_pixel_count,
            command=self.update_displays,
            bootstyle="round-toggle"
        )
        self.pixel_count_check.pack(side=tk.RIGHT, padx=5)

        # Save Images button
        self.save_btn = ttk.Button(
            self.top_frame,
            text="Save Results",
            command=self.save_results,
            state=tk.DISABLED,
            bootstyle=SUCCESS
        )
        self.save_btn.pack(side=tk.RIGHT, padx=5)

        # Frame for image displays
        self.images_frame = ttk.Frame(self.root, padding=10)
        self.images_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create image display frames
        self.display_frames = {}
        self.image_labels = {}
        self.info_labels = {}

        # Define display positions
        positions = {
            "Original": (0, 0),
            "Sobel": (0, 1),
            "Prewitt": (0, 2),
            "Canny": (1, 0),
            "Laplacian": (1, 1)
        }

        # Create frames for each image display
        for name, pos in positions.items():
            frame = ttk.Labelframe(
                self.images_frame, text=name, padding=8, bootstyle="secondary")
            frame.grid(row=pos[0], column=pos[1],
                       padx=15, pady=15, sticky="nsew")
            # Make frame title text appear at north position
            frame.configure(labelanchor="n")
            # Add border style for better visibility
            frame.configure(borderwidth=2, relief="ridge")

            # Image display label
            img_label = ttk.Label(frame)
            img_label.pack(pady=8)
            self.image_labels[name] = img_label

            # Info label for pixel count
            info_label = ttk.Label(
                frame, text="", bootstyle="info", font=("", 10, "bold"))
            info_label.pack(pady=8, fill="x", padx=5)
            self.info_labels[name] = info_label

            self.display_frames[name] = frame

        # Configure grid weights
        for i in range(2):
            self.images_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.images_frame.grid_columnconfigure(i, weight=1)

        # Theme selector widget
        theme_frame = self.theme_selector.create_theme_selector(self.root)
        theme_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=8)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            bootstyle="inverse-info",
            padding=8,
            anchor=tk.W,
            font=("", 10)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def upload_image(self):
        """Upload and display an image"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )

        if not file_path:
            return

        try:
            self.image_path = file_path
            self.original_image = cv2.imread(file_path)

            if self.original_image is None:
                raise ValueError("Could not read the image")

            # Convert from BGR to RGB for display
            self.original_image_rgb = cv2.cvtColor(
                self.original_image, cv2.COLOR_BGR2RGB)

            # Display original image
            self.display_image("Original", self.original_image_rgb)

            # Enable processing buttons
            self.enable_buttons()

            self.status_var.set(f"Image loaded: {os.path.basename(file_path)}")

        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {str(e)}")
            self.status_var.set("Error loading image")

    def enable_buttons(self):
        """Enable processing buttons after image is loaded"""
        for btn in [
            self.process_btn_sobel,
            self.process_btn_prewitt,
            self.process_btn_canny,
            self.process_btn_laplacian,
            self.process_btn_all,
            self.save_btn
        ]:
            btn.config(state=tk.NORMAL)

    def process_image(self, method):
        """Process the image with the selected edge detection method"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please upload an image first")
            return

        try:
            self.status_var.set(f"Processing with {method}...")
            self.root.update()

            # Apply edge detection based on method
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

            # Store the result
            self.processed_images[method] = result

            # Display the result
            # Convert to RGB for display (edges are grayscale but need 3 channels for PIL)
            display_img = cv2.cvtColor(result, cv2.COLOR_GRAY2RGB)
            self.display_image(method, display_img)

            self.status_var.set(f"{method} edge detection completed")

        except Exception as e:
            messagebox.showerror("Error", f"Processing error: {str(e)}")
            self.status_var.set(f"Error during {method} processing")

    def process_all(self):
        """Apply all edge detection methods"""
        self.status_var.set("Applying all edge detection methods...")
        self.root.update()
        methods = ["Sobel", "Prewitt", "Canny", "Laplacian"]
        for method in methods:
            self.process_image(method)
        self.status_var.set("All edge detection methods applied")

    def display_image(self, name, image):
        """Display an image in the appropriate frame"""
        # Resize the image to standard size
        resized = cv2.resize(image, self.display_size)

        # Convert to PIL format for Tkinter
        img_pil = Image.fromarray(resized)
        img_tk = ImageTk.PhotoImage(img_pil)

        # Update image label
        self.image_labels[name].configure(image=img_tk)
        self.image_labels[name].image = img_tk  # Keep a reference

        # Update info label if needed
        if name != "Original" and name in self.processed_images:
            self.update_info_label(name)

    def update_info_label(self, name):
        """Update the information label with edge pixel count"""
        if name not in self.processed_images and name != "Original":
            self.info_labels[name].configure(text="")
            return

        info_text = ""

        # Add edge pixel count and density if selected
        if self.show_pixel_count.get() and name != "Original":
            # Count non-zero pixels (edges)
            edge_pixels = np.count_nonzero(self.processed_images[name])
            total_pixels = self.processed_images[name].size
            edge_density = (edge_pixels / total_pixels) * 100

            info_text += f"Edge pixels: {edge_pixels:,}\nDensity: {edge_density:.2f}%"

        # Update info label
        self.info_labels[name].configure(text=info_text)

    def update_displays(self):
        """Update all information displays"""
        self.update_info_label("Original")
        for name in self.processed_images.keys():
            self.update_info_label(name)

    def save_results(self):
        """Save all processed images to disk"""
        if not self.processed_images:
            messagebox.showwarning("Warning", "No processed images to save")
            return

        try:
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(self.image_path))[0]

            # Ask for directory to save images
            save_dir = filedialog.askdirectory(
                title="Select Directory to Save Images")

            if not save_dir:
                return

            # Save original image
            original_save_path = os.path.join(
                save_dir, f"Original_{base_name}.png")
            cv2.imwrite(original_save_path, self.original_image)

            # Save processed images
            saved_files = [original_save_path]
            for method, img in self.processed_images.items():
                save_path = os.path.join(save_dir, f"{method}_{base_name}.png")
                cv2.imwrite(save_path, img)
                saved_files.append(save_path)

            # Confirmation message
            messagebox.showinfo(
                "Success",
                f"Saved {len(saved_files)} images to:\n{save_dir}"
            )

            self.status_var.set(f"Images saved to {save_dir}")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Error saving images: {str(e)}")
            self.status_var.set("Error saving images")

    def create_menu(self):
        """Create the application menu bar"""
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Image", command=self.upload_image)
        file_menu.add_command(label="Save Results", command=self.save_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Process menu
        process_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Process", menu=process_menu)
        process_menu.add_command(label="Sobel Edge Detection",
                                 command=lambda: self.process_image("Sobel"))
        process_menu.add_command(label="Prewitt Edge Detection",
                                 command=lambda: self.process_image("Prewitt"))
        process_menu.add_command(label="Canny Edge Detection",
                                 command=lambda: self.process_image("Canny"))
        process_menu.add_command(label="Laplacian Edge Detection",
                                 command=lambda: self.process_image("Laplacian"))
        process_menu.add_separator()
        process_menu.add_command(
            label="Apply All Methods", command=self.process_all)

        # Theme menu
        self.theme_selector.create_theme_menu(menu_bar)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def show_about(self):
        """Display about information"""
        messagebox.showinfo(
            title="About Edge Detection App",
            message="Flower Edge Detection Application\n\n"
                    "A modern application for applying and comparing\n"
                    "different edge detection algorithms on images.\n\n"
                    "Built with OpenCV, Tkinter, and ttkbootstrap.\n\n"
                    "© 2025 Muhammad Thariq Arya Putra Sembiring"
        )

    def on_theme_change(self, theme_name):
        """Callback for when theme changes"""
        # Update any components that need adjustment
        self.status_var.set(f"Theme changed to {theme_name}")

        # Update frame title colors
        self.update_frame_title_colors()

        # Refresh displays if needed
        self.update_displays()

    def update_frame_title_colors(self):
        """Update frame title colors to ensure visibility"""
        # Frame titles are handled through the bootstyle property
        # No need to manually configure them
        pass
