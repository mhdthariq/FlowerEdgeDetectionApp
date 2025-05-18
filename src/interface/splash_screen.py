import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import os
import time
import threading
import sys

class SplashScreen:
    """A splash screen that shows while the application is loading"""
    
    def __init__(self, parent, image_path=None, timeout=2000):
        """Initialize the splash screen
        
        Parameters:
        parent - The parent window (hidden during splash)
        image_path - Path to splash image (creates default if None)
        timeout - Time in milliseconds before closing splash
        """
        self.parent = parent
        self.timeout = timeout
        
        # Create splash window
        self.root = tk.Toplevel()
        self.root.withdraw()  # Hide initially to avoid flicker
        
        # Remove window decorations
        self.root.overrideredirect(True)
        
        # Set window style
        self.bg_color = "#1e1e2f"  # Dark background
        self.root.configure(bg=self.bg_color)
        
        # Splash screen size
        width, height = 500, 350
        
        # Center splash screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Raise above all windows
        self.root.attributes('-topmost', True)
        
        # Create frame with border
        frame = tk.Frame(self.root, bg=self.bg_color, bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.95, relheight=0.95)
        
        # Logo or image
        if image_path and os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((200, 200), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                logo_label = tk.Label(frame, image=photo, bg=self.bg_color)
                logo_label.image = photo
                logo_label.pack(pady=(30, 10))
            except Exception:
                self._create_default_logo(frame)
        else:
            self._create_default_logo(frame)
        
        # Application name
        app_name = tk.Label(
            frame, 
            text="FLOWER EDGE DETECTION", 
            font=("Helvetica", 16, "bold"), 
            fg="#86b6c2",
            bg=self.bg_color
        )
        app_name.pack(pady=5)
        
        # Loading message
        self.message_var = tk.StringVar(value="Loading application...")
        message = tk.Label(
            frame, 
            textvariable=self.message_var, 
            font=("Helvetica", 10), 
            fg="#ffffff",
            bg=self.bg_color
        )
        message.pack(pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            frame, 
            length=300, 
            bootstyle="info-striped",
            mode="indeterminate"
        )
        self.progress.pack(pady=10, padx=20)
        self.progress.start(15)
        
        # Version info
        version = tk.Label(
            frame, 
            text="Version 1.0", 
            font=("Helvetica", 8), 
            fg="#999999",
            bg=self.bg_color
        )
        version.pack(pady=5)
    
    def _create_default_logo(self, parent):
        """Create a default logo when image is not available"""
        logo_frame = tk.Frame(parent, bg=self.bg_color, height=120, width=120)
        logo_frame.pack(pady=(20, 10))
        
        # Draw a simple flower-like shape
        canvas = tk.Canvas(logo_frame, width=120, height=120, bg=self.bg_color, bd=0, highlightthickness=0)
        canvas.pack()
        
        # Draw petals
        petal_color = "#9c72ca"  # Purple
        center_x, center_y = 60, 60
        
        for i in range(8):
            angle = i * 45
            x1 = center_x + 40 * self._cos_deg(angle)
            y1 = center_y + 40 * self._sin_deg(angle)
            canvas.create_oval(
                center_x-20, center_y-20, 
                x1+20, y1+20, 
                fill=petal_color, outline=""
            )
        
        # Draw center circle
        canvas.create_oval(40, 40, 80, 80, fill="#86b6c2", outline="")
        
    def _cos_deg(self, deg):
        """Cosine function for degrees"""
        import math
        return math.cos(math.radians(deg))
        
    def _sin_deg(self, deg):
        """Sine function for degrees"""
        import math
        return math.sin(math.radians(deg))
    
    def show(self):
        """Show the splash screen and start the timeout timer"""
        # Show splash screen
        self.root.deiconify()
        
        # Update to ensure window is drawn
        self.root.update()
        
        # Start timer to close splash screen
        self.root.after(self.timeout, self._finish)
        
    def update_message(self, message):
        """Update the loading message"""
        self.message_var.set(message)
        self.root.update()
    
    def _finish(self):
        """Close splash screen and show parent window"""
        # Stop progress bar animation
        self.progress.stop()
        
        # Hide splash screen
        self.root.withdraw()
        
        # Show parent window
        self.parent.deiconify()
        self.parent.focus_force()
        
        # Destroy splash screen after a brief delay
        self.root.after(200, self.root.destroy)


# Example usage
if __name__ == "__main__":
    # Create a window to serve as the parent
    main_window = tk.Tk()
    main_window.title("Main Application")
    main_window.geometry("800x600")
    main_window.withdraw()  # Hide main window during splash
    
    # Create and show splash screen
    splash = SplashScreen(main_window, timeout=3000)
    splash.show()
    
    # Simulate loading tasks
    def loading_tasks():
        time.sleep(0.8)
        splash.update_message("Loading modules...")
        time.sleep(0.7)
        splash.update_message("Initializing components...")
        time.sleep(0.7)
        splash.update_message("Starting application...")
        time.sleep(0.8)
    
    # Run loading tasks in background thread
    threading.Thread(target=loading_tasks).start()
    
    # Add content to main window
    ttk.Label(main_window, text="Application Content", font=("Helvetica", 24)).pack(pady=50)
    
    # Start main loop
    main_window.mainloop()