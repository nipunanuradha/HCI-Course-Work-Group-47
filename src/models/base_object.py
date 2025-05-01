import numpy as np
import math
from src.rendering.matrix import vec3, mat4, translate, rotate, scale, radians

class BaseObject:
    """
    Base class for all 3D objects in the scene
    """
    def __init__(self, object_id, name, position=None, rotation=None):
        """
        Initialize the base object
        
        Args:
            object_id: Unique identifier
            name: Display name of the object
            position: 3D position vector (x, y, z)
            rotation: 3D rotation vector in degrees (x, y, z)
        """
        self._id = object_id
        self._name = name
        self._position = np.array([0.0, 0.0, 0.0], dtype=np.float32) if position is None else np.array(position, dtype=np.float32)
        self._rotation = np.array([0.0, 0.0, 0.0], dtype=np.float32) if rotation is None else np.array(rotation, dtype=np.float32)
        self._scale = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        self._visible = True
        self._selectable = True
        self._is_selected = False
        
        # Will be set when the object mesh is loaded
        self._mesh = None
        self._material = None
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = np.array(position, dtype=np.float32)
    
    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, rotation):
        self._rotation = np.array(rotation, dtype=np.float32)
    
    @property
    def scale(self):
        return self._scale
    
    @scale.setter
    def scale(self, scale):
        if isinstance(scale, (int, float)):
            self._scale = np.array([scale, scale, scale], dtype=np.float32)
        else:
            self._scale = np.array(scale, dtype=np.float32)
    
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, visible):
        self._visible = bool(visible)
    
    @property
    def selectable(self):
        return self._selectable
    
    @selectable.setter
    def selectable(self, selectable):
        self._selectable = bool(selectable)
    
    @property
    def is_selected(self):
        return self._is_selected
    
    @is_selected.setter
    def is_selected(self, selected):
        self._is_selected = bool(selected)
    
    @property
    def mesh(self):
        return self._mesh
    
    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh
    
    @property
    def material(self):
        return self._material
    
    @material.setter
    def material(self, material):
        self._material = material
    
    def get_id(self):
        """Get the object's unique ID"""
        return self._id
    
    def get_model_matrix(self):
        """
        Calculate the model matrix for this object
        
        Returns:
            4x4 transformation matrix
        """
        # Create identity matrix
        model_matrix = mat4(1.0)
        
        # Apply translation
        model_matrix = translate(model_matrix, self._position)
        
        # Apply rotation (in degrees)
        model_matrix = rotate(model_matrix, radians(self._rotation[0]), vec3(1, 0, 0))
        model_matrix = rotate(model_matrix, radians(self._rotation[1]), vec3(0, 1, 0))
        model_matrix = rotate(model_matrix, radians(self._rotation[2]), vec3(0, 0, 1))
        
        # Apply scale
        model_matrix = scale(model_matrix, self._scale)
        
        return model_matrix
    
    def to_dict(self):
        """
        Convert object to dictionary for serialization
        
        Returns:
            dict: Object data
        """
        return {
            "id": self._id,
            "name": self._name,
            "position": self._position.tolist(),
            "rotation": self._rotation.tolist(),
            "scale": self._scale.tolist(),
            "visible": self._visible,
            "selectable": self._selectable,
            "is_selected": self._is_selected
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create object from dictionary
        
        Args:
            data: Dictionary with object data
            
        Returns:
            BaseObject: Created object
        """
        obj = cls(
            object_id=data["id"],
            name=data["name"],
            position=data.get("position", [0, 0, 0]),
            rotation=data.get("rotation", [0, 0, 0])
        )
        
        # Set additional properties
        if "scale" in data:
            obj.scale = data["scale"]
        if "visible" in data:
            obj.visible = data["visible"]
        if "selectable" in data:
            obj.selectable = data["selectable"]
        
        return obj 