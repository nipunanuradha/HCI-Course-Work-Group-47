import tkinter as tk
from tkinter import ttk
import sys
import platform
import numpy as np

if platform.system() == "Windows":
    from ctypes import windll
    
    # Fix DPI scaling issues on Windows
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

try:
    from PIL import Image, ImageTk
    import OpenGL
    from OpenGL import GL as gl
    from OpenGL.GL import shaders
    from OpenGL.GLU import *
except ImportError as e:
    print(f"Error importing OpenGL libraries: {e}")
    print("Please ensure you have installed all required packages.")
    sys.exit(1)

# Use GLFW for OpenGL context handling if available
try:
    import glfw
    USE_GLFW = True
except ImportError:
    USE_GLFW = False
    print("GLFW not available, using tkinter for OpenGL context")

from src.rendering.renderer import Renderer
from src.interaction.camera import Camera
from src.interaction.input_handler import InputHandler
from src.rendering.matrix import vec3

class OpenGLFrame(ttk.Frame):
    def __init__(self, parent, scene_manager):
        """
        Initialize the OpenGL rendering frame
        
        Args:
            parent: Parent tkinter widget
            scene_manager: SceneManager instance to manage 3D scene data
        """
        ttk.Frame.__init__(self, parent, relief=tk.SUNKEN, borderwidth=1)
        
        self.parent = parent
        self.scene_manager = scene_manager
        
        # Main window will be set after initialization by the main_window class
        self.main_window = None
        
        # Initialize OpenGL canvas
        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Initialize camera
        self.camera = Camera()
        self.camera.position = np.array([0.0, 2.0, 5.0], dtype=np.float32)
        self.camera.target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        
        # Initialize input handler
        self.input_handler = InputHandler(self.canvas, self.camera, self.scene_manager, None)  # main_window will be set later
        
        # Set up OpenGL context
        self.setup_gl_context()
        
        # Initialize renderer only if we have a valid GL context
        if hasattr(self, "has_gl_context") and self.has_gl_context:
            self.renderer = Renderer(self.scene_manager, self.camera)
        
        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)
        
        # Start render loop
        self.after(16, self.render_loop)  # Approx. 60 FPS
    
    def set_main_window(self, main_window):
        """Set the main window reference and update the input handler"""
        self.main_window = main_window
        if self.input_handler:
            self.input_handler.main_window = main_window
    
    def setup_gl_context(self):
        """Set up the OpenGL context"""
        self.has_gl_context = False
        
        if USE_GLFW:
            try:
                # Initialize GLFW
                if not glfw.init():
                    print("Failed to initialize GLFW")
                    self.use_placeholder()
                    return
                    
                # Configure GLFW
                glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
                glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
                glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
                
                # Create a windowed mode window and its OpenGL context
                self.glfw_window = glfw.create_window(800, 600, "OpenGL Context", None, None)
                if not self.glfw_window:
                    glfw.terminate()
                    print("Failed to create GLFW window")
                    self.use_placeholder()
                    return
                    
                # Make the window's context current
                glfw.make_context_current(self.glfw_window)
                self.has_gl_context = True
                print("Successfully created OpenGL context with GLFW")
            except Exception as e:
                print(f"Error setting up GLFW: {e}")
                self.use_placeholder()
        else:
            # Use tkinter's togl widget or equivalent
            # This is platform-dependent and might require additional setup
            print("GLFW not available, using placeholder")
            self.use_placeholder()
    
    def use_placeholder(self):
        """Display a placeholder if OpenGL context creation fails"""
        # Show placeholder image or message
        self.placeholder_label = ttk.Label(self.canvas, 
                                         text="OpenGL rendering would appear here.\nCouldn't initialize OpenGL context.",
                                         background="black", foreground="white",
                                         anchor=tk.CENTER)
        self.canvas.create_window(400, 300, window=self.placeholder_label)
        
        # Skip renderer initialization if we don't have an OpenGL context
        self.renderer = None
    
    def on_resize(self, event):
        """Handle window resize events"""
        width, height = event.width, event.height
        if USE_GLFW and hasattr(self, 'glfw_window') and self.has_gl_context:
            glfw.set_window_size(self.glfw_window, width, height)
        
        # Update viewport
        if hasattr(self, 'renderer') and self.renderer is not None:
            self.renderer.resize(width, height)
        
        # Update camera aspect ratio
        self.camera.aspect_ratio = width / max(1, height)
        
        # Update placeholder position if using placeholder
        if hasattr(self, 'placeholder_label'):
            self.canvas.create_window(width//2, height//2, window=self.placeholder_label)
    
    def render_loop(self):
        """Main render loop"""
        if USE_GLFW and hasattr(self, 'glfw_window') and self.has_gl_context:
            # Make context current
            glfw.make_context_current(self.glfw_window)
            
            # Render the scene
            if self.renderer is not None:
                self.renderer.render()
            
            # Capture the framebuffer
            width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
            if width > 0 and height > 0:
                try:
                    # Read pixels from the framebuffer
                    pixels = gl.glReadPixels(0, 0, width, height, gl.GL_RGB, gl.GL_UNSIGNED_BYTE)
                    
                    # Convert to PIL Image
                    image = Image.frombytes('RGB', (width, height), pixels)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # OpenGL has bottom-left origin
                    
                    # Convert to PhotoImage and display on canvas
                    photo = ImageTk.PhotoImage(image=image)
                    self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
                    self.canvas.image = photo  # Keep a reference to prevent garbage collection
                except Exception as e:
                    print(f"Error capturing framebuffer: {e}")
        
        # Schedule next frame
        self.after(16, self.render_loop)
    
    def cleanup(self):
        """Clean up OpenGL resources"""
        if self.renderer is not None:
            self.renderer.cleanup()
            
        if USE_GLFW and hasattr(self, 'glfw_window') and self.has_gl_context:
            glfw.destroy_window(self.glfw_window)
            glfw.terminate() 