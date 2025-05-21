import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from src.ui.environment_frame import PythonEnvironmentFrame

class PyVersionerApp(ctk.CTk):
    def __init__(self, version="1.0.0"):
        super().__init__()
        
        # Store application version
        self.version = version
        
        # Setup the window
        self.title("Python Version Comparison Tool")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Initialize script path
        self.script_path = None
        
        # Setup UI components
        self._create_menu()
        self._setup_layout()
        
    def _create_menu(self):
        """Create the application menu."""
        self.menu = tk.Menu(self)
        self.configure(menu=self.menu)
        
        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Script", command=self.browse_script)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        
        # Help menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_command(label="Documentation", command=self.show_documentation)
    
    def _setup_layout(self):
        """Set up the main application layout."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Title frame with script selection
        self._create_title_frame()
        
        # Environment frames
        self.env1 = PythonEnvironmentFrame(self, "Environment 1")
        self.env1.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        
        self.env2 = PythonEnvironmentFrame(self, "Environment 2")
        self.env2.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        
        # Run together button
        self._create_run_frame()
    
    def _create_title_frame(self):
        """Create the title frame with script selection."""
        title_frame = ctk.CTkFrame(self)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        title_frame.grid_columnconfigure(1, weight=1)
        
        # Script selection
        ctk.CTkLabel(title_frame, text="Python Script:").grid(
            row=0, column=0, sticky="w", padx=5, pady=10
        )
        self.script_entry = ctk.CTkEntry(title_frame)
        self.script_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        browse_button = ctk.CTkButton(
            title_frame, text="Browse", command=self.browse_script
        )
        browse_button.grid(row=0, column=2, sticky="e", padx=5, pady=10)

    
    def _create_run_frame(self):
        """Create the frame with the run button."""
        run_frame = ctk.CTkFrame(self)
        run_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        run_frame.grid_columnconfigure(0, weight=1)
        
        self.run_together_button = ctk.CTkButton(
            run_frame,
            text="Run in Both Environments",
            command=self.run_both,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled",
        )
        self.run_together_button.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
    
    def browse_script(self):
        """Open file dialog to select a Python script."""
        script_path = filedialog.askopenfilename(
            title="Select Python Script",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")],
        )
        
        if script_path:
            self.script_path = script_path
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, script_path)
            
            # Enable run buttons if Python versions are detected
            if hasattr(self.env1, 'version_info') and self.env1.version_info:
                self.env1.run_button.configure(state="normal")
            if hasattr(self.env2, 'version_info') and self.env2.version_info:
                self.env2.run_button.configure(state="normal")
            
            if (hasattr(self.env1, 'version_info') and self.env1.version_info and
                hasattr(self.env2, 'version_info') and self.env2.version_info):
                self.run_together_button.configure(state="normal")
    
    def run_both(self):
        """Run the script in both environments."""
        if not self.script_path:
            messagebox.showerror("Error", "Please select a Python script first.")
            return
        
        self.env1.run_script()
        self.env2.run_script()
    
    def show_about(self):
        """Show the about dialog."""
        messagebox.showinfo(
            "About",
            f"Python Version Comparison Tool v{self.version}\n"
            "Licensed under MIT License"
        )
    
    def show_documentation(self):
        """Show the documentation window."""
        doc_text = """
Python Version Comparison Tool
==============================

USAGE:
1. Select Python script with Browse button
2. Configure environments
3. Run script in both environments
4. Compare output

FEATURES:
- Compare Python versions side-by-side
- Test compatibility across versions
- View packages in each environment
"""
        
        # Create a window for documentation
        doc_window = ctk.CTkToplevel(self)
        doc_window.title("Documentation")
        doc_window.geometry("600x400")
        doc_window.grid_columnconfigure(0, weight=1)
        doc_window.grid_rowconfigure(0, weight=1)
        doc_window.transient(self)  # Make window stay on top of parent
        doc_window.grab_set()  # Make window modal
        doc_window.focus_force()  # Force focus on this window


        # Create a text widget for the documentation
        doc_text_widget = scrolledtext.ScrolledText(
            doc_window,
            wrap=tk.WORD,
            font=("Arial", 20),
            bg="#1e1e1e",
            fg="#f0f0f0",
        )
        doc_text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        doc_text_widget.insert(tk.END, doc_text)
        doc_text_widget.configure(state="disabled")
