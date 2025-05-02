import math
import numpy as np
from src.rendering.matrix import vec3, normalize, length, lookAt, perspective, radians, cross

class Camera:
    """
    Camera class for navigating the 3D scene
    """
    def __init__(self):
        # Camera position in world space
        self._position = np.array([0.0, 2.0, 5.0], dtype=np.float32)
        
        # Camera target point
        self._target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        
        # Up vector
        self._up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        
        # Field of view in degrees
        self._fov = 45.0
        
        # Aspect ratio (width/height)
        self._aspect_ratio = 16.0 / 9.0
        
        # Near and far clipping planes
        self._near = 0.1
        self._far = 1000.0
        
        # Camera orientation
        self._yaw = -90.0  # Horizontal rotation
        self._pitch = 0.0  # Vertical rotation
        
        # Movement speed
        self._movement_speed = 0.1
        self._rotation_speed = 0.2
        
        # View matrices
        self._view_matrix = self._calculate_view_matrix()
        self._projection_matrix = self._calculate_projection_matrix()
    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = np.array(position, dtype=np.float32)
        self._update_matrices()
    
    @property
    def target(self):
        return self._target
    
    @target.setter
    def target(self, target):
        self._target = np.array(target, dtype=np.float32)
        self._update_matrices()
    
    @property
    def up(self):
        return self._up
    
    @up.setter
    def up(self, up):
        self._up = np.array(up, dtype=np.float32)
        self._update_matrices()
    
    @property
    def fov(self):
        return self._fov
    
    @fov.setter
    def fov(self, fov):
        self._fov = max(1.0, min(120.0, fov))  # Clamp between 1 and 120 degrees
        self._update_matrices()
    
    @property
    def aspect_ratio(self):
        return self._aspect_ratio
    
    @aspect_ratio.setter
    def aspect_ratio(self, aspect_ratio):
        self._aspect_ratio = max(0.1, aspect_ratio)  # Ensure positive aspect ratio
        self._update_matrices()
    
    @property
    def view_matrix(self):
        return self._view_matrix
    
    @property
    def projection_matrix(self):
        return self._projection_matrix
    
    def reset(self):
        """Reset camera to default position and orientation"""
        self._position = np.array([0.0, 2.0, 5.0], dtype=np.float32)
        self._target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self._up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self._yaw = -90.0
        self._pitch = 0.0
        self._update_matrices()
    
    def rotate(self, yaw_offset, pitch_offset):
        """
        Rotate the camera around the target
        
        Args:
            yaw_offset: Change in horizontal angle (degrees)
            pitch_offset: Change in vertical angle (degrees)
        """
        self._yaw += yaw_offset * self._rotation_speed
        self._pitch += pitch_offset * self._rotation_speed
        
        # Clamp pitch to avoid flipping
        self._pitch = max(-89.0, min(89.0, self._pitch))
        
        # Convert spherical to Cartesian coordinates
        radius = np.linalg.norm(self._position - self._target)
        pitch_rad = math.radians(self._pitch)
        yaw_rad = math.radians(self._yaw)
        
        x = radius * math.cos(pitch_rad) * math.cos(yaw_rad)
        y = radius * math.sin(pitch_rad)
        z = radius * math.cos(pitch_rad) * math.sin(yaw_rad)
        
        # Update position relative to target
        self._position = self._target + np.array([x, y, z], dtype=np.float32)
        self._update_matrices()
    
    def pan(self, offset_x, offset_y):
        """
        Pan the camera and target in the view plane
        
        Args:
            offset_x: Horizontal movement
            offset_y: Vertical movement
        """
        # Calculate right and up vectors in world space
        forward = normalize(self._target - self._position)
        right = normalize(cross(forward, self._up))
        up = normalize(cross(right, forward))
        
        # Scale by movement speed
        right_offset = right * offset_x * self._movement_speed
        up_offset = up * offset_y * self._movement_speed
        
        # Move both position and target
        offset = right_offset + up_offset
        self._position += offset
        self._target += offset
        
        self._update_matrices()
    
    def zoom(self, amount):
        """
        Zoom camera by moving closer to or further from target
        
        Args:
            amount: Zoom amount (positive = zoom in, negative = zoom out)
        """
        direction = normalize(self._target - self._position)
        
        # Move along the view direction
        offset = direction * amount * self._movement_speed * 5.0
        
        # Calculate new position
        new_position = self._position + offset
        
        # Only update if we're not too close or too far
        distance = np.linalg.norm(new_position - self._target)
        if 0.5 < distance < 100.0:
            self._position = new_position
            self._update_matrices()
    
    def orbit(self, delta_x, delta_y):
        """
        Orbit around target point
        
        Args:
            delta_x: Horizontal orbit amount
            delta_y: Vertical orbit amount
        """
        self.rotate(delta_x, delta_y)
    
    def _update_matrices(self):
        """Update view and projection matrices"""
        self._view_matrix = self._calculate_view_matrix()
        self._projection_matrix = self._calculate_projection_matrix()
    
    def _calculate_view_matrix(self):
        """Calculate the view matrix"""
        return lookAt(self._position, self._target, self._up)
    
    def _calculate_projection_matrix(self):
        """Calculate the projection matrix"""
        return perspective(
            radians(self._fov),
            self._aspect_ratio,
            self._near,
            self._far
        ) 