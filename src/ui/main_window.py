import tkinter as tk
from tkinter import ttk
import sys
import os

from src.ui.opengl_frame import OpenGLFrame
from src.ui.sidebar import Sidebar
from src.ui.toolbar import Toolbar
from src.models.scene_manager import SceneManager

class MainWindow:
    def __init__(self, master):
        """
        Initialize the main application window
        
        Args:
            master: The tkinter root window
        """
        self.master = master
        self.scene_manager = SceneManager()
        
        # Configure the main window
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Create main frame to hold all components
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create toolbar at the top
        self.toolbar = Toolbar(self.main_frame, self)
        self.toolbar.pack(fill=tk.X, side=tk.TOP)
        
        # Create a horizontal paned window
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Create sidebar on the left
        self.sidebar = Sidebar(self.paned_window, self)
        
        # Create OpenGL frame on the right
        self.opengl_frame = OpenGLFrame(self.paned_window, self.scene_manager)
        
        # Set main window reference in OpenGL frame for history updates
        self.opengl_frame.set_main_window(self)
        
        # Add sidebar and OpenGL frame to the paned window
        self.paned_window.add(self.sidebar, weight=1)
        self.paned_window.add(self.opengl_frame, weight=4)
        
        # Create status bar
        self.status_bar = ttk.Label(self.main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set up key bindings
        self.setup_bindings()
        
    def setup_bindings(self):
        """Set up keyboard and mouse bindings"""
        self.master.bind("<Escape>", lambda e: self.on_close())
        
    def update_status(self, message):
        """Update the status bar with a message"""
        self.status_bar.config(text=message)
        
    def on_close(self):
        """Handle application closing"""
        if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.opengl_frame.cleanup()
            self.master.destroy()
            sys.exit(0) 