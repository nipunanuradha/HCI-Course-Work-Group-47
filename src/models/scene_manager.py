import os
import json
import numpy as np
import uuid

# Add missing import for the methods that use it
import glm

from src.models.room import Room
from src.models.door import Door
from src.models.window import Window
from src.models.furniture import Furniture

class SceneManager:
    """
    Manages all objects in the 3D scene
    """
    def __init__(self):
        """Initialize the scene manager"""
        self.room = None
        self.doors = []  # List to store door objects
        self.windows = []  # List to store window objects
        self.furniture = []  # List to store furniture objects
        self.selected_object = None
        self.last_id = 0
        
        # Dictionary to track objects by ID
        self.object_map = {}
        
        # History tracking for undo/redo
        self.history = []
        self.history_index = -1
        self.max_history = 20  # Maximum number of history states to keep
        
        # Set default room
        self.set_room("Living Room", 5.0, 6.0, 2.5)
        
        # Clear history after initial setup
        self.history.clear()
        self.history_index = -1
    
    def set_room(self, name, width, length, height, room_type="bedroom"):
        """
        Set the room for the scene
        
        Args:
            name (str): Name of the room
            width (float): Width of the room in meters
            length (float): Length of the room in meters
            height (float): Height of the room in meters
            room_type (str): Type of the room (default: "bedroom")
            
        Returns:
            Room: The created room object
        """
        # Save current state for undo
        if self.room:
            self._save_state(f"Change Room to {name}")
            
        room_id = str(uuid.uuid4())
        self.room = Room(
            room_id=room_id,
            name=name,
            room_type=room_type,
            width=width,
            length=length,
            height=height,
            position=[0, 0, 0],
            rotation=[0, 0, 0]
        )
        
        # Set room colors to light gray
        self.set_room_color("wall", "#CCCCCC", [0.8, 0.8, 0.8])
        
        return self.room
    
    def add_door(self, door_type, width, height, position=None, rotation=None, thickness=0.05):
        """
        Add a door to the scene
        
        Args:
            door_type: Type of door (single, double, sliding)
            width: Door width
            height: Door height
            position: Position (x, y, z)
            rotation: Rotation in degrees (x, y, z)
            thickness: Door thickness in meters
            
        Returns:
            Door object that was added
        """
        # Save state for undo
        self._save_state(f"Add {door_type}")
        
        # Create default position if not provided
        if position is None:
            # Place the door on one of the walls
            if self.room is not None:
                room_width = self.room.width
                room_length = self.room.length
                position = [-room_width/2, height/2, 0]  # Default on west wall
                rotation = [0, 90, 0]  # Facing inward
        
        # Create default rotation if not provided
        if rotation is None:
            rotation = [0, 0, 0]
        
        # Create door object
        door = Door(
            door_id=f"door_{len(self.doors)}",
            name=f"{door_type} {len(self.doors) + 1}",
            position=position,
            rotation=rotation,
            door_type=door_type,
            width=width,
            height=height
        )
        
        # Set the thickness property
        door.thickness = thickness
        
        # Add to scene
        self.add_object(door)
        
        return door
    
    def add_window(self, window_type, width, height, position=None, rotation=None):
        """
        Add a window to the scene
        
        Args:
            window_type: Type of window (single, double, sliding, bay)
            width: Window width
            height: Window height
            position: Position (x, y, z)
            rotation: Rotation in degrees (x, y, z)
            
        Returns:
            Window object that was added
        """
        # Save state for undo
        self._save_state(f"Add {window_type}")
        
        # Create default position if not provided
        if position is None:
            # Place the window on one of the walls
            if self.room is not None:
                room_width = self.room.width
                room_length = self.room.length
                position = [0, self.room.height/2, -room_length/2]  # Default on north wall
                rotation = [0, 0, 0]  # Facing outward
        
        # Create default rotation if not provided
        if rotation is None:
            rotation = [0, 0, 0]
        
        # Create window object
        window = Window(
            window_id=f"window_{len(self.windows)}",
            name=f"{window_type} {len(self.windows) + 1}",
            position=position,
            rotation=rotation,
            window_type=window_type,
            width=width,
            height=height
        )
        
        # Add to scene
        self.add_object(window)
        
        return window
    
    def add_furniture(self, furniture_type, width, depth, height, position=None, rotation=None, category=None):
        """
        Add furniture to the scene
        
        Args:
            furniture_type: Type of furniture
            width: Furniture width
            depth: Furniture depth
            height: Furniture height
            position: Position (x, y, z)
            rotation: Rotation in degrees (x, y, z)
            category: Furniture category (optional, will be derived from furniture_type if None)
            
        Returns:
            Furniture object that was added
        """
        # Save state for undo
        self._save_state(f"Add {furniture_type}")
        
        # Create default position if not provided
        if position is None:
            # Place furniture on the floor in the center of the room
            position = [0, height/2, 0]
        
        # Create default rotation if not provided
        if rotation is None:
            rotation = [0, 0, 0]
        
        # Determine category if not provided
        if category is None:
            # Derive category from furniture type
            if furniture_type in ["Dining Chair", "Office Chair", "Armchair"]:
                category = "Chairs"
            elif furniture_type in ["Dining Table", "Coffee Table", "Desk"]:
                category = "Tables"
            elif furniture_type in ["2-Seater Sofa", "3-Seater Sofa", "L-Shaped Sofa"]:
                category = "Sofas"
            elif furniture_type in ["Single Bed", "Double Bed", "King Size Bed"]:
                category = "Beds"
            elif furniture_type in ["Single Door Cupboard", "Double Door Cupboard", "Sliding Door Cupboard"]:
                category = "Cupboards"
            else:
                category = "Miscellaneous"
        
        # Create furniture object
        furniture = Furniture(
            furniture_id=f"furniture_{len(self.furniture)}",
            name=f"{furniture_type} {len(self.furniture) + 1}",
            position=position,
            rotation=rotation,
            furniture_type=furniture_type,
            category=category,
            width=width,
            depth=depth,
            height=height
        )
        
        # Add to scene
        self.add_object(furniture)
        
        return furniture
    
    def _get_furniture_dimensions(self, furniture_type):
        """
        Get default dimensions for furniture type
        
        Args:
            furniture_type: Type of furniture
            
        Returns:
            dict: Dictionary with width, depth and height
        """
        # Default dimensions for various furniture types (in meters)
        furniture_dimensions = {
            # Chairs
            "Dining Chair": {"width": 0.5, "depth": 0.5, "height": 0.9},
            "Office Chair": {"width": 0.6, "depth": 0.6, "height": 1.1},
            "Armchair": {"width": 0.8, "depth": 0.8, "height": 0.8},
            
            # Tables
            "Dining Table": {"width": 1.5, "depth": 0.9, "height": 0.75},
            "Coffee Table": {"width": 1.0, "depth": 0.6, "height": 0.45},
            "Desk": {"width": 1.2, "depth": 0.6, "height": 0.75},
            
            # Sofas
            "2-Seater Sofa": {"width": 1.5, "depth": 0.85, "height": 0.7},
            "3-Seater Sofa": {"width": 2.1, "depth": 0.85, "height": 0.7},
            "L-Shaped Sofa": {"width": 2.5, "depth": 2.0, "height": 0.7},
            
            # Beds
            "Single Bed": {"width": 0.9, "depth": 2.0, "height": 0.5},
            "Double Bed": {"width": 1.4, "depth": 2.0, "height": 0.5},
            "King Size Bed": {"width": 1.8, "depth": 2.0, "height": 0.5},
            
            # Cupboards
            "Single Door Cupboard": {"width": 0.6, "depth": 0.5, "height": 2.0},
            "Double Door Cupboard": {"width": 1.2, "depth": 0.5, "height": 2.0},
            "Sliding Door Cupboard": {"width": 1.5, "depth": 0.6, "height": 2.0},
        }
        
        # Return dimensions or default if not found
        if furniture_type in furniture_dimensions:
            return furniture_dimensions[furniture_type]
        else:
            return {"width": 1.0, "depth": 1.0, "height": 1.0}
    
    def get_all_objects(self):
        """
        Get all objects in the scene
        
        Returns:
            List of all objects in the scene
        """
        all_objects = []
        
        # Add room
        if self.room is not None:
            all_objects.append(self.room)
        
        # Add doors
        all_objects.extend(self.doors)
        
        # Add windows
        all_objects.extend(self.windows)
        
        # Add furniture
        all_objects.extend(self.furniture)
        
        return all_objects
    
    def get_object_by_id(self, object_id):
        """
        Get object by ID
        
        Args:
            object_id: UUID of the object
            
        Returns:
            Object or None
        """
        return self.object_map.get(object_id)
    
    def pick_object(self, screen_x, screen_y, cycle_selection=False, current_object=None):
        """
        Pick object using ray casting with support for cycling through overlapping objects
        
        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate
            cycle_selection: If True, will cycle to the next object if multiple objects are in the same area
            current_object: Currently selected object (used for cycling)
            
        Returns:
            Object or None
        """
        # In a real implementation, this would perform ray casting from the screen coordinates
        # through the camera's view frustum and into the 3D scene.
        
        # Get all objects in the scene
        all_objects = self.get_all_objects()
        
        # Filter out the room (optional) and sort by distance from camera
        pickable_objects = [obj for obj in all_objects if obj != self.room]
        
        # If no objects to pick, return None
        if not pickable_objects:
            return None
            
        # If cycling through selection and we have a current object
        if cycle_selection and current_object in pickable_objects:
            # Find the current object's index
            current_index = pickable_objects.index(current_object)
            # Select the next object (wrap around if at the end)
            next_index = (current_index + 1) % len(pickable_objects)
            return pickable_objects[next_index]
            
        # For non-cycling selection, return the first pickable object
        # In a real implementation, this would calculate which objects
        # are actually under the cursor via raycasting, then return them in order
        # of distance from the camera (nearest first)
        for obj in pickable_objects:
            if hasattr(obj, 'position'):
                # Here we would check if the ray intersects this object
                # For testing, just return it
                return obj
        
        return None
        
    def cycle_selection(self, screen_x, screen_y):
        """
        Cycle through objects at the given screen position
        
        Args:
            screen_x: Screen X coordinate
            screen_y: Screen Y coordinate
            
        Returns:
            Next object in selection cycle or None
        """
        # Get the next object in the cycle
        next_obj = self.pick_object(screen_x, screen_y, cycle_selection=True, current_object=self.selected_object)
        
        # Set as selected
        if next_obj:
            self.set_selected_object(next_obj)
            
        return next_obj
    
    def set_selected_object(self, obj):
        """
        Set the currently selected object
        
        Args:
            obj: Object to select
        """
        # Clear selection state on previously selected object
        if self.selected_object and hasattr(self.selected_object, 'is_selected'):
            self.selected_object.is_selected = False
            
        # Set new selected object
        self.selected_object = obj
        
        # Mark the object as selected for visual highlighting
        if obj and hasattr(obj, 'is_selected'):
            obj.is_selected = True
        
        # We could also trigger a sound effect or other feedback here
    
    def delete_selected_object(self):
        """
        Delete the currently selected object
        
        Returns:
            bool: True if successful
        """
        if self.selected_object is None:
            return False
        
        # Can't delete the room
        if self.selected_object == self.room:
            return False
        
        # Save state for undo before deleting
        self._save_state(f"Delete {self.selected_object.name}")
        
        # Remove from collections
        if isinstance(self.selected_object, Door):
            if self.selected_object in self.doors:
                self.doors.remove(self.selected_object)
        elif isinstance(self.selected_object, Window):
            if self.selected_object in self.windows:
                self.windows.remove(self.selected_object)
        elif isinstance(self.selected_object, Furniture):
            if self.selected_object in self.furniture:
                self.furniture.remove(self.selected_object)
        
        # Remove from objects dictionary
        object_id = self.selected_object.get_id()
        if object_id in self.object_map:
            del self.object_map[object_id]
            self.selected_object = None
            return True
        
        return False
    
    def move_selected_object(self, dx, dy, dz):
        """
        Move the selected object
        
        Args:
            dx: Change in X position
            dy: Change in Y position
            dz: Change in Z position
            
        Returns:
            bool: True if successful
        """
        if self.selected_object is None or self.selected_object == self.room:
            return False
        
        # Get current position
        current_pos = self.selected_object.position
        
        # Calculate new position - use numpy array instead of glm.vec3
        new_pos = np.array([
            current_pos[0] + dx,
            current_pos[1] + dy,
            current_pos[2] + dz
        ], dtype=np.float32)
        
        # Check if new position is within room bounds (with some margin)
        margin = 0.1
        
        if self.room:
            half_width = self.room.width / 2 - margin
            half_length = self.room.length / 2 - margin
            max_height = self.room.height - margin
            
            # Clamp position to room bounds - use numpy functions
            new_pos[0] = max(-half_width, min(half_width, new_pos[0]))
            new_pos[1] = max(0, min(max_height, new_pos[1]))
            new_pos[2] = max(-half_length, min(half_length, new_pos[2]))
        
        # Update position
        self.selected_object.position = new_pos
        
        # Save state for undo after moving
        self._save_state(f"Move {self.selected_object.name}")
        
        return True
    
    def rotate_selected_object(self, dx, dy, dz):
        """
        Rotate the selected object
        
        Args:
            dx: Change in X rotation (degrees)
            dy: Change in Y rotation (degrees)
            dz: Change in Z rotation (degrees)
            
        Returns:
            bool: True if successful
        """
        if self.selected_object is None or self.selected_object == self.room:
            return False
        
        # Get current rotation
        current_rot = self.selected_object.rotation
        
        # Calculate new rotation - use numpy array instead of glm.vec3
        new_rot = np.array([
            (current_rot[0] + dx) % 360,
            (current_rot[1] + dy) % 360,
            (current_rot[2] + dz) % 360
        ], dtype=np.float32)
        
        # Update rotation
        self.selected_object.rotation = new_rot
        
        # Save state for undo after rotating
        self._save_state(f"Rotate {self.selected_object.name}")
        
        return True
    
    def set_selected_object_position(self, x, y, z):
        """
        Set the position of the selected object
        
        Args:
            x: X position
            y: Y position
            z: Z position
            
        Returns:
            bool: True if successful
        """
        if self.selected_object is None or self.selected_object == self.room:
            return False
        
        # Save current position for comparison
        old_pos = self.selected_object.position.copy()
        
        # Update position
        self.selected_object.position = np.array([x, y, z], dtype=np.float32)
        
        # Save state for undo if position changed significantly
        if np.linalg.norm(old_pos - self.selected_object.position) > 0.01:
            self._save_state(f"Move {self.selected_object.name}")
        
        return True
    
    def set_selected_object_rotation(self, x, y, z):
        """
        Set the rotation of the selected object
        
        Args:
            x: X rotation (degrees)
            y: Y rotation (degrees)
            z: Z rotation (degrees)
            
        Returns:
            bool: True if successful
        """
        if self.selected_object is None or self.selected_object == self.room:
            return False
        
        # Save current rotation for comparison
        old_rot = self.selected_object.rotation.copy()
        
        # Update rotation
        self.selected_object.rotation = np.array([x, y, z], dtype=np.float32)
        
        # Save state for undo if rotation changed significantly
        if np.linalg.norm(old_rot - self.selected_object.rotation) > 0.1:
            self._save_state(f"Rotate {self.selected_object.name}")
        
        return True
    
    def clear_scene(self):
        """Clear all objects from the scene"""
        # Save state for undo
        self._save_state("Clear Scene")
        
        self.doors.clear()
        self.windows.clear()
        self.furniture.clear()
        self.object_map.clear()
        self.selected_object = None
        self.last_id = 0
        
        # Create a default empty room
        self.set_room("Empty Room", 5.0, 5.0, 2.5)
    
    def save_scene(self):
        """
        Save the scene to a dictionary
        
        Returns:
            dict: Scene data
        """
        scene_data = {
            "objects": {}
        }
        
        # Save all objects
        for obj_id, obj in self.object_map.items():
            scene_data["objects"][obj_id] = obj.to_dict()
        
        return scene_data
    
    def load_scene(self, scene_data):
        """
        Load scene from dictionary
        
        Args:
            scene_data: Scene data
            
        Returns:
            bool: True if successful
        """
        try:
            # Clear current scene
            self.clear_scene()
            
            # Reset room reference
            self.room = None
            
            # Load objects
            object_data = scene_data.get("objects", {})
            
            for obj_id, data in object_data.items():
                obj_type = data.get("type")
                
                if obj_type == "Room":
                    # Create room
                    self.room = Room.from_dict(data)
                    self.object_map[obj_id] = self.room
                    
                elif obj_type == "Door":
                    # Create door
                    door = Door.from_dict(data)
                    self.object_map[obj_id] = door
                    self.doors.append(door)
                    
                elif obj_type == "Window":
                    # Create window
                    window = Window.from_dict(data)
                    self.object_map[obj_id] = window
                    self.windows.append(window)
                    
                elif obj_type == "Furniture":
                    # Create furniture
                    furniture = Furniture.from_dict(data)
                    self.object_map[obj_id] = furniture
                    self.furniture.append(furniture)
            
            # If no room was loaded, create default room
            if self.room is None:
                self.set_room("Living Room", 5.0, 6.0, 2.5)
            
            return True
            
        except Exception as e:
            print(f"Error loading scene: {e}")
            # Create default room if loading failed
            self.clear_scene()
            return False
    
    def add_object(self, obj):
        """
        Add an object to the scene
        
        Args:
            obj: Object to add
        """
        object_id = str(self.last_id)
        self.last_id += 1
        
        if hasattr(obj, '_id'):
            obj._id = object_id
        
        # Add to appropriate collection based on type
        if isinstance(obj, Door):
            self.doors.append(obj)
            print(f"Added door: {obj.door_type}, {obj.width}x{obj.height}")
        elif isinstance(obj, Window):
            self.windows.append(obj)
            print(f"Added window: {obj.window_type}, {obj.width}x{obj.height}")
        elif isinstance(obj, Furniture):
            self.furniture.append(obj)
            print(f"Added furniture: {obj.furniture_type}")
        
        # Add to object map for lookup by ID
        self.object_map[object_id] = obj
        
        return object_id
    
    def remove_object(self, object_id):
        """
        Remove an object from the scene
        
        Args:
            object_id: ID of object to remove
        """
        if object_id in self.object_map:
            obj = self.object_map[object_id]
            
            # Remove from the appropriate collection
            if isinstance(obj, Door):
                if obj in self.doors:
                    self.doors.remove(obj)
            elif isinstance(obj, Window):
                if obj in self.windows:
                    self.windows.remove(obj)
            elif isinstance(obj, Furniture):
                if obj in self.furniture:
                    self.furniture.remove(obj)
            
            # Remove from object map
            del self.object_map[object_id]
            
            # If selected object was removed, deselect
            if self.selected_object is obj:
                self.selected_object = None 
    
    def delete_object(self, object_id):
        """
        Delete an object from the scene by its ID
        
        Args:
            object_id: ID of the object to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        if object_id not in self.object_map:
            return False
            
        obj = self.object_map[object_id]
        
        # Can't delete the room
        if obj == self.room:
            return False
            
        # Save state for undo before deleting
        self._save_state(f"Delete {obj.name}")
        
        # Remove the object
        self.remove_object(object_id)
        
        return True
    
    # History management methods
    def _save_state(self, description=""):
        """
        Save the current state to history
        
        Args:
            description: Description of the state change
        """
        # Get current scene state
        scene_data = self.save_scene()
        scene_data["description"] = description
        
        # If we're not at the end of the history, truncate the future history
        if self.history_index < len(self.history) - 1:
            self.history = self.history[:self.history_index + 1]
        
        # Add the new state to history
        self.history.append(scene_data)
        self.history_index = len(self.history) - 1
        
        # Enforce history size limit
        if len(self.history) > self.max_history:
            # Remove the oldest state
            self.history.pop(0)
            self.history_index -= 1
    
    def can_undo(self):
        """Check if undo is available"""
        return self.history_index > 0
    
    def can_redo(self):
        """Check if redo is available"""
        return self.history_index < len(self.history) - 1
    
    def undo(self):
        """
        Undo the last action
        
        Returns:
            str: Description of the undone action, or empty if failed
        """
        if not self.can_undo():
            return ""
        
        # Decrement the history index
        self.history_index -= 1
        
        # Get the previous state
        prev_state = self.history[self.history_index]
        
        # Restore that state
        self.load_scene(prev_state)
        
        # Return the description of what was undone
        next_state = self.history[self.history_index + 1]
        return next_state.get("description", "Unknown action")
    
    def redo(self):
        """
        Redo the last undone action
        
        Returns:
            str: Description of the redone action, or empty if failed
        """
        if not self.can_redo():
            return ""
        
        # Increment the history index
        self.history_index += 1
        
        # Get the next state
        next_state = self.history[self.history_index]
        
        # Restore that state
        self.load_scene(next_state)
        
        # Return the description of what was redone
        return next_state.get("description", "Unknown action")
    
    # Object selection and interaction methods
    def handle_mouse_click(self, x, y, ctrl_pressed=False):
        """
        Handle mouse click for object selection
        
        Args:
            x: X screen coordinate
            y: Y screen coordinate
            ctrl_pressed: Whether Ctrl key is pressed
            
        Returns:
            bool: True if an object was selected
        """
        # Perform ray casting to find object under cursor
        hit_object = self.pick_object(x, y)
        
        if hit_object:
            if ctrl_pressed:
                # With Ctrl pressed, select the object
                self.set_selected_object(hit_object)
                return True
            else:
                # Without Ctrl, just perform regular click action based on current mode
                self.set_selected_object(hit_object)
                return True
        else:
            # If clicking on empty space without Ctrl, deselect
            if not ctrl_pressed:
                self.set_selected_object(None)
            
        return False
    
    def handle_key_press(self, key):
        """
        Handle key press events
        
        Args:
            key: Key code or name
            
        Returns:
            bool: True if the key was handled
        """
        # Delete key - delete selected object
        if key == 'Delete':
            return self.delete_selected_object()
            
        # Arrow keys - move selected object
        if key.startswith('Arrow'):
            direction = key.replace('Arrow', '').lower()
            move_amount = 0.1  # Move by 10cm
            
            if direction == 'left':
                return self.move_selected_object(-move_amount, 0, 0)
            elif direction == 'right':
                return self.move_selected_object(move_amount, 0, 0)
            elif direction == 'up':
                return self.move_selected_object(0, 0, -move_amount)
            elif direction == 'down':
                return self.move_selected_object(0, 0, move_amount)
                
        return False
    
    def handle_rotation_key(self, key):
        """
        Handle R + arrow key combinations for rotation
        
        Args:
            key: Key code or name
            
        Returns:
            bool: True if the key was handled
        """
        # Default rotation amount
        rotation_amount = 15  # Rotate by 15 degrees
        
        # R + Arrow keys - rotate selected object
        if key.startswith('Arrow'):
            direction = key.replace('Arrow', '').lower()
            
            # Regular arrow keys handle Y-axis (yaw) rotation
            if direction == 'left':
                return self.rotate_selected_object(0, -rotation_amount, 0)
            elif direction == 'right':
                return self.rotate_selected_object(0, rotation_amount, 0)
            # Up/down handle X-axis (pitch) rotation 
            elif direction == 'up':
                return self.rotate_selected_object(-rotation_amount, 0, 0)
            elif direction == 'down':
                return self.rotate_selected_object(rotation_amount, 0, 0)
        
        # Additional keys for Z-axis (roll) rotation
        elif key == 'z':
            return self.rotate_selected_object(0, 0, -rotation_amount)
        elif key == 'x':
            return self.rotate_selected_object(0, 0, rotation_amount)
                
        return False
    
    def handle_mouse_drag(self, x, y, dx, dy, mode='select'):
        """
        Handle mouse drag for moving or rotating objects
        
        Args:
            x: Current X screen coordinate
            y: Current Y screen coordinate
            dx: Change in X position
            dy: Change in Y position
            mode: Interaction mode ('select', 'move', 'rotate')
            
        Returns:
            bool: True if drag was handled
        """
        if self.selected_object is None:
            return False
            
        if mode == 'move':
            # Convert screen dx/dy to 3D movement
            # This is simplified and would need proper 3D calculations in real implementation
            move_scale = 0.01  # Scaling factor
            return self.move_selected_object(
                dx * move_scale,
                0,  # Don't change height with mouse drag
                dy * move_scale
            )
            
        elif mode == 'rotate':
            # Convert screen dx/dy to rotation
            rotation_scale = 0.5  # Scaling factor
            return self.rotate_selected_object(
                dy * rotation_scale,  # Pitch (around X)
                dx * rotation_scale,  # Yaw (around Y)
                0                     # Roll (around Z)
            )
            
        return False
    
    # Color management methods
    def set_object_color(self, obj, color_hex, opacity=1.0):
        """
        Set color for a specific object
        
        Args:
            obj: Object to set color for
            color_hex: Hex color code (e.g. "#FF0000" for red)
            opacity: Opacity value (0.0 to 1.0)
            
        Returns:
            bool: True if successful
        """
        if obj is None:
            return False
            
        # Save state for undo before changing color
        self._save_state(f"Change {obj.name} color to {color_hex}")
        
        # Set color attribute - use RGB format for internal storage
        if hasattr(obj, 'color'):
            if obj == self.room:
                # For room objects, use _hex_to_rgb conversion
                obj.color = self._hex_to_rgb(color_hex)
            elif isinstance(obj, (Door, Furniture)):
                # For Door and Furniture, always store as RGB list
                obj.color = self._hex_to_rgb(color_hex)
            else:
                # For other objects, store as hex string
                obj.color = color_hex
            
        if hasattr(obj, 'opacity'):
            obj.opacity = opacity
        
        return True
    
    def set_color_by_type(self, obj_type, color_hex, opacity=1.0):
        """
        Set color for all objects of a specified type
        
        Args:
            obj_type: Type of object ('room', 'door', 'window', 'furniture')
            color_hex: Hex color code
            opacity: Opacity value (0.0 to 1.0)
            
        Returns:
            int: Number of objects updated
        """
        count = 0
        
        # Save state for undo before changing colors
        self._save_state(f"Change all {obj_type} colors to {color_hex}")
        
        if obj_type.lower() == 'door':
            # Update all doors
            for door in self.doors:
                if hasattr(door, 'color'):
                    door.color = self._hex_to_rgb(color_hex)
                if hasattr(door, 'opacity'):
                    door.opacity = opacity
                count += 1
        elif obj_type.lower() == 'window':
            # Update all windows
            for window in self.windows:
                if hasattr(window, 'color'):
                    window.color = color_hex
                if hasattr(window, 'opacity'):
                    window.opacity = opacity
                count += 1
        elif obj_type.lower() == 'furniture':
            # Update all furniture
            for furniture in self.furniture:
                if hasattr(furniture, 'color'):
                    furniture.color = self._hex_to_rgb(color_hex)
                if hasattr(furniture, 'opacity'):
                    furniture.opacity = opacity
                count += 1
        
        return count
    
    def set_room_color(self, color_hex, opacity=1.0, component="walls"):
        """
        Set color for room (exterior surfaces)
        
        Args:
            color_hex: Color in hex format (#RRGGBB)
            opacity: Opacity value (0.0-1.0)
            component: Which component to color ('walls', 'floor', 'ceiling', 'north_wall', etc.)
        """
        if self.room is None:
            return
        
        # Save state for undo
        self._save_state(f"Change {component} color")
        
        # Convert hex color to RGB
        color_rgb = self._hex_to_rgb(color_hex)
        
        # Set color based on component
        if component == "walls":
            # When setting all walls, make sure to update both the default color and clear any individual settings
            self.room.wall_color = color_rgb
            self.room._north_wall_color = None
            self.room._south_wall_color = None
            self.room._east_wall_color = None
            self.room._west_wall_color = None
            self.room.wall_opacity = opacity
        elif component == "north_wall":
            self.room.north_wall_color = color_rgb
            # Also update default if this is the first wall being set
            if (self.room._south_wall_color is None and 
                self.room._east_wall_color is None and 
                self.room._west_wall_color is None):
                self.room.wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "south_wall":
            self.room.south_wall_color = color_rgb
            # Also update default if this is the first wall being set
            if (self.room._north_wall_color is None and 
                self.room._east_wall_color is None and 
                self.room._west_wall_color is None):
                self.room.wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "east_wall":
            self.room.east_wall_color = color_rgb
            # Also update default if this is the first wall being set
            if (self.room._north_wall_color is None and 
                self.room._south_wall_color is None and 
                self.room._west_wall_color is None):
                self.room.wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "west_wall":
            self.room.west_wall_color = color_rgb
            # Also update default if this is the first wall being set
            if (self.room._north_wall_color is None and 
                self.room._south_wall_color is None and 
                self.room._east_wall_color is None):
                self.room.wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "floor":
            self.room.floor_color = color_rgb
            self.room.floor_opacity = opacity
        elif component == "ceiling":
            self.room.ceiling_color = color_rgb
            self.room.ceiling_opacity = opacity
    
    def set_room_interior_color(self, color_hex, opacity=1.0, component="interior_walls"):
        """
        Set color for room interior surfaces
        
        Args:
            color_hex: Color in hex format (#RRGGBB)
            opacity: Opacity value (0.0-1.0)
            component: Which interior component to color ('interior_walls', 'interior_floor', etc.)
        """
        if self.room is None:
            return
        
        # Save state for undo
        self._save_state(f"Change interior {component} color")
        
        # Convert hex color to RGB
        color_rgb = self._hex_to_rgb(color_hex)
        
        # Set color based on component
        if component == "interior_walls":
            self.room.interior_wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "interior_north_wall":
            self.room.interior_north_wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "interior_south_wall":
            self.room.interior_south_wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "interior_east_wall":
            self.room.interior_east_wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "interior_west_wall":
            self.room.interior_west_wall_color = color_rgb
            self.room.wall_opacity = opacity
        elif component == "interior_floor":
            self.room.interior_floor_color = color_rgb
            self.room.floor_opacity = opacity
        elif component == "interior_ceiling":
            self.room.interior_ceiling_color = color_rgb
            self.room.ceiling_opacity = opacity
        
        # Update the corresponding exterior colors if interior colors are changed
        # (only if they haven't been explicitly set)
        if component == "interior_walls" and self.room._wall_color == [0.9, 0.9, 0.9]:
            # Default wall color not changed, sync with interior
            self.room.wall_color = color_rgb
    
    def _hex_to_rgb(self, hex_color):
        """
        Convert hex color string to RGB array with values 0-1
        
        Args:
            hex_color: Hex color string (e.g., "#FF0000")
            
        Returns:
            list: [r, g, b] with values 0-1
        """
        # Check if already an RGB array
        if isinstance(hex_color, (list, tuple)) and len(hex_color) >= 3:
            return hex_color
        
        # Convert hex to RGB
        hex_color = hex_color.lstrip('#')
        try:
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                return [r, g, b]
            elif len(hex_color) == 3:
                r = int(hex_color[0] + hex_color[0], 16) / 255.0
                g = int(hex_color[1] + hex_color[1], 16) / 255.0
                b = int(hex_color[2] + hex_color[2], 16) / 255.0
                return [r, g, b]
        except:
            pass
        
        # Return white as default if conversion fails
        return [1.0, 1.0, 1.0] 