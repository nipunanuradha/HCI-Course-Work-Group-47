from src.models.base_object import BaseObject

class Furniture(BaseObject):
    """
    Represents a furniture item in the 3D scene
    """
    def __init__(self, furniture_id, name, furniture_type, category, width, depth, height, position=None, rotation=None):
        """
        Initialize a furniture item
        
        Args:
            furniture_id: Unique furniture identifier
            name: Display name
            furniture_type: Type of furniture (e.g., "Dining Chair", "Coffee Table")
            category: Furniture category (e.g., "Chairs", "Tables")
            width: Furniture width in meters (X-axis)
            depth: Furniture depth in meters (Z-axis)
            height: Furniture height in meters (Y-axis)
            position: 3D position vector (x, y, z)
            rotation: 3D rotation vector in degrees (x, y, z)
        """
        super().__init__(furniture_id, name, position, rotation)
        
        self._furniture_type = furniture_type
        self._category = category
        self._width = max(0.1, float(width))
        self._depth = max(0.1, float(depth))
        self._height = max(0.1, float(height))
        
        # Furniture appearance
        self._color = [0.8, 0.8, 0.8]  # Default light gray
        self._texture = None
        self._material_type = "wood"  # Default material
        
        # For some furniture types (e.g., adjustable chairs)
        self._adjustable_parts = {}
        
        # Set default color based on category
        self._set_default_color()
    
    @property
    def furniture_type(self):
        return self._furniture_type
    
    @furniture_type.setter
    def furniture_type(self, furniture_type):
        self._furniture_type = furniture_type
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        self._category = category
        # Update default color when category changes
        self._set_default_color()
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, width):
        self._width = max(0.1, float(width))
    
    @property
    def depth(self):
        return self._depth
    
    @depth.setter
    def depth(self, depth):
        self._depth = max(0.1, float(depth))
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = max(0.1, float(height))
    
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
    def material_type(self):
        return self._material_type
    
    @material_type.setter
    def material_type(self, material_type):
        valid_materials = ["wood", "metal", "fabric", "leather", "glass", "plastic"]
        self._material_type = material_type if material_type in valid_materials else "wood"
    
    @property
    def adjustable_parts(self):
        return self._adjustable_parts
    
    def add_adjustable_part(self, part_name, min_value, max_value, current_value):
        """
        Add an adjustable part to the furniture
        
        Args:
            part_name: Name of the adjustable part
            min_value: Minimum value for adjustment
            max_value: Maximum value for adjustment
            current_value: Current value
        """
        self._adjustable_parts[part_name] = {
            "min": min_value,
            "max": max_value,
            "current": current_value
        }
    
    def adjust_part(self, part_name, value):
        """
        Adjust a part of the furniture
        
        Args:
            part_name: Name of the part to adjust
            value: New value for the part
            
        Returns:
            bool: True if adjustment was successful
        """
        if part_name in self._adjustable_parts:
            part = self._adjustable_parts[part_name]
            # Clamp value to valid range
            clamped_value = max(part["min"], min(part["max"], value))
            part["current"] = clamped_value
            return True
        return False
    
    def _set_default_color(self):
        """Set default color based on furniture category"""
        if self._category == "Chairs":
            self._color = [0.3, 0.3, 0.35]  # Dark gray
        elif self._category == "Tables":
            self._color = [0.6, 0.4, 0.2]  # Brown wood
        elif self._category == "Sofas":
            self._color = [0.2, 0.2, 0.6]  # Blue
        elif self._category == "Beds":
            self._color = [0.9, 0.9, 0.9]  # White/light
    
    def to_dict(self):
        """
        Convert furniture to dictionary for serialization
        
        Returns:
            dict: Furniture data
        """
        data = super().to_dict()
        
        # Add furniture-specific properties
        data.update({
            "type": "Furniture",
            "furniture_type": self._furniture_type,
            "category": self._category,
            "width": self._width,
            "depth": self._depth,
            "height": self._height,
            "color": self._color,
            "material_type": self._material_type,
            "adjustable_parts": self._adjustable_parts.copy() if self._adjustable_parts else {}
        })
        
        # Add texture path if it exists
        if self._texture:
            data["texture"] = self._texture
        
        return data
    
    @classmethod
    def from_dict(cls, data):
        """
        Create furniture from dictionary
        
        Args:
            data: Dictionary with furniture data
            
        Returns:
            Furniture: Created furniture
        """
        furniture = cls(
            furniture_id=data["id"],
            name=data["name"],
            furniture_type=data["furniture_type"],
            category=data["category"],
            width=data["width"],
            depth=data["depth"],
            height=data["height"],
            position=data.get("position", [0, 0, 0]),
            rotation=data.get("rotation", [0, 0, 0])
        )
        
        # Set appearance properties
        if "color" in data:
            furniture.color = data["color"]
        if "texture" in data:
            furniture.texture = data["texture"]
        if "material_type" in data:
            furniture.material_type = data["material_type"]
        
        # Set adjustable parts
        for part_name, part_data in data.get("adjustable_parts", {}).items():
            furniture.add_adjustable_part(
                part_name=part_name,
                min_value=part_data["min"],
                max_value=part_data["max"],
                current_value=part_data["current"]
            )
        
        # Set additional base properties
        if "scale" in data:
            furniture.scale = data["scale"]
        if "visible" in data:
            furniture.visible = data["visible"]
        if "selectable" in data:
            furniture.selectable = data["selectable"]
        
        return furniture 