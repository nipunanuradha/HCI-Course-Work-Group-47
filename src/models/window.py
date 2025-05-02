from src.models.base_object import BaseObject

class Window(BaseObject):
    """
    Represents a window in the 3D scene
    """
    def __init__(self, window_id, name, window_type, width, height, position=None, rotation=None):
        """
        Initialize a window
        
        Args:
            window_id: Unique window identifier
            name: Display name
            window_type: Type of window (e.g., "Single Window", "Double Window")
            width: Window width in meters
            height: Window height in meters
            position: 3D position vector (x, y, z)
            rotation: 3D rotation vector in degrees (x, y, z)
        """
        super().__init__(window_id, name, position, rotation)
        
        self._window_type = window_type
        self._width = max(0.5, float(width))
        self._height = max(0.5, float(height))
        self._thickness = 0.1  # Window frame thickness in meters
        
        # Window appearance and state
        self._frame_color = [0.95, 0.95, 0.95]  # White frame like in the reference image
        self._glass_color = [0.95, 0.97, 0.99, 0.4]  # Very light blue with transparency
        self._glass_transparency = 0.6  # Slightly more transparent for realistic glass
        self._texture = None
        self._open_percentage = 0  # Window open state (0 = closed, 100 = fully open)
        self._is_open = False
        
        # For bay windows
        self._angle = 0  # Angle between window segments (for bay windows)
        self._segments = 1  # Number of segments (1 for regular, 3+ for bay windows)
    
    @property
    def window_type(self):
        return self._window_type
    
    @window_type.setter
    def window_type(self, window_type):
        self._window_type = window_type
        
        # Set default segments based on window type
        if window_type == "Bay Window":
            self._segments = 3
        elif window_type == "Double Window":
            self._segments = 2
        else:
            self._segments = 1
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = max(0.5, float(width))
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = max(0.5, float(height))
    
    @property
    def thickness(self):
        return self._thickness
    
    @thickness.setter
    def thickness(self, thickness):
        self._thickness = max(0.05, float(thickness))
    
    @property
    def frame_color(self):
        return self._frame_color
    
    @frame_color.setter
    def frame_color(self, color):
        self._frame_color = color
    
    @property
    def glass_color(self):
        return self._glass_color
    
    @glass_color.setter
    def glass_color(self, color):
        self._glass_color = color
    
    @property
    def glass_transparency(self):
        return self._glass_transparency
    
    @glass_transparency.setter
    def glass_transparency(self, transparency):
        # Clamp transparency between 0 and 1
        self._glass_transparency = max(0, min(1, float(transparency)))
    
    @property
    def texture(self):
        return self._texture
    
    @texture.setter
    def texture(self, texture_path):
        self._texture = texture_path
    
    @property
    def open_percentage(self):
        return self._open_percentage
    
    @open_percentage.setter
    def open_percentage(self, percentage):
        # Clamp percentage between 0 and 100
        self._open_percentage = max(0, min(100, float(percentage)))
        self._is_open = self._open_percentage > 0
    
    @property
    def is_open(self):
        return self._is_open
    
    @property
    def angle(self):
        return self._angle
    
    @angle.setter
    def angle(self, angle):
        if self._window_type == "Bay Window":
            # Bay windows typically have angles between 90 and 180 degrees
            self._angle = max(90, min(180, float(angle)))
    
    @property
    def segments(self):
        return self._segments
    
    @segments.setter
    def segments(self, segments):
        if self._window_type == "Bay Window":
            # Bay windows should have at least 3 segments
            self._segments = max(3, int(segments))
        elif self._window_type == "Double Window":
            self._segments = 2
        else:
            self._segments = 1
    
    def open(self, percentage=100):
        """
        Open the window to the specified percentage
        
        Args:
            percentage: Opening percentage (0-100)
        """
        self.open_percentage = percentage
    
    def close(self):
        """Close the window"""
        self.open_percentage = 0
    
    def toggle(self):
        """Toggle the window open/closed state"""
        if self._is_open:
            self.close()
        else:
            self.open()
    
    def to_dict(self):
        """
        Convert window to dictionary for serialization
        
        Returns:
            dict: Window data
        """
        data = super().to_dict()
        
        # Add window-specific properties
        data.update({
            "type": "Window",
            "window_type": self._window_type,
            "width": self._width,
            "height": self._height,
            "thickness": self._thickness,
            "frame_color": self._frame_color,
            "glass_color": self._glass_color,
            "glass_transparency": self._glass_transparency,
            "open_percentage": self._open_percentage,
            "is_open": self._is_open,
            "segments": self._segments
        })
        
        # Add bay window angle if applicable
        if self._window_type == "Bay Window":
            data["angle"] = self._angle
        
        # Add texture path if it exists
        if self._texture:
            data["texture"] = self._texture
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create window from dictionary
        
        Args:
            data: Dictionary with window data
            
        Returns:
            Window: Created window
        """
        window = cls(
            window_id=data["id"],
            name=data["name"],
            window_type=data["window_type"],
            width=data["width"],
            height=data["height"],
            position=data.get("position", [0, 0, 0]),
            rotation=data.get("rotation", [0, 0, 0])
        )
        
        # Set appearance properties
        if "thickness" in data:
            window.thickness = data["thickness"]
        if "frame_color" in data:
            window.frame_color = data["frame_color"]
        if "glass_color" in data:
            window.glass_color = data["glass_color"]
        if "glass_transparency" in data:
            window.glass_transparency = data["glass_transparency"]
        if "texture" in data:
            window.texture = data["texture"]
        
        # Set state
        if "open_percentage" in data:
            window.open_percentage = data["open_percentage"]
        
        # Set bay window properties
        if "segments" in data:
            window.segments = data["segments"]
        if "angle" in data and window.window_type == "Bay Window":
            window.angle = data["angle"]
        
        # Set additional base properties
        if "scale" in data:
            window.scale = data["scale"]
        if "visible" in data:
            window.visible = data["visible"]
        if "selectable" in data:
            window.selectable = data["selectable"]
        
        return window 