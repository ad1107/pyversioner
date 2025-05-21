import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import platform

from src.ui.package_table import PackageListWindow
from src.utils.python_env import detect_python_version, get_installed_packages, run_python_script


class PythonEnvironmentFrame(ctk.CTkFrame):
    """Frame for configuring and running a Python environment"""
    def __init__(self, master, title: str, **kwargs):
        super().__init__(master, **kwargs)
        # Store master without type enforcing
        self._app_master = master
        self.title = title
        self.python_path = None
        self.version_info = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=10, weight="bold"))
        title_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 5))
        
        # Frame for Python selection
        selection_frame = ctk.CTkFrame(self)
        selection_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        selection_frame.grid_columnconfigure(1, weight=1)
        
        # Checkbox for using system Python
        self.use_system_var = tk.BooleanVar(value=True)
        self.use_system_checkbox = ctk.CTkCheckBox(
            selection_frame, 
            text="Use Python from system PATH", 
            variable=self.use_system_var,
            command=self.toggle_path_selection
        )
        self.use_system_checkbox.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Python path selection
        self.path_entry = ctk.CTkEntry(selection_frame, state="disabled")
        self.path_entry.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        
        self.browse_button = ctk.CTkButton(
            selection_frame, 
            text="Browse", 
            command=self.browse_python_executable,
            state="disabled"
        )
        self.browse_button.grid(row=1, column=1, sticky="e", padx=5, pady=5)
        
        # Get Python version button and label
        version_frame = ctk.CTkFrame(self)
        version_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        version_frame.grid_columnconfigure(2, weight=1)
        
        self.check_version_button = ctk.CTkButton(
            version_frame, 
            text="Check Version", 
            command=self.get_python_version
        )
        self.check_version_button.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        self.get_packages_button = ctk.CTkButton(
            version_frame, 
            text="View Packages", 
            command=self.view_installed_packages,
            state="disabled"
        )
        self.get_packages_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)
        
        self.version_label = ctk.CTkLabel(self, text="Python version: Not checked")
        self.version_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)
        
        # Console output
        console_label = ctk.CTkLabel(self, text="Console Output:")
        console_label.grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))
        
        # Console with dark mode
        self.console = scrolledtext.ScrolledText(
            self, 
            height=20, 
            wrap=tk.WORD,
            font=("Courier New", 20),
            bg="#1e1e1e",
            fg="#f0f0f0",
            insertbackground="#f0f0f0"
        )
        self.console.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)
        self.grid_rowconfigure(5, weight=1)
        
        # Run button
        self.run_button = ctk.CTkButton(
            self, 
            text="Run Script", 
            command=self.run_script,
            state="disabled"
        )
        self.run_button.grid(row=6, column=0, sticky="ew", padx=20, pady=10)
        
        # If use_system_var is checked initially, detect system Python
        if self.use_system_var.get():
            self.get_python_version()
    
    def toggle_path_selection(self):
        """Toggle between system Python and custom Python path"""
        if self.use_system_var.get():
            self.path_entry.configure(state="disabled")
            self.browse_button.configure(state="disabled")
            self.python_path = "python"  # Default system Python
        else:
            self.path_entry.configure(state="normal")
            self.browse_button.configure(state="normal")
            self.python_path = None
            self.version_info = None
            self.version_label.configure(text="Python version: Not selected")
            self.get_packages_button.configure(state="disabled")
            self.run_button.configure(state="disabled")
    
    def browse_python_executable(self):
        file_types = [("Python Executable", "python*.exe"), ("All Files", "*.*")] if platform.system() == "Windows" else [("All Files", "*")]
        
        python_path = filedialog.askopenfilename(
            title="Select Python Executable",
            filetypes=file_types
        )
        
        if python_path:
            self.python_path = python_path
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, python_path)
            
            self.get_python_version()
    
    def get_python_version(self):
        """Get and display the Python version"""
        if self.use_system_var.get():
            self.python_path = "python"
        elif not self.python_path:
            if not self.path_entry.get():
                messagebox.showerror("Error", "Please select a Python executable.")
                return
            self.python_path = self.path_entry.get()
        
        version, return_code, error = detect_python_version(self.python_path)
        
        if version:
            self.version_info = version
            self.version_label.configure(text=f"Python version: {version}")

            self.get_packages_button.configure(state="normal")
            if hasattr(self._app_master, 'script_path') and getattr(self._app_master, 'script_path', None):
                self.run_button.configure(state="normal")
        else:
            # Display error
            self.version_label.configure(text=f"Error: {error}")
            self.version_info = None
            self.get_packages_button.configure(state="disabled")
            self.run_button.configure(state="disabled")
    
    def view_installed_packages(self):
        """Show a window with installed packages"""
        if not self.python_path:
            messagebox.showerror("Error", "No Python executable selected.")
            return
        
        # Get packages
        packages, return_code, error = get_installed_packages(self.python_path)
        
        if packages:
            window = PackageListWindow(packages, f"{self.title} - Installed Packages")
        else:
            # Display error
            messagebox.showerror("Error", f"Failed to get package list: {error}")
            print(f"View Packages Error: {error}")
    
    def run_script(self):
        """Run the selected Python script"""
        if not self.python_path:
            messagebox.showerror("Error", "No Python executable selected.")
            return
            
        if not hasattr(self._app_master, 'script_path') or not getattr(self._app_master, 'script_path', None):
            messagebox.showerror("Error", "No Python script selected. Please select a script first.")
            return
        
        # Store script path locally to avoid attribute access issues
        script_path = getattr(self._app_master, 'script_path')
        
        self.console.delete(1.0, tk.END)
        self.console.insert(tk.END, f"Running {script_path} with {self.version_info}...\n\n")
        
        def run():
            stdout, stderr, return_code = run_python_script(self.python_path, script_path)
            
            self.console.insert(tk.END, "STDOUT:\n")
            self.console.insert(tk.END, stdout or "No output\n")
            
            if stderr:
                self.console.insert(tk.END, "\nSTDERR:\n")
                self.console.insert(tk.END, stderr)
            
            if return_code != 0:
                self.console.insert(tk.END, f"\n\nProcess exited with code {return_code}\n")
            else:
                self.console.insert(tk.END, "\n\nProcess completed successfully.\n")
        
        # Run in a separate thread to avoid freezing the UI
        threading.Thread(target=run, daemon=True).start()
