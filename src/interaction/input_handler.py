import tkinter as tk
from src.models.room import Room
from src.models.door import Door
from src.models.window import Window
from src.models.furniture import Furniture

class InputHandler:
    """
    Handle user input for interacting with the 3D scene
    """
    def __init__(self, canvas, camera, scene_manager, main_window=None):
        """
        Initialize the input handler
        
        Args:
            canvas: tkinter Canvas widget
            camera: Camera instance for view manipulation
            scene_manager: SceneManager instance
            main_window: MainWindow instance for UI updates
        """
        self.canvas = canvas
        self.camera = camera
        self.scene_manager = scene_manager
        self.main_window = main_window
        
        # Mouse state
        self.last_x = 0
        self.last_y = 0
        self.left_button_down = False
        self.right_button_down = False
        self.middle_button_down = False
        
        # Keyboard state
        self.shift_pressed = False
        
        # Interaction mode (select, move, rotate)
        self.mode = "select"
        
        # Selected object
        self.selected_object = None
        
        # Bind input events
        self.bind_events()
    
    def bind_events(self):
        """Bind input events to the canvas"""
        # Mouse button events
        self.canvas.bind("<ButtonPress-1>", self.on_left_mouse_down)
        self.canvas.bind("<ButtonRelease-1>", self.on_left_mouse_up)
        self.canvas.bind("<ButtonPress-2>", self.on_middle_mouse_down)
        self.canvas.bind("<ButtonRelease-2>", self.on_middle_mouse_up)
        self.canvas.bind("<ButtonPress-3>", self.on_right_mouse_down)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_mouse_up)
        
        # Mouse motion events
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
        # Mouse wheel events
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)  # Windows
        self.canvas.bind("<Button-4>", self.on_mouse_wheel)    # Linux scroll up
        self.canvas.bind("<Button-5>", self.on_mouse_wheel)    # Linux scroll down
        
        # Keyboard events
        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.bind("<KeyRelease>", self.on_key_release)
        
        # Make sure canvas can receive key events
        self.canvas.focus_set()
        
        # Store last clicked position for cycling through objects
        self.last_click_x = 0
        self.last_click_y = 0
    
    def set_mode(self, mode):
        """
        Set the current interaction mode
        
        Args:
            mode: Interaction mode ("select", "move", "rotate")
        """
        self.mode = mode
    
    def on_left_mouse_down(self, event):
        """
        Handle left mouse button press
        
        Args:
            event: Tkinter event
        """
        self.left_button_down = True
        self.last_x = event.x
        self.last_y = event.y
        
        # Store click position for potential cycling
        self.last_click_x = event.x
        self.last_click_y = event.y
        
        # Handle based on current mode
        if self.mode == "select":
            # Ray casting to select object
            selected = self.scene_manager.pick_object(event.x, event.y)
            if selected is not None:
                self.select_object(selected)
            else:
                self.deselect_object()
    
    def on_left_mouse_up(self, event):
        """
        Handle left mouse button release
        
        Args:
            event: Tkinter event
        """
        self.left_button_down = False
    
    def on_middle_mouse_down(self, event):
        """
        Handle middle mouse button press
        
        Args:
            event: Tkinter event
        """
        self.middle_button_down = True
        self.last_x = event.x
        self.last_y = event.y
    
    def on_middle_mouse_up(self, event):
        """
        Handle middle mouse button release
        
        Args:
            event: Tkinter event
        """
        self.middle_button_down = False
    
    def on_right_mouse_down(self, event):
        """
        Handle right mouse button press
        
        Args:
            event: Tkinter event
        """
        self.right_button_down = True
        self.last_x = event.x
        self.last_y = event.y
    
    def on_right_mouse_up(self, event):
        """
        Handle right mouse button release
        
        Args:
            event: Tkinter event
        """
        self.right_button_down = False
    
    def on_mouse_move(self, event):
        """
        Handle mouse movement
        
        Args:
            event: Tkinter event
        """
        delta_x = event.x - self.last_x
        delta_y = event.y - self.last_y
        
        if self.left_button_down:
            if self.mode == "select":
                # Camera orbit
                self.camera.orbit(delta_x, delta_y)
            elif self.mode == "move" and self.selected_object is not None:
                # Move selected object in XZ plane
                self.scene_manager.move_selected_object(delta_x * 0.01, 0, delta_y * 0.01)
            elif self.mode == "rotate" and self.selected_object is not None:
                # Rotation behavior depends on modifier keys
                if self.shift_pressed:
                    # Shift + drag: Rotate around X and Z axes
                    self.scene_manager.rotate_selected_object(delta_y * 0.5, 0, delta_x * 0.5)
                    rotation = self.selected_object.rotation
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating X: {rotation[0]:.1f}°, Z: {rotation[2]:.1f}°")
                else:
                    # Normal drag: Rotate around Y axis only
                    self.scene_manager.rotate_selected_object(0, delta_x * 0.5, 0)
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating Y-axis: {self.selected_object.rotation[1]:.1f}°")
        
        if self.right_button_down:
            # Pan camera
            self.camera.pan(delta_x * 0.01, -delta_y * 0.01)
        
        if self.middle_button_down:
            # Custom action (e.g., adjust height)
            if self.selected_object is not None and self.mode == "move":
                self.scene_manager.move_selected_object(0, delta_y * 0.01, 0)
        
        self.last_x = event.x
        self.last_y = event.y
    
    def on_mouse_wheel(self, event):
        """
        Handle mouse wheel scrolling
        
        Args:
            event: Tkinter event
        """
        # Different handling based on platform
        if event.num == 4:
            # Linux scroll up
            self.camera.zoom(1)
        elif event.num == 5:
            # Linux scroll down
            self.camera.zoom(-1)
        else:
            # Windows wheel
            delta = event.delta
            
            # Windows platform uses negative values for scrolling down
            if delta > 0:
                self.camera.zoom(1)
            else:
                self.camera.zoom(-1)
    
    def on_key_press(self, event):
        """
        Handle key press
        
        Args:
            event: Tkinter event
        """
        key = event.keysym.lower()
        
        # General shortcuts
        if key == "escape":
            self.deselect_object()
        elif key == "delete" and self.selected_object is not None:
            self.scene_manager.delete_selected_object()
            self.selected_object = None
        elif key == "tab":
            # Cycle through objects at the last clicked position
            next_obj = self.scene_manager.cycle_selection(self.last_click_x, self.last_click_y)
            if next_obj:
                self.select_object(next_obj)
        elif key == "c":
            # Alternative shortcut for cycling objects under cursor
            if hasattr(self.main_window, 'update_status'):
                self.main_window.update_status("Cycling through objects under cursor")
            # Get cursor position from last mouse position
            next_obj = self.scene_manager.cycle_selection(self.last_x, self.last_y)
            if next_obj:
                self.select_object(next_obj)
        
        # Camera controls
        if key == "r":
            self.camera.reset()
        
        # Object manipulation with arrow keys
        if self.selected_object is not None:
            # Position controls
            if key == "up":
                self.scene_manager.move_selected_object(0, 0, -0.1)
            elif key == "down":
                self.scene_manager.move_selected_object(0, 0, 0.1)
            elif key == "left":
                self.scene_manager.move_selected_object(-0.1, 0, 0)
            elif key == "right":
                self.scene_manager.move_selected_object(0.1, 0, 0)
            elif key == "page_up":
                self.scene_manager.move_selected_object(0, 0.1, 0)
            elif key == "page_down":
                self.scene_manager.move_selected_object(0, -0.1, 0)
            
            # Rotation controls with Shift key
            elif key == "shift_l" or key == "shift_r":
                # Store that shift is pressed
                self.shift_pressed = True
            
            # Rotation with shift + arrow keys or shift + rotation keys
            if hasattr(self, 'shift_pressed') and self.shift_pressed:
                rotation_amount = 15
                
                # Y-axis rotation
                if key == "left":
                    self.scene_manager.rotate_selected_object(0, -rotation_amount, 0)
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating Y-axis: {self.selected_object.rotation[1]}°")
                elif key == "right":
                    self.scene_manager.rotate_selected_object(0, rotation_amount, 0)
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating Y-axis: {self.selected_object.rotation[1]}°")
                
                # X-axis rotation
                elif key == "up":
                    self.scene_manager.rotate_selected_object(-rotation_amount, 0, 0)
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating X-axis: {self.selected_object.rotation[0]}°")
                elif key == "down":
                    self.scene_manager.rotate_selected_object(rotation_amount, 0, 0)
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating X-axis: {self.selected_object.rotation[0]}°")
                
                # Z-axis rotation
                elif key == "z":
                    self.scene_manager.rotate_selected_object(0, 0, -rotation_amount)
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating Z-axis: {self.selected_object.rotation[2]}°")
                elif key == "x":
                    self.scene_manager.rotate_selected_object(0, 0, rotation_amount)
                    if hasattr(self.main_window, 'update_status'):
                        self.main_window.update_status(f"Rotating Z-axis: {self.selected_object.rotation[2]}°")
    
    def on_key_release(self, event):
        """
        Handle key release
        
        Args:
            event: Tkinter event
        """
        key = event.keysym.lower()
        
        # Track shift key release
        if key == "shift_l" or key == "shift_r":
            self.shift_pressed = False
    
    def select_object(self, obj):
        """
        Select an object and provide visual/audio feedback
        
        Args:
            obj: Object to select
        """
        # Only process if this is a different object
        if self.selected_object != obj:
            self.selected_object = obj
            self.scene_manager.set_selected_object(obj)
            
            # Update UI if available
            if hasattr(self.main_window, 'sidebar'):
                self.main_window.sidebar.show_object_properties(obj)
            
            # Show status message with object details
            if hasattr(self.main_window, 'update_status'):
                if obj is not None:
                    # Format a nice message based on object type
                    cycling_msg = " (Tab to cycle through objects)" if self.are_objects_overlapping() else ""
                    rotation_msg = " | Set rotation in Properties tab or use Shift+Arrows/XZ keys"
                    
                    if isinstance(obj, Room):
                        self.main_window.update_status(f"Selected {obj.room_type} ({obj.width}m × {obj.length}m × {obj.height}m){cycling_msg}")
                    elif isinstance(obj, Door):
                        self.main_window.update_status(f"Selected {obj.door_type} ({obj.width}m × {obj.height}m){cycling_msg}{rotation_msg}")
                    elif isinstance(obj, Window):
                        self.main_window.update_status(f"Selected {obj.window_type} ({obj.width}m × {obj.height}m){cycling_msg}{rotation_msg}")
                    elif isinstance(obj, Furniture):
                        self.main_window.update_status(f"Selected {obj.furniture_type} ({obj.width}m × {obj.depth}m × {obj.height}m){cycling_msg}{rotation_msg}")
                    else:
                        self.main_window.update_status(f"Selected {obj.name}{cycling_msg}{rotation_msg}")
    
    def are_objects_overlapping(self):
        """Check if there might be other selectable objects near the current selection"""
        # Simple implementation - just check if we have more than 2 objects in the scene
        # In a real implementation, this would check for objects near the current selection point
        all_objects = self.scene_manager.get_all_objects()
        return len([obj for obj in all_objects if obj != self.scene_manager.room]) >= 2
    
    def deselect_object(self):
        """Deselect the currently selected object and provide feedback"""
        if self.selected_object is not None:
            self.selected_object = None
            self.scene_manager.set_selected_object(None)
            
            # Update UI if available
            if hasattr(self.main_window, 'sidebar'):
                self.main_window.sidebar.show_object_properties(None)
            
            # Update status
            if hasattr(self.main_window, 'update_status'):
                self.main_window.update_status("No object selected") 