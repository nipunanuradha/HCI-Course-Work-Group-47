import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import json
import numpy as np
from PIL import Image, ImageDraw
import random

class Toolbar(ttk.Frame):
    def __init__(self, parent, main_window):
        """
        Initialize the toolbar
        
        Args:
            parent: Parent tkinter widget
            main_window: MainWindow instance
        """
        ttk.Frame.__init__(self, parent, relief=tk.RAISED, borderwidth=1)
        
        self.parent = parent
        self.main_window = main_window
        self.scene_manager = main_window.scene_manager
        
        # Create toolbar buttons
        self.create_buttons()
    
    def create_buttons(self):
        """Create toolbar buttons"""
        # File operations
        file_frame = ttk.LabelFrame(self, text="File")
        file_frame.pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(file_frame, text="New", command=self.new_scene).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="Open", command=self.open_scene).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="Save", command=self.save_scene).pack(side=tk.LEFT, padx=2)
        ttk.Button(file_frame, text="Export", command=self.export_scene).pack(side=tk.LEFT, padx=2)
        
        # Edit operations
        edit_frame = ttk.LabelFrame(self, text="Edit")
        edit_frame.pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(edit_frame, text="Select", command=lambda: self.set_mode("select")).pack(side=tk.LEFT, padx=2)
        ttk.Button(edit_frame, text="Move", command=lambda: self.set_mode("move")).pack(side=tk.LEFT, padx=2)
        ttk.Button(edit_frame, text="Rotate", command=lambda: self.set_mode("rotate")).pack(side=tk.LEFT, padx=2)
        
        # View controls
        view_frame = ttk.LabelFrame(self, text="View")
        view_frame.pack(side=tk.LEFT, padx=5, pady=2)
        
        ttk.Button(view_frame, text="Reset View", command=self.reset_view).pack(side=tk.LEFT, padx=2)
        ttk.Button(view_frame, text="Top View", command=lambda: self.set_view("top")).pack(side=tk.LEFT, padx=2)
        ttk.Button(view_frame, text="Front View", command=lambda: self.set_view("front")).pack(side=tk.LEFT, padx=2)
        ttk.Button(view_frame, text="Side View", command=lambda: self.set_view("side")).pack(side=tk.LEFT, padx=2)
        
        # Help
        help_frame = ttk.Frame(self)
        help_frame.pack(side=tk.RIGHT, padx=5, pady=2)
        
        ttk.Button(help_frame, text="Help", command=self.show_help).pack(side=tk.RIGHT, padx=2)
    
    def new_scene(self):
        """Create a new scene"""
        if messagebox.askyesno("New Scene", "Are you sure you want to create a new scene? Any unsaved changes will be lost."):
            self.scene_manager.clear_scene()
            self.main_window.update_status("Created new scene")
    
    def open_scene(self):
        """Open a scene from file"""
        filename = filedialog.askopenfilename(
            title="Open Scene",
            filetypes=[("Scene Files", "*.json"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    scene_data = json.load(f)
                
                self.scene_manager.load_scene(scene_data)
                self.main_window.update_status(f"Opened scene from {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open scene: {str(e)}")
    
    def save_scene(self):
        """Save the scene to a file"""
        filename = filedialog.asksaveasfilename(
            title="Save Scene",
            defaultextension=".json",
            filetypes=[("Scene Files", "*.json"), ("All Files", "*.*")]
        )
        
        if filename:
            try:
                scene_data = self.scene_manager.save_scene()
                
                with open(filename, 'w') as f:
                    json.dump(scene_data, f, indent=2)
                
                self.main_window.update_status(f"Saved scene to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save scene: {str(e)}")
    
    def export_scene(self):
        """Export the scene to other formats"""
        # Create export window with options
        export_window = tk.Toplevel(self.main_window.master)
        export_window.title("Export Scene")
        export_window.geometry("400x300")
        export_window.transient(self.main_window.master)
        export_window.grab_set()
        
        ttk.Label(export_window, text="Export Options", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Create a frame for export options
        options_frame = ttk.Frame(export_window)
        options_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Export format selection
        format_frame = ttk.LabelFrame(options_frame, text="Export Format")
        format_frame.pack(fill=tk.X, pady=5)
        
        format_var = tk.StringVar(value="json")
        ttk.Radiobutton(format_frame, text="JSON Format (Scene Data)", value="json", 
                     variable=format_var).pack(anchor=tk.W, padx=20, pady=2)
        ttk.Radiobutton(format_frame, text="OBJ Format (3D Model)", value="obj", 
                     variable=format_var).pack(anchor=tk.W, padx=20, pady=2)
        ttk.Radiobutton(format_frame, text="PNG Image (Screenshot)", value="png", 
                     variable=format_var).pack(anchor=tk.W, padx=20, pady=2)
        
        # Export options
        options_label_frame = ttk.LabelFrame(options_frame, text="Export Settings")
        options_label_frame.pack(fill=tk.X, pady=5)
        
        # Include textures option
        textures_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_label_frame, text="Include Textures", 
                      variable=textures_var).pack(anchor=tk.W, padx=20, pady=2)
        
        # Export scale for OBJ
        scale_frame = ttk.Frame(options_label_frame)
        scale_frame.pack(fill=tk.X, padx=20, pady=2)
        ttk.Label(scale_frame, text="Scale:").pack(side=tk.LEFT)
        scale_var = tk.DoubleVar(value=1.0)
        scale_spinbox = ttk.Spinbox(scale_frame, from_=0.1, to=10.0, increment=0.1, 
                                  textvariable=scale_var, width=5)
        scale_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Export quality for PNG
        quality_frame = ttk.Frame(options_label_frame)
        quality_frame.pack(fill=tk.X, padx=20, pady=2)
        ttk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT)
        quality_var = tk.IntVar(value=90)
        quality_spinbox = ttk.Spinbox(quality_frame, from_=10, to=100, increment=10, 
                                    textvariable=quality_var, width=5)
        quality_spinbox.pack(side=tk.LEFT, padx=5)
        
        # Status label
        status_label = ttk.Label(export_window, text="")
        status_label.pack(pady=5)
        
        # Buttons
        button_frame = ttk.Frame(export_window)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=10)
        
        def do_export():
            export_format = format_var.get()
            
            # Get appropriate file extension and type description
            file_extensions = {
                "json": [("JSON Files", "*.json")],
                "obj": [("OBJ Files", "*.obj")],
                "png": [("PNG Images", "*.png")]
            }
            
            file_ext = file_extensions.get(export_format, [("All Files", "*.*")])
            
            # Ask for filename
            filename = filedialog.asksaveasfilename(
                title=f"Export as {export_format.upper()}",
                defaultextension=f".{export_format}",
                filetypes=file_ext + [("All Files", "*.*")]
            )
            
            if not filename:
                return
            
            try:
                if export_format == "json":
                    # Export as JSON (scene data)
                    scene_data = self.scene_manager.save_scene()
                    
                    # Add metadata
                    scene_data["metadata"] = {
                        "format": "3D Room Model",
                        "version": "1.0",
                        "description": "Exported from 3D Room and Furniture Modeling System"
                    }
                    
                    with open(filename, 'w') as f:
                        json.dump(scene_data, f, indent=2)
                    
                    status_label.config(text=f"Scene exported to {os.path.basename(filename)}")
                    self.main_window.update_status(f"Scene exported as JSON to {os.path.basename(filename)}")
                    
                elif export_format == "obj":
                    # Export as OBJ (requires implementation in the renderer)
                    # This would typically use the OpenGL renderer to export geometry
                    
                    # For demonstration, we'll create a simple OBJ file with basic geometry
                    from src.models.room import Room
                    scale = scale_var.get()
                    
                    with open(filename, 'w') as f:
                        # OBJ header
                        f.write("# Exported from 3D Room and Furniture Modeling System\n")
                        f.write("# Format: OBJ\n\n")
                        
                        # Add geometry for each object
                        vertex_offset = 1  # OBJ indices start at 1
                        
                        for obj in self.scene_manager.get_all_objects():
                            f.write(f"# Object: {obj.name}\n")
                            
                            # Get position and dimensions
                            pos = obj.position
                            
                            # Different geometry based on object type
                            if isinstance(obj, Room):
                                # Room as a box
                                width = obj.width * scale
                                length = obj.length * scale
                                height = obj.height * scale
                                
                                # Create vertices for a box
                                # Bottom vertices
                                f.write(f"v {-width/2 + pos[0]} {0 + pos[1]} {-length/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {0 + pos[1]} {-length/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {0 + pos[1]} {length/2 + pos[2]}\n")
                                f.write(f"v {-width/2 + pos[0]} {0 + pos[1]} {length/2 + pos[2]}\n")
                                
                                # Top vertices
                                f.write(f"v {-width/2 + pos[0]} {height + pos[1]} {-length/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {height + pos[1]} {-length/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {height + pos[1]} {length/2 + pos[2]}\n")
                                f.write(f"v {-width/2 + pos[0]} {height + pos[1]} {length/2 + pos[2]}\n")
                                
                                # Define faces (using relative indices)
                                # Bottom face
                                f.write(f"f {vertex_offset} {vertex_offset+1} {vertex_offset+2} {vertex_offset+3}\n")
                                
                                # Side faces
                                f.write(f"f {vertex_offset} {vertex_offset+4} {vertex_offset+7} {vertex_offset+3}\n")
                                f.write(f"f {vertex_offset+1} {vertex_offset+5} {vertex_offset+6} {vertex_offset+2}\n")
                                f.write(f"f {vertex_offset} {vertex_offset+1} {vertex_offset+5} {vertex_offset+4}\n")
                                f.write(f"f {vertex_offset+3} {vertex_offset+2} {vertex_offset+6} {vertex_offset+7}\n")
                                
                                # Top face
                                f.write(f"f {vertex_offset+4} {vertex_offset+5} {vertex_offset+6} {vertex_offset+7}\n")
                                
                                vertex_offset += 8
                            else:
                                # Other objects as simple boxes based on their dimensions
                                width = depth = height = 0.5  # Default
                                
                                if hasattr(obj, 'width'):
                                    width = obj.width * scale
                                if hasattr(obj, 'depth'):
                                    depth = obj.depth * scale
                                elif hasattr(obj, 'length'):
                                    depth = obj.length * scale
                                if hasattr(obj, 'height'):
                                    height = obj.height * scale
                                
                                # Create vertices for a box
                                # Bottom vertices
                                f.write(f"v {-width/2 + pos[0]} {-height/2 + pos[1]} {-depth/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {-height/2 + pos[1]} {-depth/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {-height/2 + pos[1]} {depth/2 + pos[2]}\n")
                                f.write(f"v {-width/2 + pos[0]} {-height/2 + pos[1]} {depth/2 + pos[2]}\n")
                                
                                # Top vertices
                                f.write(f"v {-width/2 + pos[0]} {height/2 + pos[1]} {-depth/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {height/2 + pos[1]} {-depth/2 + pos[2]}\n")
                                f.write(f"v {width/2 + pos[0]} {height/2 + pos[1]} {depth/2 + pos[2]}\n")
                                f.write(f"v {-width/2 + pos[0]} {height/2 + pos[1]} {depth/2 + pos[2]}\n")
                                
                                # Define faces (using relative indices)
                                # Bottom face
                                f.write(f"f {vertex_offset} {vertex_offset+1} {vertex_offset+2} {vertex_offset+3}\n")
                                
                                # Side faces
                                f.write(f"f {vertex_offset} {vertex_offset+4} {vertex_offset+7} {vertex_offset+3}\n")
                                f.write(f"f {vertex_offset+1} {vertex_offset+5} {vertex_offset+6} {vertex_offset+2}\n")
                                f.write(f"f {vertex_offset} {vertex_offset+1} {vertex_offset+5} {vertex_offset+4}\n")
                                f.write(f"f {vertex_offset+3} {vertex_offset+2} {vertex_offset+6} {vertex_offset+7}\n")
                                
                                # Top face
                                f.write(f"f {vertex_offset+4} {vertex_offset+5} {vertex_offset+6} {vertex_offset+7}\n")
                                
                                vertex_offset += 8
                                
                            f.write("\n")  # Add space between objects
                    
                    status_label.config(text=f"Scene exported to {os.path.basename(filename)}")
                    self.main_window.update_status(f"Scene exported as OBJ to {os.path.basename(filename)}")
                    
                elif export_format == "png":
                    # Export as PNG screenshot
                    # This would capture the OpenGL frame
                    try:
                        from PIL import Image, ImageDraw
                        import random
                        
                        # Get canvas dimensions
                        canvas = self.main_window.opengl_frame.canvas
                        width = canvas.winfo_width()
                        height = canvas.winfo_height()
                        
                        # Create an image to hold the 3D scene
                        img = Image.new('RGB', (width, height), color=(240, 240, 240))
                        draw = ImageDraw.Draw(img)
                        
                        # Try to get actual screenshot from OpenGL canvas if possible
                        try:
                            # First try using PIL's ImageGrab if available
                            from PIL import ImageGrab
                            
                            # Request OpenGL frame to update and render
                            self.main_window.opengl_frame.render_loop()
                            
                            # Use the tkinter canvas to take a screenshot
                            x = canvas.winfo_rootx()
                            y = canvas.winfo_rooty()
                            
                            # Use PIL to capture the screen region
                            screenshot = ImageGrab.grab(bbox=(x, y, x+width, y+height))
                            img = screenshot
                        except (NameError, ImportError, AttributeError) as e:
                            # If PIL's ImageGrab fails or isn't available
                            # Create a representative render of the scene with basic shapes
                            
                            # Get background gradient
                            for y in range(height):
                                r = int(240 * (1 - y/height))
                                g = int(240 * (1 - y/height))
                                b = int(255 * (1 - y/height) + 200 * (y/height))
                                draw.line([(0, y), (width, y)], fill=(r, g, b))
                            
                            # Draw floor grid
                            grid_size = 20
                            grid_spacing = width // grid_size
                            for i in range(grid_size + 1):
                                # Horizontal lines
                                y_pos = height//2 + i * grid_spacing // 2
                                if y_pos < height:
                                    draw.line([(0, y_pos), (width, y_pos)], fill=(180, 180, 180), width=1)
                                
                                # Vertical lines
                                x_pos = i * grid_spacing
                                draw.line([(x_pos, height//2), (x_pos, height)], fill=(180, 180, 180), width=1)
                            
                            # Draw representation of objects in the scene
                            objects = self.scene_manager.get_all_objects()
                            
                            # Draw room outline
                            room = None
                            for obj in objects:
                                if obj.__class__.__name__ == "Room":
                                    room = obj
                                    break
                                    
                            if room:
                                # Draw room as a perspective rectangle
                                room_width = min(width-40, room.width * 30)
                                room_height = min(height//3, room.height * 20)
                                
                                # Simple perspective box for room
                                center_x = width // 2
                                center_y = height // 2
                                
                                # Room floor
                                draw.polygon([
                                    (center_x - room_width//2, center_y + room_height),
                                    (center_x + room_width//2, center_y + room_height),
                                    (center_x + room_width//3, center_y),
                                    (center_x - room_width//3, center_y)
                                ], outline=(0, 0, 0), fill=(220, 220, 220))
                                
                                # Room back wall
                                draw.polygon([
                                    (center_x - room_width//3, center_y),
                                    (center_x + room_width//3, center_y),
                                    (center_x + room_width//3, center_y - room_height),
                                    (center_x - room_width//3, center_y - room_height)
                                ], outline=(0, 0, 0), fill=(200, 200, 200))
                                
                                # Room left wall
                                draw.polygon([
                                    (center_x - room_width//2, center_y + room_height),
                                    (center_x - room_width//3, center_y),
                                    (center_x - room_width//3, center_y - room_height),
                                    (center_x - room_width//2, center_y)
                                ], outline=(0, 0, 0), fill=(180, 180, 180))
                                
                                # Room right wall
                                draw.polygon([
                                    (center_x + room_width//2, center_y + room_height),
                                    (center_x + room_width//3, center_y),
                                    (center_x + room_width//3, center_y - room_height),
                                    (center_x + room_width//2, center_y)
                                ], outline=(0, 0, 0), fill=(160, 160, 160))
                            
                            # Draw furniture, doors, and windows
                            for obj in objects:
                                if obj.__class__.__name__ in ["Door", "Window", "Furniture"]:
                                    # Random color based on object type
                                    if obj.__class__.__name__ == "Door":
                                        color = (139, 69, 19)  # Brown
                                    elif obj.__class__.__name__ == "Window":
                                        color = (173, 216, 230)  # Light blue
                                    else:
                                        # Random color for furniture
                                        r = random.randint(50, 200)
                                        g = random.randint(50, 200)
                                        b = random.randint(50, 200)
                                        color = (r, g, b)
                                    
                                    # Position based on object's position relative to room
                                    pos = obj.position
                                    if room:
                                        rel_x = (pos[0] + room.width/2) / room.width  # 0 to 1
                                        rel_z = (pos[2] + room.length/2) / room.length  # 0 to 1
                                        
                                        obj_x = center_x - room_width//3 + rel_x * (room_width//1.5)
                                        obj_y = center_y + room_height - rel_z * room_height * 2
                                        
                                        # Get object dimensions
                                        width_attr = getattr(obj, 'width', 0.5) * 30
                                        height_attr = getattr(obj, 'height', 0.5) * 20
                                        
                                        # Draw a simple representation
                                        draw.rectangle([
                                            (obj_x - width_attr/2, obj_y - height_attr/2),
                                            (obj_x + width_attr/2, obj_y + height_attr/2)
                                        ], outline=(0, 0, 0), fill=color)
                            
                            # Add text label for exported image
                            try:
                                draw.text((10, 10), "3D Room and Furniture Model", fill=(0, 0, 0))
                            except Exception:
                                # Some systems might not have default font support
                                pass
                        
                        # Save the image
                        img.save(filename, quality=quality_var.get())
                        
                        status_label.config(text=f"Screenshot saved to {os.path.basename(filename)}")
                        self.main_window.update_status(f"Screenshot saved to {os.path.basename(filename)}")
                        
                    except ImportError:
                        messagebox.showerror("Error", "PIL (Pillow) library is required for image export")
                        status_label.config(text="Error: PIL library not found")
                
                # Show success message
                messagebox.showinfo("Export Complete", f"Scene exported successfully to {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export: {str(e)}")
                status_label.config(text=f"Error: {str(e)}")
        
        ttk.Button(button_frame, text="Export", command=do_export).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=export_window.destroy).pack(side=tk.RIGHT, padx=10)
    
    def reset_view(self):
        """Reset the camera view"""
        camera = self.main_window.opengl_frame.camera
        camera.reset()
        self.main_window.update_status("View reset")
    
    def set_view(self, view_type):
        """Set predefined camera view"""
        camera = self.main_window.opengl_frame.camera
        
        if view_type == "top":
            camera.position = np.array([0, 5, 0], dtype=np.float32)
            camera.target = np.array([0, 0, 0], dtype=np.float32)
            camera.up = np.array([0, 0, -1], dtype=np.float32)
            self.main_window.update_status("Top view")
        elif view_type == "front":
            camera.position = np.array([0, 0, 5], dtype=np.float32)
            camera.target = np.array([0, 0, 0], dtype=np.float32)
            camera.up = np.array([0, 1, 0], dtype=np.float32)
            self.main_window.update_status("Front view")
        elif view_type == "side":
            camera.position = np.array([5, 0, 0], dtype=np.float32)
            camera.target = np.array([0, 0, 0], dtype=np.float32)
            camera.up = np.array([0, 1, 0], dtype=np.float32)
            self.main_window.update_status("Side view")
    
    def set_mode(self, mode):
        """Set the current interaction mode"""
        input_handler = self.main_window.opengl_frame.input_handler
        input_handler.set_mode(mode)
        self.main_window.update_status(f"Mode: {mode.capitalize()}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
        3D Room and Furniture Modeling System
        
        Controls:
        - Left-click & drag: Rotate camera
        - Right-click & drag: Pan camera
        - Scroll wheel: Zoom in/out
        - Ctrl + click: Select object
        - Delete key: Delete selected object
        - Arrow keys: Move selected object
        - R + Arrow keys: Rotate selected object
        
        Modes:
        - Select: Click to select objects
        - Move: Click and drag to move objects
        - Rotate: Click and drag to rotate objects
        """
        
        help_window = tk.Toplevel(self.main_window.master)
        help_window.title("Help")
        help_window.geometry("400x300")
        help_window.transient(self.main_window.master)
        
        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)
        
        ttk.Button(help_window, text="Close", command=help_window.destroy).pack(pady=10) 