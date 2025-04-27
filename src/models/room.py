from src.models.base_object import BaseObject

class Room(BaseObject):
    """
    Represents a room in the 3D scene
    """
    def __init__(self, room_id, name, room_type, width, length, height, position=None, rotation=None):
        """
        Initialize a room
        
        Args:
            room_id: Unique room identifier
            name: Display name
            room_type: Type of room (e.g., "Living Room", "Dining Room")
            width: Room width in meters (X-axis)
            length: Room length in meters (Z-axis)
            height: Room height in meters (Y-axis)
            position: 3D position vector (x, y, z)
            rotation: 3D rotation vector in degrees (x, y, z)
        """
        super().__init__(room_id, name, position, rotation)
        
        self._room_type = room_type
        self._width = max(1.0, float(width))     # Ensure positive dimensions
        self._length = max(1.0, float(length))
        self._height = max(1.0, float(height))
        
        # Room appearance properties - Exterior colors (seen from outside)
        self._wall_color = [0.8, 0.8, 0.8]       # Light gray (default for all walls)
        self._north_wall_color = None
        self._south_wall_color = None
        self._east_wall_color = None
        self._west_wall_color = None
        self._floor_color = [0.8, 0.8, 0.8]      # Light gray
        self._ceiling_color = [0.8, 0.8, 0.8]    # Light gray
        
        # Interior colors (seen from inside the room)
        self._interior_wall_color = [0.85, 0.85, 0.82]  # Slightly warmer light gray for all interior walls
        self._interior_north_wall_color = None
        self._interior_south_wall_color = None
        self._interior_east_wall_color = None
        self._interior_west_wall_color = None
        self._interior_floor_color = [0.82, 0.8, 0.75]  # Slightly warmer floor
        self._interior_ceiling_color = [0.9, 0.9, 0.9]  # Slightly brighter ceiling
        
        # Textures
        self._floor_texture = None
        self._wall_texture = None
        self._ceiling_texture = None
        
        # Opacity properties 
        self._wall_opacity = 1.0
        self._floor_opacity = 1.0
        self._ceiling_opacity = 1.0
    
    @property
    def room_type(self):
        return self._room_type
    
    @room_type.setter
    def room_type(self, room_type):
        self._room_type = room_type
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = max(1.0, float(width))
    
    @property
    def length(self):
        return self._length
    
    @length.setter
    def length(self, length):
        self._length = max(1.0, float(length))
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = max(1.0, float(height))
    
    @property
    def wall_color(self):
        return self._wall_color
    
    @wall_color.setter
    def wall_color(self, color):
        self._wall_color = color
    
    @property
    def floor_color(self):
        return self._floor_color
    
    @floor_color.setter
    def floor_color(self, color):
        self._floor_color = color
    
    @property
    def ceiling_color(self):
        return self._ceiling_color
    
    @ceiling_color.setter
    def ceiling_color(self, color):
        self._ceiling_color = color
    
    @property
    def north_wall_color(self):
        return self._north_wall_color if self._north_wall_color is not None else self._wall_color

    @north_wall_color.setter
    def north_wall_color(self, color):
        self._north_wall_color = color

    @property
    def south_wall_color(self):
        return self._south_wall_color if self._south_wall_color is not None else self._wall_color

    @south_wall_color.setter
    def south_wall_color(self, color):
        self._south_wall_color = color

    @property
    def east_wall_color(self):
        return self._east_wall_color if self._east_wall_color is not None else self._wall_color

    @east_wall_color.setter
    def east_wall_color(self, color):
        self._east_wall_color = color

    @property
    def west_wall_color(self):
        return self._west_wall_color if self._west_wall_color is not None else self._wall_color

    @west_wall_color.setter
    def west_wall_color(self, color):
        self._west_wall_color = color
    
    @property
    def wall_texture(self):
        return self._wall_texture
    
    @wall_texture.setter
    def wall_texture(self, texture_path):
        self._wall_texture = texture_path
    
    @property
    def floor_texture(self):
        return self._floor_texture
    
    @floor_texture.setter
    def floor_texture(self, texture_path):
        self._floor_texture = texture_path
    
    @property
    def ceiling_texture(self):
        return self._ceiling_texture
    
    @ceiling_texture.setter
    def ceiling_texture(self, texture_path):
        self._ceiling_texture = texture_path
    
    @property
    def wall_opacity(self):
        return self._wall_opacity

    @wall_opacity.setter
    def wall_opacity(self, opacity):
        self._wall_opacity = float(opacity)

    @property
    def floor_opacity(self):
        return self._floor_opacity

    @floor_opacity.setter
    def floor_opacity(self, opacity):
        self._floor_opacity = float(opacity)

    @property
    def ceiling_opacity(self):
        return self._ceiling_opacity

    @ceiling_opacity.setter
    def ceiling_opacity(self, opacity):
        self._ceiling_opacity = float(opacity)
    
    # Properties for interior wall colors
    @property
    def interior_wall_color(self):
        return self._interior_wall_color
    
    @interior_wall_color.setter
    def interior_wall_color(self, color):
        self._interior_wall_color = color
    
    @property
    def interior_north_wall_color(self):
        return self._interior_north_wall_color if self._interior_north_wall_color is not None else self._interior_wall_color

    @interior_north_wall_color.setter
    def interior_north_wall_color(self, color):
        self._interior_north_wall_color = color

    @property
    def interior_south_wall_color(self):
        return self._interior_south_wall_color if self._interior_south_wall_color is not None else self._interior_wall_color

    @interior_south_wall_color.setter
    def interior_south_wall_color(self, color):
        self._interior_south_wall_color = color

    @property
    def interior_east_wall_color(self):
        return self._interior_east_wall_color if self._interior_east_wall_color is not None else self._interior_wall_color

    @interior_east_wall_color.setter
    def interior_east_wall_color(self, color):
        self._interior_east_wall_color = color

    @property
    def interior_west_wall_color(self):
        return self._interior_west_wall_color if self._interior_west_wall_color is not None else self._interior_wall_color

    @interior_west_wall_color.setter
    def interior_west_wall_color(self, color):
        self._interior_west_wall_color = color
    
    @property
    def interior_floor_color(self):
        return self._interior_floor_color
    
    @interior_floor_color.setter
    def interior_floor_color(self, color):
        self._interior_floor_color = color
    
    @property
    def interior_ceiling_color(self):
        return self._interior_ceiling_color
    
    @interior_ceiling_color.setter
    def interior_ceiling_color(self, color):
        self._interior_ceiling_color = color
    
    def to_dict(self):
        """
        Convert room to dictionary for serialization
        
        Returns:
            dict: Room data
        """
        data = super().to_dict()
        
        # Add room-specific properties
        data.update({
            "type": "Room",
            "room_type": self._room_type,
            "width": self._width,
            "length": self._length,
            "height": self._height,
            # Exterior colors
            "wall_color": self._wall_color,
            "north_wall_color": self._north_wall_color,
            "south_wall_color": self._south_wall_color,
            "east_wall_color": self._east_wall_color,
            "west_wall_color": self._west_wall_color,
            "floor_color": self._floor_color,
            "ceiling_color": self._ceiling_color,
            # Interior colors
            "interior_wall_color": self._interior_wall_color,
            "interior_north_wall_color": self._interior_north_wall_color,
            "interior_south_wall_color": self._interior_south_wall_color,
            "interior_east_wall_color": self._interior_east_wall_color,
            "interior_west_wall_color": self._interior_west_wall_color,
            "interior_floor_color": self._interior_floor_color,
            "interior_ceiling_color": self._interior_ceiling_color,
            # Textures and opacity
            "wall_texture": self._wall_texture,
            "floor_texture": self._floor_texture,
            "ceiling_texture": self._ceiling_texture,
            "wall_opacity": self._wall_opacity,
            "floor_opacity": self._floor_opacity,
            "ceiling_opacity": self._ceiling_opacity
        })
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a room from dictionary data
        
        Args:
            data: Dictionary containing room data
            
        Returns:
            Room: Room instance
        """
        obj = cls(
            room_id=data.get("id"),
            name=data.get("name"),
            room_type=data.get("room_type"),
            width=data.get("width", 5.0),
            length=data.get("length", 5.0),
            height=data.get("height", 2.5),
            position=data.get("position"),
            rotation=data.get("rotation")
        )
        
        # Set room appearance properties if available
        if "wall_color" in data:
            obj._wall_color = data["wall_color"]
        if "north_wall_color" in data:
            obj._north_wall_color = data["north_wall_color"]
        if "south_wall_color" in data:
            obj._south_wall_color = data["south_wall_color"]
        if "east_wall_color" in data:
            obj._east_wall_color = data["east_wall_color"]
        if "west_wall_color" in data:
            obj._west_wall_color = data["west_wall_color"]
        if "floor_color" in data:
            obj._floor_color = data["floor_color"]
        if "ceiling_color" in data:
            obj._ceiling_color = data["ceiling_color"]
            
        # Set interior colors if available
        if "interior_wall_color" in data:
            obj._interior_wall_color = data["interior_wall_color"]
        if "interior_north_wall_color" in data:
            obj._interior_north_wall_color = data["interior_north_wall_color"]
        if "interior_south_wall_color" in data:
            obj._interior_south_wall_color = data["interior_south_wall_color"]
        if "interior_east_wall_color" in data:
            obj._interior_east_wall_color = data["interior_east_wall_color"]
        if "interior_west_wall_color" in data:
            obj._interior_west_wall_color = data["interior_west_wall_color"]
        if "interior_floor_color" in data:
            obj._interior_floor_color = data["interior_floor_color"]
        if "interior_ceiling_color" in data:
            obj._interior_ceiling_color = data["interior_ceiling_color"]
        
        # Set texture paths if available
        if "wall_texture" in data:
            obj._wall_texture = data["wall_texture"]
        if "floor_texture" in data:
            obj._floor_texture = data["floor_texture"]
        if "ceiling_texture" in data:
            obj._ceiling_texture = data["ceiling_texture"]
            
        # Set opacity values if available
        if "wall_opacity" in data:
            obj._wall_opacity = data["wall_opacity"]
        if "floor_opacity" in data:
            obj._floor_opacity = data["floor_opacity"]
        if "ceiling_opacity" in data:
            obj._ceiling_opacity = data["ceiling_opacity"]
        
        return obj 