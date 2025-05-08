from src.models.base_object import BaseObject

class Door(BaseObject):
    """
    Represents a door in the 3D scene
    """
    def __init__(self, door_id, name, door_type, width, height, position=None, rotation=None):
        """
        Initialize a door
        
        Args:
            door_id: Unique door identifier
            name: Display name
            door_type: Type of door (e.g., "Single Door", "Double Door")
            width: Door width in meters
            height: Door height in meters
            position: 3D position vector (x, y, z)
            rotation: 3D rotation vector in degrees (x, y, z)
        """
        super().__init__(door_id, name, position, rotation)
        
        self._door_type = door_type
        self._width = max(0.6, float(width))
        self._height = max(1.8, float(height))
        self._thickness = 0.05  # Door thickness in meters
        
        # Door appearance and state
        self._color = [0.6, 0.4, 0.2]  # Wood brown color
        self._texture = None
        self._open_angle = 0  # Door open angle (0 = closed, 90 = fully open)
        self._is_open = False
    
    @property
    def door_type(self):
        return self._door_type
    
    @door_type.setter
    def door_type(self, door_type):
        self._door_type = door_type
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = max(0.6, float(width))
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = max(1.8, float(height))
    
    @property
    def thickness(self):
        return self._thickness
    
    @thickness.setter
    def thickness(self, thickness):
        self._thickness = max(0.01, float(thickness))
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        self._color = color
    
    @property
    def texture(self):
        return self._texture
    
    @texture.setter
    def texture(self, texture_path):
        self._texture = texture_path
    
    @property
    def open_angle(self):
        return self._open_angle
    
    @open_angle.setter
    def open_angle(self, angle):
        # Clamp angle between 0 and 90 degrees
        self._open_angle = max(0, min(90, float(angle)))
        self._is_open = self._open_angle > 0
    
    @property
    def is_open(self):
        return self._is_open
    
    def open(self, angle=90):
        """
        Open the door to the specified angle
        
        Args:
            angle: Opening angle in degrees (0-90)
        """
        self.open_angle = angle
    
    def close(self):
        """Close the door"""
        self.open_angle = 0
    
    def toggle(self):
        """Toggle the door open/closed state"""
        if self._is_open:
            self.close()
        else:
            self.open()
    
    def to_dict(self):
        """
        Convert door to dictionary for serialization
        
        Returns:
            dict: Door data
        """
        data = super().to_dict()
        
        # Add door-specific properties
        data.update({
            "type": "Door",
            "door_type": self._door_type,
            "width": self._width,
            "height": self._height,
            "thickness": self._thickness,
            "color": self._color,
            "open_angle": self._open_angle,
            "is_open": self._is_open
        })
        
        # Add texture path if it exists
        if self._texture:
            data["texture"] = self._texture
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create door from dictionary
        
        Args:
            data: Dictionary with door data
            
        Returns:
            Door: Created door
        """
        door = cls(
            door_id=data["id"],
            name=data["name"],
            door_type=data["door_type"],
            width=data["width"],
            height=data["height"],
            position=data.get("position", [0, 0, 0]),
            rotation=data.get("rotation", [0, 0, 0])
        )
        
        # Set appearance properties
        if "thickness" in data:
            door.thickness = data["thickness"]
        if "color" in data:
            door.color = data["color"]
        if "texture" in data:
            door.texture = data["texture"]
        
        # Set state
        if "open_angle" in data:
            door.open_angle = data["open_angle"]
        
        # Set additional base properties
        if "scale" in data:
            door.scale = data["scale"]
        if "visible" in data:
            door.visible = data["visible"]
        if "selectable" in data:
            door.selectable = data["selectable"]
        
        return door 