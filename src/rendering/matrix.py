import numpy as np
import math

def vec3(x, y=None, z=None):
    """Create a 3D vector"""
    if y is None and z is None:
        if isinstance(x, (list, tuple, np.ndarray)):
            return np.array(x, dtype=np.float32)
        return np.array([x, x, x], dtype=np.float32)
    return np.array([x, y, z], dtype=np.float32)

def normalize(vector):
    """Normalize a vector"""
    norm = np.linalg.norm(vector)
    if norm < 1e-10:  # Avoid division by zero
        return vector
    return vector / norm

def cross(v1, v2):
    """Cross product of two vectors"""
    return np.cross(v1, v2)

def radians(degrees):
    """Convert degrees to radians"""
    return math.radians(degrees)

def length(vector):
    """Calculate vector length"""
    return np.linalg.norm(vector)

def distance(v1, v2):
    """Calculate distance between two points"""
    return np.linalg.norm(v1 - v2)

def mat4(value=None):
    """Create a 4x4 matrix"""
    if value is None or value == 1.0:
        return np.identity(4, dtype=np.float32)
    return np.array([[value, 0, 0, 0],
                     [0, value, 0, 0],
                     [0, 0, value, 0],
                     [0, 0, 0, value]], dtype=np.float32)

def translate(matrix, vec):
    """Translate a matrix by a vector"""
    result = matrix.copy()
    result[0, 3] = matrix[0, 0] * vec[0] + matrix[0, 1] * vec[1] + matrix[0, 2] * vec[2] + matrix[0, 3]
    result[1, 3] = matrix[1, 0] * vec[0] + matrix[1, 1] * vec[1] + matrix[1, 2] * vec[2] + matrix[1, 3]
    result[2, 3] = matrix[2, 0] * vec[0] + matrix[2, 1] * vec[1] + matrix[2, 2] * vec[2] + matrix[2, 3]
    result[3, 3] = matrix[3, 0] * vec[0] + matrix[3, 1] * vec[1] + matrix[3, 2] * vec[2] + matrix[3, 3]
    return result

def rotate(matrix, angle, axis):
    """Rotate a matrix around an axis by angle radians"""
    c = math.cos(angle)
    s = math.sin(angle)
    axis = normalize(axis)
    temp = np.array([(1 - c) * axis], dtype=np.float32).T
    
    rotate_matrix = np.identity(4, dtype=np.float32)
    rotate_matrix[0, 0] = c + temp[0, 0] * axis[0]
    rotate_matrix[0, 1] = temp[0, 0] * axis[1] + s * axis[2]
    rotate_matrix[0, 2] = temp[0, 0] * axis[2] - s * axis[1]
    rotate_matrix[1, 0] = temp[0, 0] * axis[0] - s * axis[2]
    rotate_matrix[1, 1] = c + temp[0, 0] * axis[1]
    rotate_matrix[1, 2] = temp[0, 0] * axis[2] + s * axis[0]
    rotate_matrix[2, 0] = temp[0, 0] * axis[0] + s * axis[1]
    rotate_matrix[2, 1] = temp[0, 0] * axis[1] - s * axis[0]
    rotate_matrix[2, 2] = c + temp[0, 0] * axis[2]
    
    # Correct matrix multiplication
    return np.matmul(matrix, rotate_matrix)

def scale(matrix, vec):
    """Scale a matrix by a vector"""
    result = matrix.copy()
    result[0, 0] *= vec[0]
    result[1, 1] *= vec[1]
    result[2, 2] *= vec[2]
    return result

def lookAt(eye, center, up):
    """
    Create a view matrix looking from eye to center with up vector
    
    Args:
        eye: Camera position
        center: Target position
        up: Up vector
        
    Returns:
        4x4 view matrix
    """
    eye = np.asarray(eye, dtype=np.float32)
    center = np.asarray(center, dtype=np.float32)
    up = np.asarray(up, dtype=np.float32)
    
    f = normalize(center - eye)
    s = normalize(np.cross(f, up))
    u = np.cross(s, f)
    
    result = np.identity(4, dtype=np.float32)
    result[0, 0] = s[0]
    result[0, 1] = s[1]
    result[0, 2] = s[2]
    result[1, 0] = u[0]
    result[1, 1] = u[1]
    result[1, 2] = u[2]
    result[2, 0] = -f[0]
    result[2, 1] = -f[1]
    result[2, 2] = -f[2]
    result[0, 3] = -np.dot(s, eye)
    result[1, 3] = -np.dot(u, eye)
    result[2, 3] = np.dot(f, eye)
    
    return result

def perspective(fov, aspect, near, far):
    """
    Create a perspective projection matrix
    
    Args:
        fov: Field of view in radians
        aspect: Aspect ratio (width/height)
        near: Near clipping plane
        far: Far clipping plane
        
    Returns:
        4x4 perspective projection matrix
    """
    f = 1.0 / math.tan(fov / 2)
    
    result = np.zeros((4, 4), dtype=np.float32)
    result[0, 0] = f / aspect
    result[1, 1] = f
    result[2, 2] = (far + near) / (near - far)
    result[2, 3] = (2 * far * near) / (near - far)
    result[3, 2] = -1
    
    return result

def value_ptr(matrix):
    """
    Convert a matrix to a format suitable for OpenGL uniforms
    
    Args:
        matrix: Numpy matrix
        
    Returns:
        Flattened matrix in column-major order (OpenGL format)
    """
    # OpenGL expects column-major order (Fortran order in numpy)
    return np.ascontiguousarray(matrix.T, dtype=np.float32) 