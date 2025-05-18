import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

class ThemeSelector:
    """A utility class for selecting and applying ttkbootstrap themes"""
    
    def __init__(self, root, callback=None):
        """
        Initialize the theme selector
        
        Parameters:
        - root: The root window to apply themes to
        - callback: Optional callback function to execute after theme change
        """
        self.root = root
        self.callback = callback
        self.available_themes = self._get_available_themes()
    
    def _get_available_themes(self):
        """Get all available ttkbootstrap themes"""
        return [
            "darkly",       # Dark theme with blue accents
            "superhero",    # Dark blue theme
            "solar",        # Brown/orange dark theme
            "cyborg",       # High contrast dark theme
            "vapor",        # Purple/pink theme
            "morph",        # Light blue theme
            "litera",       # Clean light theme
            "flatly",       # Flat design light theme
            "journal",      # News-like light theme
            "yeti",         # Clean modern light theme
            "pulse",        # Pink/purple light theme
            "cosmo",        # Clean sans-serif theme
            "sandstone",    # Orange accents light theme
            "united",       # Red accents light theme
            "lumen",        # Light minimal theme
            "cerculean"     # Blue light theme
        ]
    
    def create_theme_menu(self, parent_menu):
        """
        Create a themes submenu in the given parent menu
        
        Parameters:
        - parent_menu: The parent menu to add themes submenu to
        """
        theme_menu = tk.Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label="Themes", menu=theme_menu)
        
        # Add a radio button for each theme
        theme_var = tk.StringVar(value=self.root.style.theme.name)
        
        for theme in self.available_themes:
            theme_menu.add_radiobutton(
                label=theme.capitalize(),
                value=theme,
                variable=theme_var,
                command=lambda t=theme: self.apply_theme(t)
            )
        
        return theme_menu
    
    def create_theme_selector(self, parent):
        """
        Create a theme selector component (combobox) within a parent widget
        
        Parameters:
        - parent: The parent widget to add the selector to
        
        Returns:
        - frame: The frame containing the theme selector
        """
        frame = ttk.Frame(parent, padding=5)
        
        # Label
        ttk.Label(frame, text="Theme:").pack(side=tk.LEFT, padx=5)
        
        # Combobox
        theme_cb = ttk.Combobox(
            frame,
            values=[t.capitalize() for t in self.available_themes],
            state="readonly",
            width=15
        )
        theme_cb.set(self.root.style.theme.name.capitalize())
        theme_cb.pack(side=tk.LEFT, padx=5)
        
        # Bind selection event
        theme_cb.bind("<<ComboboxSelected>>", 
                      lambda e: self.apply_theme(self.available_themes[theme_cb.current()]))
        
        return frame
    
    def apply_theme(self, theme_name):
        """
        Apply the selected theme to the application
        
        Parameters:
        - theme_name: Name of the theme to apply
        """
        try:
            # Apply the theme
            self.root.style.theme_use(theme_name)
            
            # Update window background if needed
            if hasattr(self.root, '_configure_window_bg'):
                self.root._configure_window_bg()
            
            # Make sure to update any labelframes to keep white text for visibility
            self._ensure_label_visibility()
            
            # Call the callback if provided
            if self.callback:
                self.callback(theme_name)
                
            return True
            
        except Exception as e:
            messagebox.showerror("Theme Error", f"Error applying theme '{theme_name}': {str(e)}")
            return False
            
    def _ensure_label_visibility(self):
        """Ensure all labelframe titles are visible"""
        # For ttkbootstrap, frame labels are handled through styling
        # No need to manually configure them in newer versions
        pass
    
    def get_current_theme(self):
        """Get the name of the currently applied theme"""
        return self.root.style.theme.name


# Example usage:
if __name__ == "__main__":
    # Create a sample application
    root = ttk.Window(themename="darkly")
    root.title("Theme Selector Demo")
    root.geometry("400x300")
    
    # Create main container
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Add some sample widgets
    ttk.Label(main_frame, text="Theme Selector Demo", font=("Helvetica", 16)).pack(pady=10)
    ttk.Button(main_frame, text="Primary Button", bootstyle=PRIMARY).pack(pady=5)
    ttk.Button(main_frame, text="Secondary Button", bootstyle=SECONDARY).pack(pady=5)
    ttk.Button(main_frame, text="Success Button", bootstyle=SUCCESS).pack(pady=5)
    ttk.Button(main_frame, text="Danger Button", bootstyle=DANGER).pack(pady=5)
    
    # Create menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    
    # Create file menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=root.quit)
    
    # Add theme selector menu
    theme_selector = ThemeSelector(root)
    theme_selector.create_theme_menu(menu_bar)
    
    # Add theme selector widget at the bottom
    theme_frame = theme_selector.create_theme_selector(root)
    theme_frame.pack(side=tk.BOTTOM, pady=10)
    
    # Start the application
    root.mainloop()