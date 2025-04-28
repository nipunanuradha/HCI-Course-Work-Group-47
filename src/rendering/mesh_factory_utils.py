import numpy as np

def create_floor_vertices(half_width, half_length):
    """
    Create floor vertices with a border for visual distinction
    
    Args:
        half_width: Half width of the floor
        half_length: Half length of the floor
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Floor vertices (facing up, Y+)
    # Triangle 1
    vertices.extend([-half_width, 0, -half_length, 0, 1, 0, 0, 0])  # Bottom-left
    vertices.extend([half_width, 0, -half_length, 0, 1, 0, 1, 0])   # Bottom-right
    vertices.extend([half_width, 0, half_length, 0, 1, 0, 1, 1])    # Top-right
    
    # Triangle 2
    vertices.extend([-half_width, 0, -half_length, 0, 1, 0, 0, 0])  # Bottom-left
    vertices.extend([half_width, 0, half_length, 0, 1, 0, 1, 1])    # Top-right
    vertices.extend([-half_width, 0, half_length, 0, 1, 0, 0, 1])   # Top-left
    
    # Add border (slightly larger, dark color, as a separate set of vertices)
    border_offset = 0.03 * max(half_width, half_length)
    border_y = 0.001  # Slightly above the floor
    # Border rectangle (as two triangles)
    vertices.extend([
        -half_width - border_offset, border_y, -half_length - border_offset, 0, 1, 0, 0, 0,
        half_width + border_offset, border_y, -half_length - border_offset, 0, 1, 0, 1, 0,
        half_width + border_offset, border_y, half_length + border_offset, 0, 1, 0, 1, 1,
        -half_width - border_offset, border_y, -half_length - border_offset, 0, 1, 0, 0, 0,
        half_width + border_offset, border_y, half_length + border_offset, 0, 1, 0, 1, 1,
        -half_width - border_offset, border_y, half_length + border_offset, 0, 1, 0, 0, 1
    ])
    
    return vertices

def create_walls_vertices(half_width, half_length, height):
    """
    Create walls vertices with a border for visual distinction
    
    Args:
        half_width: Half width of the room
        half_length: Half length of the room
        height: Height of the room
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Wall 1: -X (left) wall, facing right (X+)
    # Triangle 1
    vertices.extend([-half_width, 0, -half_length, 1, 0, 0, 0, 0])         # Bottom-back
    vertices.extend([-half_width, 0, half_length, 1, 0, 0, 1, 0])          # Bottom-front
    vertices.extend([-half_width, height, half_length, 1, 0, 0, 1, 1])     # Top-front
    
    # Triangle 2
    vertices.extend([-half_width, 0, -half_length, 1, 0, 0, 0, 0])         # Bottom-back
    vertices.extend([-half_width, height, half_length, 1, 0, 0, 1, 1])     # Top-front
    vertices.extend([-half_width, height, -half_length, 1, 0, 0, 0, 1])    # Top-back
    
    # Wall 2: +X (right) wall, facing left (X-)
    # Triangle 1
    vertices.extend([half_width, 0, half_length, -1, 0, 0, 0, 0])          # Bottom-front
    vertices.extend([half_width, 0, -half_length, -1, 0, 0, 1, 0])         # Bottom-back
    vertices.extend([half_width, height, -half_length, -1, 0, 0, 1, 1])    # Top-back
    
    # Triangle 2
    vertices.extend([half_width, 0, half_length, -1, 0, 0, 0, 0])          # Bottom-front
    vertices.extend([half_width, height, -half_length, -1, 0, 0, 1, 1])    # Top-back
    vertices.extend([half_width, height, half_length, -1, 0, 0, 0, 1])     # Top-front
    
    # Wall 3: -Z (back) wall, facing forward (Z+)
    # Triangle 1
    vertices.extend([half_width, 0, -half_length, 0, 0, 1, 0, 0])          # Bottom-right
    vertices.extend([-half_width, 0, -half_length, 0, 0, 1, 1, 0])         # Bottom-left
    vertices.extend([-half_width, height, -half_length, 0, 0, 1, 1, 1])    # Top-left
    
    # Triangle 2
    vertices.extend([half_width, 0, -half_length, 0, 0, 1, 0, 0])          # Bottom-right
    vertices.extend([-half_width, height, -half_length, 0, 0, 1, 1, 1])    # Top-left
    vertices.extend([half_width, height, -half_length, 0, 0, 1, 0, 1])     # Top-right
    
    # Wall 4: +Z (front) wall, facing backward (Z-)
    # Triangle 1
    vertices.extend([-half_width, 0, half_length, 0, 0, -1, 0, 0])         # Bottom-left
    vertices.extend([half_width, 0, half_length, 0, 0, -1, 1, 0])          # Bottom-right
    vertices.extend([half_width, height, half_length, 0, 0, -1, 1, 1])     # Top-right
    
    # Triangle 2
    vertices.extend([-half_width, 0, half_length, 0, 0, -1, 0, 0])         # Bottom-left
    vertices.extend([half_width, height, half_length, 0, 0, -1, 1, 1])     # Top-right
    vertices.extend([-half_width, height, half_length, 0, 0, -1, 0, 1])    # Top-left
    
    # Add borders for each wall (slightly larger, dark color, as a separate set of vertices)
    border_offset = 0.01 * max(half_width, half_length, height)
    border_height = height + border_offset * 2
    # West wall border
    vertices.extend([
        -half_width - border_offset, 0, -half_length - border_offset, 1, 0, 0, 0, 0,
        -half_width - border_offset, 0, half_length + border_offset, 1, 0, 0, 1, 0,
        -half_width - border_offset, border_height, half_length + border_offset, 1, 0, 0, 1, 1,
        -half_width - border_offset, 0, -half_length - border_offset, 1, 0, 0, 0, 0,
        -half_width - border_offset, border_height, half_length + border_offset, 1, 0, 0, 1, 1,
        -half_width - border_offset, border_height, -half_length - border_offset, 1, 0, 0, 0, 1
    ])
    # East wall border
    vertices.extend([
        half_width + border_offset, 0, half_length + border_offset, -1, 0, 0, 0, 0,
        half_width + border_offset, 0, -half_length - border_offset, -1, 0, 0, 1, 0,
        half_width + border_offset, border_height, -half_length - border_offset, -1, 0, 0, 1, 1,
        half_width + border_offset, 0, half_length + border_offset, -1, 0, 0, 0, 0,
        half_width + border_offset, border_height, -half_length - border_offset, -1, 0, 0, 1, 1,
        half_width + border_offset, border_height, half_length + border_offset, -1, 0, 0, 0, 1
    ])
    # North wall border
    vertices.extend([
        half_width + border_offset, 0, -half_length - border_offset, 0, 0, 1, 0, 0,
        -half_width - border_offset, 0, -half_length - border_offset, 0, 0, 1, 1, 0,
        -half_width - border_offset, border_height, -half_length - border_offset, 0, 0, 1, 1, 1,
        half_width + border_offset, 0, -half_length - border_offset, 0, 0, 1, 0, 0,
        -half_width - border_offset, border_height, -half_length - border_offset, 0, 0, 1, 1, 1,
        half_width + border_offset, border_height, -half_length - border_offset, 0, 0, 1, 0, 1
    ])
    # South wall border
    vertices.extend([
        -half_width - border_offset, 0, half_length + border_offset, 0, 0, -1, 0, 0,
        half_width + border_offset, 0, half_length + border_offset, 0, 0, -1, 1, 0,
        half_width + border_offset, border_height, half_length + border_offset, 0, 0, -1, 1, 1,
        -half_width - border_offset, 0, half_length + border_offset, 0, 0, -1, 0, 0,
        half_width + border_offset, border_height, half_length + border_offset, 0, 0, -1, 1, 1,
        -half_width - border_offset, border_height, half_length + border_offset, 0, 0, -1, 0, 1
    ])
    
    return vertices

def create_ceiling_vertices(half_width, half_length, height):
    """
    Create ceiling vertices with a border for visual distinction
    
    Args:
        half_width: Half width of the room
        half_length: Half length of the room
        height: Height of the room
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Ceiling vertices (facing down, Y-)
    # Triangle 1
    vertices.extend([half_width, height, -half_length, 0, -1, 0, 0, 0])    # Bottom-right
    vertices.extend([-half_width, height, -half_length, 0, -1, 0, 1, 0])   # Bottom-left
    vertices.extend([-half_width, height, half_length, 0, -1, 0, 1, 1])    # Top-left
    
    # Triangle 2
    vertices.extend([half_width, height, -half_length, 0, -1, 0, 0, 0])    # Bottom-right
    vertices.extend([-half_width, height, half_length, 0, -1, 0, 1, 1])    # Top-left
    vertices.extend([half_width, height, half_length, 0, -1, 0, 0, 1])     # Top-right
    
    # Add border (slightly larger, dark color, as a separate set of vertices)
    border_offset = 0.03 * max(half_width, half_length)
    border_y = height + 0.001  # Slightly above the ceiling
    vertices.extend([
        half_width + border_offset, border_y, -half_length - border_offset, 0, -1, 0, 0, 0,
        -half_width - border_offset, border_y, -half_length - border_offset, 0, -1, 0, 1, 0,
        -half_width - border_offset, border_y, half_length + border_offset, 0, -1, 0, 1, 1,
        half_width + border_offset, border_y, -half_length - border_offset, 0, -1, 0, 0, 0,
        -half_width - border_offset, border_y, half_length + border_offset, 0, -1, 0, 1, 1,
        half_width + border_offset, border_y, half_length + border_offset, 0, -1, 0, 0, 1
    ])
    
    return vertices

def create_box_vertices(half_width, half_height, half_depth, offset_x=0, offset_y=0, offset_z=0):
    """
    Create vertices for a box
    
    Args:
        half_width: Half width of the box
        half_height: Half height of the box
        half_depth: Half depth of the box
        offset_x: X position offset
        offset_y: Y position offset
        offset_z: Z position offset
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Define the 8 corners of the box
    corners = [
        # Front face (Z+)
        [-half_width + offset_x, -half_height + offset_y, half_depth + offset_z],  # Bottom-left
        [half_width + offset_x, -half_height + offset_y, half_depth + offset_z],   # Bottom-right
        [half_width + offset_x, half_height + offset_y, half_depth + offset_z],    # Top-right
        [-half_width + offset_x, half_height + offset_y, half_depth + offset_z],   # Top-left
        
        # Back face (Z-)
        [half_width + offset_x, -half_height + offset_y, -half_depth + offset_z],  # Bottom-right
        [-half_width + offset_x, -half_height + offset_y, -half_depth + offset_z], # Bottom-left
        [-half_width + offset_x, half_height + offset_y, -half_depth + offset_z],  # Top-left
        [half_width + offset_x, half_height + offset_y, -half_depth + offset_z]    # Top-right
    ]
    
    # Define the 6 faces of the box (2 triangles each)
    # Each face: normal vector and texture coordinates
    faces = [
        # Front face (Z+)
        [[0, 1, 2], [0, 0, 1], [0, 0, 1, 0, 1, 1]],
        [[0, 2, 3], [0, 0, 1], [0, 0, 1, 1, 0, 1]],
        
        # Right face (X+)
        [[1, 4, 7], [1, 0, 0], [0, 0, 1, 0, 1, 1]],
        [[1, 7, 2], [1, 0, 0], [0, 0, 1, 1, 0, 1]],
        
        # Back face (Z-)
        [[4, 5, 6], [0, 0, -1], [0, 0, 1, 0, 1, 1]],
        [[4, 6, 7], [0, 0, -1], [0, 0, 1, 1, 0, 1]],
        
        # Left face (X-)
        [[5, 0, 3], [-1, 0, 0], [0, 0, 1, 0, 1, 1]],
        [[5, 3, 6], [-1, 0, 0], [0, 0, 1, 1, 0, 1]],
        
        # Top face (Y+)
        [[3, 2, 7], [0, 1, 0], [0, 0, 1, 0, 1, 1]],
        [[3, 7, 6], [0, 1, 0], [0, 0, 1, 1, 0, 1]],
        
        # Bottom face (Y-)
        [[5, 4, 1], [0, -1, 0], [0, 0, 1, 0, 1, 1]],
        [[5, 1, 0], [0, -1, 0], [0, 0, 1, 1, 0, 1]]
    ]
    
    # Create vertices for each face
    for face in faces:
        indices, normal, texcoords = face
        
        # Add vertices for this triangle
        for i, idx in enumerate(indices):
            # Position
            vertices.extend(corners[idx])
            
            # Normal
            vertices.extend(normal)
            
            # Texture coordinates
            vertices.extend([texcoords[i*2], texcoords[i*2+1]])
    
    return vertices

def create_box_frame_vertices(half_width, half_height, half_depth, offset_x=0, offset_y=0, offset_z=0, frame_width=0.05):
    """
    Create vertices for a box frame (like a window frame)
    
    Args:
        half_width: Half width of the box
        half_height: Half height of the box
        half_depth: Half depth of the box
        offset_x: X position offset
        offset_y: Y position offset
        offset_z: Z position offset
        frame_width: Width of the frame
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Outer box
    outer_vertices = create_box_vertices(
        half_width, half_height, half_depth,
        offset_x, offset_y, offset_z
    )
    
    # Inner box (smaller)
    inner_width = half_width - frame_width
    inner_height = half_height - frame_width
    inner_depth = half_depth
    
    inner_vertices = create_box_vertices(
        inner_width, inner_height, inner_depth,
        offset_x, offset_y, offset_z
    )
    
    # We need to keep the outer faces and remove the inner faces
    # For simplicity, just use the outer box vertices
    vertices.extend(outer_vertices)
    
    return vertices

def create_glass_vertices(half_width, half_height, half_depth, offset_x=0, offset_y=0, offset_z=0):
    """
    Create vertices for a glass panel
    
    Args:
        half_width: Half width of the glass
        half_height: Half height of the glass
        half_depth: Half depth of the glass
        offset_x: X position offset
        offset_y: Y position offset
        offset_z: Z position offset
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # For simplicity, just create a very thin box for the glass
    # We make it very thin in the Z dimension
    glass_vertices = create_box_vertices(
        half_width, half_height, 0.005,  # Very thin
        offset_x, offset_y, offset_z
    )
    
    vertices.extend(glass_vertices)
    
    return vertices

def create_chair_vertices(width, depth, height):
    """
    Create vertices for a chair
    
    Args:
        width: Chair width
        depth: Chair depth
        height: Chair height
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Chair dimensions
    seat_height = height * 0.4
    back_height = height - seat_height
    leg_width = width * 0.1
    
    # Chair seat
    seat_vertices = create_box_vertices(
        width / 2, seat_height * 0.1, depth / 2,
        0, seat_height, 0
    )
    
    # Chair back
    back_vertices = create_box_vertices(
        width / 2, back_height / 2, depth * 0.1,
        0, seat_height + back_height / 2, -depth / 2 + depth * 0.1
    )
    
    # Chair legs (4)
    leg_vertices = []
    
    # Front-left leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, seat_height / 2, leg_width / 2,
        -width / 2 + leg_width / 2, seat_height / 2 - seat_height * 0.1, depth / 2 - leg_width / 2
    ))
    
    # Front-right leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, seat_height / 2, leg_width / 2,
        width / 2 - leg_width / 2, seat_height / 2 - seat_height * 0.1, depth / 2 - leg_width / 2
    ))
    
    # Back-left leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, seat_height / 2, leg_width / 2,
        -width / 2 + leg_width / 2, seat_height / 2 - seat_height * 0.1, -depth / 2 + leg_width / 2
    ))
    
    # Back-right leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, seat_height / 2, leg_width / 2,
        width / 2 - leg_width / 2, seat_height / 2 - seat_height * 0.1, -depth / 2 + leg_width / 2
    ))
    
    # Combine all parts
    vertices.extend(seat_vertices)
    vertices.extend(back_vertices)
    vertices.extend(leg_vertices)
    
    return vertices

def create_table_vertices(width, depth, height):
    """
    Create vertices for a table
    
    Args:
        width: Table width
        depth: Table depth
        height: Table height
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Table dimensions
    top_thickness = height * 0.05
    leg_width = width * 0.05
    
    # Table top
    top_vertices = create_box_vertices(
        width / 2, top_thickness / 2, depth / 2,
        0, height - top_thickness / 2, 0
    )
    
    # Table legs (4)
    leg_vertices = []
    
    # Front-left leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, (height - top_thickness) / 2, leg_width / 2,
        -width / 2 + leg_width, (height - top_thickness) / 2, depth / 2 - leg_width
    ))
    
    # Front-right leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, (height - top_thickness) / 2, leg_width / 2,
        width / 2 - leg_width, (height - top_thickness) / 2, depth / 2 - leg_width
    ))
    
    # Back-left leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, (height - top_thickness) / 2, leg_width / 2,
        -width / 2 + leg_width, (height - top_thickness) / 2, -depth / 2 + leg_width
    ))
    
    # Back-right leg
    leg_vertices.extend(create_box_vertices(
        leg_width / 2, (height - top_thickness) / 2, leg_width / 2,
        width / 2 - leg_width, (height - top_thickness) / 2, -depth / 2 + leg_width
    ))
    
    # Combine all parts
    vertices.extend(top_vertices)
    vertices.extend(leg_vertices)
    
    return vertices

def create_sofa_vertices(width, depth, height, sofa_type):
    """
    Create vertices for a sofa
    
    Args:
        width: Sofa width
        depth: Sofa depth
        height: Sofa height
        sofa_type: Type of sofa
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Sofa dimensions
    seat_height = height * 0.4
    back_height = height - seat_height
    armrest_width = width * 0.1
    
    if sofa_type == "L-Shaped Sofa":
        # Create an L-shaped sofa
        # Main part
        main_width = width * 0.7
        
        # Base
        base_vertices = create_box_vertices(
            main_width / 2, seat_height / 2, depth / 2,
            -width / 2 + main_width / 2, seat_height / 2, 0
        )
        
        # Back
        back_vertices = create_box_vertices(
            main_width / 2, back_height / 2, depth * 0.2,
            -width / 2 + main_width / 2, seat_height + back_height / 2, -depth / 2 + depth * 0.2
        )
        
        # L part (extends to the right)
        l_width = width - main_width
        l_depth = depth * 0.7
        
        # L base
        l_base_vertices = create_box_vertices(
            l_width / 2, seat_height / 2, l_depth / 2,
            main_width / 2, seat_height / 2, depth / 2 - l_depth / 2
        )
        
        # L back
        l_back_vertices = create_box_vertices(
            l_width * 0.2, back_height / 2, l_depth / 2,
            main_width - l_width * 0.2, seat_height + back_height / 2, depth / 2 - l_depth / 2
        )
        
        # Armrests (2)
        armrest_vertices = []
        
        # Left armrest
        armrest_vertices.extend(create_box_vertices(
            armrest_width / 2, (seat_height + back_height * 0.3) / 2, depth / 2,
            -width / 2 + armrest_width / 2, seat_height / 2 + (back_height * 0.3) / 2, 0
        ))
        
        # Right armrest (on the L part)
        armrest_vertices.extend(create_box_vertices(
            armrest_width / 2, (seat_height + back_height * 0.3) / 2, l_depth / 2,
            width / 2 - armrest_width / 2, seat_height / 2 + (back_height * 0.3) / 2, depth / 2 - l_depth / 2
        ))
        
        # Combine all parts
        vertices.extend(base_vertices)
        vertices.extend(back_vertices)
        vertices.extend(l_base_vertices)
        vertices.extend(l_back_vertices)
        vertices.extend(armrest_vertices)
        
    else:
        # Regular sofas (2-seater or 3-seater)
        # Base
        base_vertices = create_box_vertices(
            width / 2, seat_height / 2, depth / 2,
            0, seat_height / 2, 0
        )
        
        # Back
        back_vertices = create_box_vertices(
            width / 2, back_height / 2, depth * 0.2,
            0, seat_height + back_height / 2, -depth / 2 + depth * 0.2
        )
        
        # Armrests (2)
        armrest_vertices = []
        
        # Left armrest
        armrest_vertices.extend(create_box_vertices(
            armrest_width / 2, (seat_height + back_height * 0.3) / 2, depth / 2,
            -width / 2 + armrest_width / 2, seat_height / 2 + (back_height * 0.3) / 2, 0
        ))
        
        # Right armrest
        armrest_vertices.extend(create_box_vertices(
            armrest_width / 2, (seat_height + back_height * 0.3) / 2, depth / 2,
            width / 2 - armrest_width / 2, seat_height / 2 + (back_height * 0.3) / 2, 0
        ))
        
        # Combine all parts
        vertices.extend(base_vertices)
        vertices.extend(back_vertices)
        vertices.extend(armrest_vertices)
    
    return vertices

def create_bed_vertices(width, depth, height):
    """
    Create vertices for a bed
    
    Args:
        width: Bed width
        depth: Bed depth
        height: Bed height
        
    Returns:
        list: Vertex data (position, normal, texcoord)
    """
    vertices = []
    
    # Bed dimensions
    base_height = height * 0.3
    mattress_height = height - base_height
    
    # Bed base
    base_vertices = create_box_vertices(
        width / 2, base_height / 2, depth / 2,
        0, base_height / 2, 0
    )
    
    # Mattress
    mattress_vertices = create_box_vertices(
        width / 2 * 0.95, mattress_height / 2, depth / 2 * 0.95,
        0, base_height + mattress_height / 2, 0
    )
    
    # Headboard
    headboard_height = height * 1.2
    headboard_vertices = create_box_vertices(
        width / 2, headboard_height / 2, depth * 0.05,
        0, headboard_height / 2, -depth / 2 + depth * 0.05
    )
    
    # Combine all parts
    vertices.extend(base_vertices)
    vertices.extend(mattress_vertices)
    vertices.extend(headboard_vertices)
    
    return vertices 