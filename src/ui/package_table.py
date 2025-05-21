import customtkinter as ctk
from typing import List, Dict


class CTkPackageTable(ctk.CTkFrame):
    """Table for displaying package information"""
    def __init__(self, master, packages: List[Dict[str, str]], **kwargs):
        super().__init__(master, **kwargs)
        self.packages = packages
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        
        # Create header
        self.header_name = ctk.CTkLabel(
            self, text="Package Name",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("gray75", "gray25"), corner_radius=6
        )
        self.header_name.grid(row=0, column=0, sticky="ew", padx=(5, 2), pady=5)
        
        self.header_version = ctk.CTkLabel(
            self, text="Version",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("gray75", "gray25"), corner_radius=6
        )
        self.header_version.grid(row=0, column=1, sticky="ew", padx=(2, 5), pady=5)
          # Create scrollable frame for package rows
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Populate the table
        self.populate_table()
    
    def populate_table(self):
        """Populate the table with package data"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        # Sort packages by name
        if self.packages:
            self.packages.sort(key=lambda x: x.get("name", "").lower())
        
        # Add package rows
        for i, package in enumerate(self.packages):
            bg_color = ("gray95", "gray15") if i % 2 == 0 else ("gray90", "gray20")
            
            name_label = ctk.CTkLabel(
                self.scrollable_frame, text=package.get("name", "Unknown"),
                anchor="w", fg_color=bg_color, corner_radius=0
            )
            name_label.grid(row=i, column=0, sticky="ew", padx=0, pady=(0, 1))
            
            version_label = ctk.CTkLabel(
                self.scrollable_frame, text=package.get("version", "Unknown"),
                anchor="w", fg_color=bg_color, corner_radius=0
            )
            version_label.grid(row=i, column=1, sticky="ew", padx=0, pady=(0, 1))


class PackageListWindow(ctk.CTkToplevel):
    """Window for displaying installed packages"""
    def __init__(self, packages: List[Dict[str, str]], title: str = "Installed Packages"):
        super().__init__()
        self.title(title)
        self.geometry("600x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create package table
        self.package_table = CTkPackageTable(self, packages)
        self.package_table.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.grab_set()
        self.focus_force()
