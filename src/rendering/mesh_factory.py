import numpy as np
import OpenGL
from OpenGL import GL as gl
import math
import ctypes

from src.rendering.mesh_factory_utils import (
    create_floor_vertices, create_walls_vertices, create_ceiling_vertices,
    create_box_vertices, create_box_frame_vertices, create_glass_vertices,
    create_chair_vertices, create_table_vertices, create_sofa_vertices, create_bed_vertices
)

class MeshFactory:
    """
    Factory for creating 3D object meshes
    """
    def __init__(self):
        # Texture loading will be added later
        pass
    
    def create_room_mesh(self, width, length, height):
        """
        Create a room mesh (floor, walls, ceiling) with borders for visual distinction
        
        Args:
            width: Room width
            length: Room length
            height: Room height
            
        Returns:
            dict: Dictionary with VAOs and vertex counts
        """
        # Calculate half dimensions for vertex positions
        half_width = width / 2
        half_length = length / 2
        
        # Create floor vertices
        floor_vertices = create_floor_vertices(half_width, half_length)
        
        # Create walls vertices
        walls_vertices = create_walls_vertices(half_width, half_length, height)
        
        # Create ceiling vertices
        ceiling_vertices = create_ceiling_vertices(half_width, half_length, height)
        
        # Create VAOs and VBOs
        floor_vao, floor_vbo = self._create_vao_vbo(floor_vertices)
        walls_vao, walls_vbo = self._create_vao_vbo(walls_vertices)
        ceiling_vao, ceiling_vbo = self._create_vao_vbo(ceiling_vertices)
        
        # Main surface vertices count (each surface has 6 vertices for the main area)
        floor_main_vertex_count = 6
        walls_main_vertex_count_per_wall = 6
        ceiling_main_vertex_count = 6
        
        # Border vertices count (each border has 6 vertices)
        floor_border_vertex_count = 6
        walls_border_vertex_count_per_wall = 6
        ceiling_border_vertex_count = 6
        
        return {
            "floor_vao": floor_vao,
            "floor_vbo": floor_vbo,
            "floor_vertex_count": len(floor_vertices) // 8,  # 8 floats per vertex (3 pos + 3 normal + 2 tex)
            "floor_main_vertex_count": floor_main_vertex_count,
            "floor_border_vertex_count": floor_border_vertex_count,
            
            "walls_vao": walls_vao,
            "walls_vbo": walls_vbo,
            "walls_vertex_count": len(walls_vertices) // 8,
            "walls_main_vertex_count_per_wall": walls_main_vertex_count_per_wall,
            "walls_border_vertex_count_per_wall": walls_border_vertex_count_per_wall,
            
            "ceiling_vao": ceiling_vao,
            "ceiling_vbo": ceiling_vbo,
            "ceiling_vertex_count": len(ceiling_vertices) // 8,
            "ceiling_main_vertex_count": ceiling_main_vertex_count,
            "ceiling_border_vertex_count": ceiling_border_vertex_count
        }
    
    def create_door_mesh(self, door_type, width, height, thickness=0.1):
        """
        Create a mesh for a door
        
        Args:
            door_type: Type of door (single, double, sliding)
            width: Door width
            height: Door height
            thickness: Door thickness
            
        Returns:
            Dictionary with VAO, VBO, and vertex count
        """
        print(f"Creating door mesh: {door_type}, {width}x{height}")
        
        # Create door geometry based on type
        vertices = []
        
        # Frame width (thickness of the door frame)
        frame_width = 0.05
        
        # Set normal for proper lighting
        normal = [0.0, 0.0, 1.0]
        
        # Set texture coordinates
        tex_coords = [0.0, 0.0]  # Default texture coordinates
        
        # Generate vertices for the door based on its type
        if door_type == "Single Door":
            # Door frame - outer rectangle
            self._create_door_frame(vertices, width, height, thickness, frame_width)
            
            # Door panel - inner rectangle
            panel_width = width - 2 * frame_width
            panel_height = height - 2 * frame_width
            panel_offset_x = 0.0
            panel_offset_y = 0.0
            panel_offset_z = thickness * 0.1  # Slightly offset to avoid z-fighting
            
            # Create panel vertices
            self._create_door_panel(vertices, panel_width, panel_height, thickness * 0.8, 
                                   panel_offset_x, panel_offset_y, panel_offset_z)
            
        elif door_type == "Double Door":
            # Total width is for both doors combined
            half_width = width / 2.0
            gap = 0.01  # Small gap between doors
            
            # Left door
            left_width = half_width - gap/2
            # Left door frame
            self._create_door_frame(vertices, left_width, height, thickness, frame_width, -half_width/2 + left_width/2, 0, 0)
            # Left door panel
            panel_width = left_width - 2 * frame_width
            panel_height = height - 2 * frame_width
            panel_offset_x = -half_width/2 + left_width/2
            self._create_door_panel(vertices, panel_width, panel_height, thickness * 0.8, 
                                   panel_offset_x, 0, thickness * 0.1)
            
            # Right door
            right_width = half_width - gap/2
            # Right door frame
            self._create_door_frame(vertices, right_width, height, thickness, frame_width, half_width/2 - right_width/2, 0, 0)
            # Right door panel
            panel_width = right_width - 2 * frame_width
            panel_height = height - 2 * frame_width
            panel_offset_x = half_width/2 - right_width/2
            self._create_door_panel(vertices, panel_width, panel_height, thickness * 0.8, 
                                   panel_offset_x, 0, thickness * 0.1)
            
        elif door_type == "Sliding Door":
            # Sliding door requires a track
            track_height = height + 0.1
            track_width = width + 0.1
            track_thickness = thickness * 0.5
            
            # Create track at the top
            self._create_block_vertices(vertices, track_width, 0.05, track_thickness, 
                                       0, height/2 + 0.025, 0)
            
            # Door panels (two overlapping panels)
            panel_width = width * 0.6
            panel_height = height - 0.05  # Slightly shorter to fit under track
            
            # Left panel (in front)
            self._create_door_frame(vertices, panel_width, panel_height, thickness * 0.6, 
                                   frame_width, -width/4, -0.025, thickness * 0.1)
            self._create_door_panel(vertices, panel_width - 2 * frame_width, panel_height - 2 * frame_width, 
                                   thickness * 0.4, -width/4, -0.025, thickness * 0.2)
            
            # Right panel (behind)
            self._create_door_frame(vertices, panel_width, panel_height, thickness * 0.6, 
                                   frame_width, width/4, -0.025, -thickness * 0.1)
            self._create_door_panel(vertices, panel_width - 2 * frame_width, panel_height - 2 * frame_width, 
                                   thickness * 0.4, width/4, -0.025, -thickness * 0.2)
        else:  # Default to single door
            self._create_door_frame(vertices, width, height, thickness, frame_width)
            panel_width = width - 2 * frame_width
            panel_height = height - 2 * frame_width
            self._create_door_panel(vertices, panel_width, panel_height, thickness * 0.8, 0, 0, thickness * 0.1)
        
        # Create VAO and VBO
        vao = gl.glGenVertexArrays(1)
        gl.glBindVertexArray(vao)
        
        vbo = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        
        # Convert vertices to numpy array
        vertices_array = np.array(vertices, dtype=np.float32)
        
        # Upload data to GPU
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER, 
            vertices_array.nbytes, 
            vertices_array, 
            gl.GL_STATIC_DRAW
        )
        
        # Position attribute
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * 4, None)
        gl.glEnableVertexAttribArray(0)
        
        # Normal attribute
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        gl.glEnableVertexAttribArray(1)
        
        # Texture attribute
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
        gl.glEnableVertexAttribArray(2)
        
        # Unbind
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)
        
        return {
            "vao": vao,
            "vbo": vbo,
            "vertex_count": len(vertices) // 8
        }
        
    def _create_door_frame(self, vertices, width, height, thickness, frame_width, offset_x=0, offset_y=0, offset_z=0):
        """Create vertices for a door frame"""
        # Outer rectangle
        outer_width = width
        outer_height = height
        
        # Inner rectangle
        inner_width = width - 2 * frame_width
        inner_height = height - 2 * frame_width
        
        # Bottom frame
        self._create_block_vertices(
            vertices, 
            outer_width, 
            frame_width, 
            thickness,
            offset_x,
            offset_y - outer_height/2 + frame_width/2,
            offset_z
        )
        
        # Top frame
        self._create_block_vertices(
            vertices, 
            outer_width, 
            frame_width, 
            thickness,
            offset_x,
            offset_y + outer_height/2 - frame_width/2,
            offset_z
        )
        
        # Left frame
        self._create_block_vertices(
            vertices, 
            frame_width, 
            inner_height, 
            thickness,
            offset_x - outer_width/2 + frame_width/2,
            offset_y,
            offset_z
        )
        
        # Right frame
        self._create_block_vertices(
            vertices, 
            frame_width, 
            inner_height, 
            thickness,
            offset_x + outer_width/2 - frame_width/2,
            offset_y,
            offset_z
        )
        
    def _create_door_panel(self, vertices, width, height, thickness, offset_x=0, offset_y=0, offset_z=0):
        """Create vertices for a door panel"""
        # Panel base
        self._create_block_vertices(
            vertices, 
            width, 
            height, 
            thickness,
            offset_x,
            offset_y,
            offset_z
        )
        
        # Add decorative details for the panel
        # For example, add a raised rectangular panel in the middle
        panel_inset = min(width, height) * 0.15
        panel_detail_width = width - panel_inset * 2
        panel_detail_height = height - panel_inset * 2
        
        if panel_detail_width > 0.1 and panel_detail_height > 0.1:
            self._create_block_vertices(
                vertices, 
                panel_detail_width, 
                panel_detail_height, 
                thickness * 0.3,
                offset_x,
                offset_y,
                offset_z + thickness * 0.5
            )
    
    def create_window_mesh(self, window_type, width, height, thickness=0.05, segments=1):
        """
        Create a mesh for a window
        
        Args:
            window_type: Type of window (single, double, sliding, bay)
            width: Window width
            height: Window height
            thickness: Window thickness
            segments: Number of glass panes/segments
            
        Returns:
            Dictionary with VAOs, VBOs, and vertex counts for frame and glass
        """
        print(f"Creating window mesh: {window_type}, {width}x{height}")
        
        # Create separate vertices for frame and glass
        frame_vertices = []
        glass_vertices = []
        
        # Frame dimensions
        frame_thickness = thickness * 2  # Thicker frame for more realistic appearance
        frame_width = 0.06  # Slightly wider frame border

        # Make windows always face outward and align with wall
        wall_offset = 0.02  # Small offset from wall surface
        
        # Create a proper window based on type
        if window_type == "Single Window":
            # Create main outer frame
            outer_frame_depth = frame_thickness * 1.5
            
            # Create outer frame (box-like structure)
            self._create_box_frame(
                frame_vertices, 
                width, height, outer_frame_depth,
                0, 0, -outer_frame_depth/2 + wall_offset
            )
            
            # Create inner frame
            inner_width = width - frame_width * 2
            inner_height = height - frame_width * 2
            
            # Create window glass
            glass_inset = frame_thickness * 0.2
            self._create_glass_pane(
                glass_vertices, 
                inner_width - 0.01, inner_height - 0.01, thickness / 4,
                0, 0, -glass_inset + wall_offset
            )
            
            # Add window sill
            sill_depth = frame_thickness * 4
            sill_height = frame_width * 1.2
            sill_width = width + frame_width * 1.5
            
            # Main sill (bottom ledge)
            self._create_block_vertices(
                frame_vertices,
                sill_width,
                sill_height,
                sill_depth,
                0, -height/2 - sill_height/2, -sill_depth/2 + wall_offset
            )
            
            # Top trim
            trim_height = frame_width * 0.4
            self._create_block_vertices(
                frame_vertices,
                width + frame_width * 0.5,
                trim_height,
                frame_thickness * 1.2,
                0, height/2 + trim_height/2, wall_offset
            )
            
        elif window_type == "Double Window":
            # Create main outer frame with proper depth
            outer_frame_depth = frame_thickness * 1.5
            
            # Create outer frame (box-like structure)
            self._create_box_frame(
                frame_vertices, 
                width, height, outer_frame_depth,
                0, 0, -outer_frame_depth/2 + wall_offset
            )
            
            # Calculate dimensions for two window panes
            inner_width = width - frame_width * 2
            inner_height = height - frame_width * 2
            pane_width = inner_width / 2 - frame_width/2
            
            # Middle divider
            self._create_block_vertices(
                frame_vertices,
                frame_width,
                inner_height,
                frame_thickness * 1.2,
                0, 0, wall_offset
            )
            
            # Left pane
            glass_inset = frame_thickness * 0.2
            self._create_glass_pane(
                glass_vertices, 
                pane_width - 0.01, inner_height - 0.01, thickness / 4,
                -pane_width/2 - frame_width/2, 0, -glass_inset + wall_offset
            )
            
            # Right pane
            self._create_glass_pane(
                glass_vertices, 
                pane_width - 0.01, inner_height - 0.01, thickness / 4,
                pane_width/2 + frame_width/2, 0, -glass_inset + wall_offset
            )
            
            # Add window handle to right pane
            handle_size = frame_width * 0.6
            self._create_block_vertices(
                frame_vertices,
                handle_size,
                handle_size,
                frame_thickness,
                pane_width/2 + frame_width/2, 0, frame_thickness * 0.6 + wall_offset
            )
            
            # Add window sill
            sill_depth = frame_thickness * 4
            sill_height = frame_width * 1.2
            sill_width = width + frame_width * 1.5
            
            # Main sill (bottom ledge)
            self._create_block_vertices(
                frame_vertices,
                sill_width,
                sill_height,
                sill_depth,
                0, -height/2 - sill_height/2, -sill_depth/2 + wall_offset
            )
            
            # Top trim
            trim_height = frame_width * 0.4
            self._create_block_vertices(
                frame_vertices,
                width + frame_width * 0.5,
                trim_height,
                frame_thickness * 1.2,
                0, height/2 + trim_height/2, wall_offset
            )
        
        elif window_type == "Bay Window":
            # Bay window has a center section and angled sides
            bay_depth = width / 3
            center_width = width / 2
            
            # Create center panel
            self._create_box_frame(
                frame_vertices, 
                center_width, height, frame_thickness * 1.5,
                0, 0, -bay_depth
            )
            
            # Center glass
            inner_width = center_width - frame_width * 2
            inner_height = height - frame_width * 2
            glass_inset = frame_thickness * 0.2
            
            self._create_glass_pane(
                glass_vertices, 
                inner_width - 0.01, inner_height - 0.01, thickness / 4,
                0, 0, -bay_depth - glass_inset
            )
            
            # Side panels (at 45-degree angles)
            side_width = width / 3
            angle = math.radians(45)
            
            # Left panel
            offset_x = -(center_width/2 + side_width/2 * math.cos(angle))
            offset_z = -bay_depth + side_width/2 * math.sin(angle)
            
            self._create_box_frame(
                frame_vertices, 
                side_width, height, frame_thickness * 1.5,
                offset_x, 0, offset_z,
                0, angle, 0
            )
            
            # Left glass
            inner_side_width = side_width - frame_width * 2
            self._create_glass_pane(
                glass_vertices, 
                inner_side_width - 0.01, inner_height - 0.01, thickness / 4,
                offset_x, 0, offset_z - glass_inset,
                0, angle, 0
            )
            
            # Right panel
            offset_x = (center_width/2 + side_width/2 * math.cos(angle))
            
            self._create_box_frame(
                frame_vertices, 
                side_width, height, frame_thickness * 1.5,
                offset_x, 0, offset_z,
                0, -angle, 0
            )
            
            # Right glass
            self._create_glass_pane(
                glass_vertices, 
                inner_side_width - 0.01, inner_height - 0.01, thickness / 4,
                offset_x, 0, offset_z - glass_inset,
                0, -angle, 0
            )
            
            # Add bay window sill (continuous across all sections)
            sill_depth = frame_thickness * 3
            sill_height = frame_width * 1.2
            
            # Center sill
            self._create_block_vertices(
                frame_vertices,
                center_width + frame_width,
                sill_height,
                sill_depth,
                0, -height/2 - sill_height/2, -bay_depth - sill_depth/2
            )
            
            # Side sills
            side_sill_width = side_width + frame_width
            side_sill_depth = sill_depth * 1.2
            
            # Left sill
            self._create_block_vertices(
                frame_vertices,
                side_sill_width,
                sill_height,
                side_sill_depth,
                offset_x, -height/2 - sill_height/2, offset_z - side_sill_depth/2,
                0, angle, 0
            )
            
            # Right sill
            self._create_block_vertices(
                frame_vertices,
                side_sill_width,
                sill_height,
                side_sill_depth,
                offset_x, -height/2 - sill_height/2, offset_z - side_sill_depth/2,
                0, -angle, 0
            )
        
        elif window_type == "Sliding Window":
            # Create main outer frame with proper depth
            outer_frame_depth = frame_thickness * 1.5
            
            # Create outer frame (box-like structure)
            self._create_box_frame(
                frame_vertices, 
                width, height, outer_frame_depth,
                0, 0, -outer_frame_depth/2 + wall_offset
            )
            
            # Create inner frame dimensions
            inner_width = width - frame_width * 2
            inner_height = height - frame_width * 2
            pane_width = inner_width / 2
            
            # Create sliding tracks at top and bottom
            track_height = frame_width * 0.4
            track_depth = frame_thickness * 1.2
            
            # Top track
            self._create_block_vertices(
                frame_vertices,
                inner_width,
                track_height,
                track_depth,
                0, inner_height/2 - track_height/2, wall_offset
            )
            
            # Bottom track
            self._create_block_vertices(
                frame_vertices,
                inner_width,
                track_height,
                track_depth,
                0, -inner_height/2 + track_height/2, wall_offset
            )
            
            # Left pane (front)
            glass_inset = frame_thickness * 0.2
            self._create_glass_pane(
                glass_vertices, 
                pane_width - 0.02, inner_height - track_height*2 - 0.02, thickness / 4,
                -pane_width/4, 0, glass_inset + wall_offset
            )
            
            # Right pane (back)
            self._create_glass_pane(
                glass_vertices, 
                pane_width - 0.02, inner_height - track_height*2 - 0.02, thickness / 4,
                pane_width/4, 0, -glass_inset + wall_offset
            )
            
            # Add window sill
            sill_depth = frame_thickness * 4
            sill_height = frame_width * 1.2
            sill_width = width + frame_width * 1.5
            
            # Main sill (bottom ledge)
            self._create_block_vertices(
                frame_vertices,
                sill_width,
                sill_height,
                sill_depth,
                0, -height/2 - sill_height/2, -sill_depth/2 + wall_offset
            )
        
        else:  # Default to single window if type not recognized
            # Create outer frame (box-like structure)
            outer_frame_depth = frame_thickness * 1.5
            self._create_box_frame(
                frame_vertices, 
                width, height, outer_frame_depth,
                0, 0, -outer_frame_depth/2 + wall_offset
            )
            
            # Create window glass
            inner_width = width - frame_width * 2
            inner_height = height - frame_width * 2
            glass_inset = frame_thickness * 0.2
            
            self._create_glass_pane(
                glass_vertices, 
                inner_width - 0.01, inner_height - 0.01, thickness / 4,
                0, 0, -glass_inset + wall_offset
            )
            
            # Add window sill
            sill_depth = frame_thickness * 4
            sill_height = frame_width * 1.2
            sill_width = width + frame_width * 1.5
            
            # Main sill (bottom ledge)
            self._create_block_vertices(
                frame_vertices,
                sill_width,
                sill_height,
                sill_depth,
                0, -height/2 - sill_height/2, -sill_depth/2 + wall_offset
            )
        
        # Create VAO and VBO for the frame
        frame_vao, frame_vbo = self._create_vao_vbo(frame_vertices)
        
        # Create VAO and VBO for the glass
        glass_vao, glass_vbo = self._create_vao_vbo(glass_vertices)
        
        return {
            "frame_vao": frame_vao,
            "frame_vbo": frame_vbo,
            "frame_vertex_count": len(frame_vertices) // 8,  # 8 floats per vertex
            "glass_vao": glass_vao,
            "glass_vbo": glass_vbo,
            "glass_vertex_count": len(glass_vertices) // 8
        }
    
    def create_furniture_mesh(self, furniture_type, width, depth, height):
        """
        Create furniture mesh
        
        Args:
            furniture_type: Type of furniture
            width: Furniture width
            depth: Furniture depth
            height: Furniture height
            
        Returns:
            dict: Dictionary with VAO, VBO and vertex count
        """
        vertices = []
        
        # Basic furniture shapes based on type
        if furniture_type in ["Dining Chair", "Office Chair", "Armchair"]:
            # Chair: seat and back
            vertices = create_chair_vertices(width, depth, height)
            
        elif furniture_type in ["Dining Table", "Coffee Table", "Desk"]:
            # Table: top and legs
            vertices = create_table_vertices(width, depth, height)
            
        elif furniture_type in ["2-Seater Sofa", "3-Seater Sofa", "L-Shaped Sofa"]:
            # Sofa: base, back and armrests
            vertices = create_sofa_vertices(width, depth, height, furniture_type)
            
        elif furniture_type in ["Single Bed", "Double Bed", "King Size Bed"]:
            # Bed: base and mattress
            vertices = create_bed_vertices(width, depth, height)
            
        else:
            # Default box shape for unknown furniture
            vertices = create_box_vertices(
                width / 2, height / 2, depth / 2,
                0, height / 2, 0
            )
        
        # Create VAO and VBO
        vao, vbo = self._create_vao_vbo(vertices)
        
        return {
            "vao": vao,
            "vbo": vbo,
            "vertex_count": len(vertices) // 8  # 8 floats per vertex
        }
    
    def _create_vao_vbo(self, vertices):
        """
        Create VAO and VBO for vertex data
        
        Args:
            vertices: List of vertex data (position, normal, texcoord)
            
        Returns:
            tuple: (VAO ID, VBO ID)
        """
        # Convert to numpy array
        vertices = np.array(vertices, dtype=np.float32)
        
        # Create VAO and VBO
        vao = gl.glGenVertexArrays(1)
        vbo = gl.glGenBuffers(1)
        
        # Bind VAO
        gl.glBindVertexArray(vao)
        
        # Bind VBO and upload data
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
        gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
        
        # Position attribute (3 floats)
        gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * 4, None)
        gl.glEnableVertexAttribArray(0)
        
        # Normal attribute (3 floats)
        gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))
        gl.glEnableVertexAttribArray(1)
        
        # Texture coordinate attribute (2 floats)
        gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))
        gl.glEnableVertexAttribArray(2)
        
        # Unbind
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindVertexArray(0)
        
        return vao, vbo

    def _create_block_vertices(self, vertices, width, height, depth, offset_x=0, offset_y=0, offset_z=0, x_rot=0, y_rot=0, z_rot=0):
        """
        Create vertices for a block/box
        
        Args:
            vertices: List to append vertices to
            width: Block width (X)
            height: Block height (Y)
            depth: Block depth (Z)
            offset_x: X position offset
            offset_y: Y position offset
            offset_z: Z position offset
            x_rot: Rotation around x-axis in radians
            y_rot: Rotation around y-axis in radians
            z_rot: Rotation around z-axis in radians
        """
        # Half dimensions
        half_width = width / 2.0
        half_height = height / 2.0
        half_depth = depth / 2.0
        
        # Define the 8 corners of the block
        x_min = -half_width
        x_max = half_width
        y_min = -half_height
        y_max = half_height
        z_min = -half_depth
        z_max = half_depth
        
        # Apply rotation matrix to each position
        # Using numpy for rotation to simplify the implementation
        import numpy as np
        from math import cos, sin
        
        # Create rotation matrices
        def create_rotation_matrix(x_angle, y_angle, z_angle):
            # X rotation matrix
            rx = np.array([
                [1, 0, 0],
                [0, cos(x_angle), -sin(x_angle)],
                [0, sin(x_angle), cos(x_angle)]
            ])
            
            # Y rotation matrix
            ry = np.array([
                [cos(y_angle), 0, sin(y_angle)],
                [0, 1, 0],
                [-sin(y_angle), 0, cos(y_angle)]
            ])
            
            # Z rotation matrix
            rz = np.array([
                [cos(z_angle), -sin(z_angle), 0],
                [sin(z_angle), cos(z_angle), 0],
                [0, 0, 1]
            ])
            
            # Combined rotation matrix: R = Rz * Ry * Rx
            combined = np.matmul(rz, np.matmul(ry, rx))
            return combined
        
        # Create the rotation matrix
        rot_matrix = create_rotation_matrix(x_rot, y_rot, z_rot)
        
        # Function to rotate a point
        def rotate_point(point):
            rotated = np.matmul(rot_matrix, np.array(point))
            return rotated
        
        # Rotate normal vectors as well
        front_normal = rotate_point([0, 0, 1])
        back_normal = rotate_point([0, 0, -1])
        right_normal = rotate_point([1, 0, 0])
        left_normal = rotate_point([-1, 0, 0])
        top_normal = rotate_point([0, 1, 0])
        bottom_normal = rotate_point([0, -1, 0])
        
        # Helper function to create a vertex with rotation and offset
        def create_vertex(x, y, z, normal):
            # Rotate the position
            pos = rotate_point([x, y, z])
            # Add offset
            pos_x = pos[0] + offset_x
            pos_y = pos[1] + offset_y
            pos_z = pos[2] + offset_z
            # Return vertex data
            return [pos_x, pos_y, pos_z, normal[0], normal[1], normal[2]]
        
        # Define front face vertices (positive Z)
        # Triangle 1
        # Position, Normal, Texture
        v1 = create_vertex(x_min, y_min, z_max, front_normal)
        v2 = create_vertex(x_max, y_min, z_max, front_normal)
        v3 = create_vertex(x_max, y_max, z_max, front_normal)
        vertices.extend(v1 + [0, 0])
        vertices.extend(v2 + [1, 0])
        vertices.extend(v3 + [1, 1])
        # Triangle 2
        v4 = create_vertex(x_min, y_min, z_max, front_normal)
        v5 = create_vertex(x_max, y_max, z_max, front_normal)
        v6 = create_vertex(x_min, y_max, z_max, front_normal)
        vertices.extend(v4 + [0, 0])
        vertices.extend(v5 + [1, 1])
        vertices.extend(v6 + [0, 1])
        
        # Define back face vertices (negative Z)
        # Triangle 1
        v1 = create_vertex(x_max, y_min, z_min, back_normal)
        v2 = create_vertex(x_min, y_min, z_min, back_normal)
        v3 = create_vertex(x_min, y_max, z_min, back_normal)
        vertices.extend(v1 + [0, 0])
        vertices.extend(v2 + [1, 0])
        vertices.extend(v3 + [1, 1])
        # Triangle 2
        v4 = create_vertex(x_max, y_min, z_min, back_normal)
        v5 = create_vertex(x_min, y_max, z_min, back_normal)
        v6 = create_vertex(x_max, y_max, z_min, back_normal)
        vertices.extend(v4 + [0, 0])
        vertices.extend(v5 + [1, 1])
        vertices.extend(v6 + [0, 1])
        
        # Define right face vertices (positive X)
        # Triangle 1
        v1 = create_vertex(x_max, y_min, z_max, right_normal)
        v2 = create_vertex(x_max, y_min, z_min, right_normal)
        v3 = create_vertex(x_max, y_max, z_min, right_normal)
        vertices.extend(v1 + [0, 0])
        vertices.extend(v2 + [1, 0])
        vertices.extend(v3 + [1, 1])
        # Triangle 2
        v4 = create_vertex(x_max, y_min, z_max, right_normal)
        v5 = create_vertex(x_max, y_max, z_min, right_normal)
        v6 = create_vertex(x_max, y_max, z_max, right_normal)
        vertices.extend(v4 + [0, 0])
        vertices.extend(v5 + [1, 1])
        vertices.extend(v6 + [0, 1])
        
        # Define left face vertices (negative X)
        # Triangle 1
        v1 = create_vertex(x_min, y_min, z_min, left_normal)
        v2 = create_vertex(x_min, y_min, z_max, left_normal)
        v3 = create_vertex(x_min, y_max, z_max, left_normal)
        vertices.extend(v1 + [0, 0])
        vertices.extend(v2 + [1, 0])
        vertices.extend(v3 + [1, 1])
        # Triangle 2
        v4 = create_vertex(x_min, y_min, z_min, left_normal)
        v5 = create_vertex(x_min, y_max, z_max, left_normal)
        v6 = create_vertex(x_min, y_max, z_min, left_normal)
        vertices.extend(v4 + [0, 0])
        vertices.extend(v5 + [1, 1])
        vertices.extend(v6 + [0, 1])
        
        # Define top face vertices (positive Y)
        # Triangle 1
        v1 = create_vertex(x_min, y_max, z_max, top_normal)
        v2 = create_vertex(x_max, y_max, z_max, top_normal)
        v3 = create_vertex(x_max, y_max, z_min, top_normal)
        vertices.extend(v1 + [0, 0])
        vertices.extend(v2 + [1, 0])
        vertices.extend(v3 + [1, 1])
        # Triangle 2
        v4 = create_vertex(x_min, y_max, z_max, top_normal)
        v5 = create_vertex(x_max, y_max, z_min, top_normal)
        v6 = create_vertex(x_min, y_max, z_min, top_normal)
        vertices.extend(v4 + [0, 0])
        vertices.extend(v5 + [1, 1])
        vertices.extend(v6 + [0, 1])
        
        # Define bottom face vertices (negative Y)
        # Triangle 1
        v1 = create_vertex(x_min, y_min, z_min, bottom_normal)
        v2 = create_vertex(x_max, y_min, z_min, bottom_normal)
        v3 = create_vertex(x_max, y_min, z_max, bottom_normal)
        vertices.extend(v1 + [0, 0])
        vertices.extend(v2 + [1, 0])
        vertices.extend(v3 + [1, 1])
        # Triangle 2
        v4 = create_vertex(x_min, y_min, z_min, bottom_normal)
        v5 = create_vertex(x_max, y_min, z_max, bottom_normal)
        v6 = create_vertex(x_min, y_min, z_max, bottom_normal)
        vertices.extend(v4 + [0, 0])
        vertices.extend(v5 + [1, 1])
        vertices.extend(v6 + [0, 1])
        
        # Return the number of vertices added (36 = 6 faces × 2 triangles × 3 vertices)
        return 36

    def _create_box_frame(self, vertices, width, height, depth, 
                        x_offset=0, y_offset=0, z_offset=0,
                        x_rot=0, y_rot=0, z_rot=0):
        """
        Create a box-shaped window frame with hollow center
        
        Args:
            vertices: List to append vertices to
            width: Frame width
            height: Frame height
            depth: Frame depth
            x_offset, y_offset, z_offset: Position offsets
            x_rot, y_rot, z_rot: Rotation angles in radians
        """
        # Frame dimensions
        frame_width = 0.06  # Width of frame border
        
        # Outer dimensions
        outer_width = width
        outer_height = height
        
        # Inner dimensions
        inner_width = width - frame_width * 2
        inner_height = height - frame_width * 2
        
        # Top horizontal
        self._create_block_vertices(vertices, outer_width, frame_width, depth,
                                  x_offset, y_offset + outer_height/2 - frame_width/2, z_offset)
        
        # Bottom horizontal
        self._create_block_vertices(vertices, outer_width, frame_width, depth,
                                  x_offset, y_offset - outer_height/2 + frame_width/2, z_offset)
        
        # Left vertical
        self._create_block_vertices(vertices, frame_width, outer_height - frame_width*2, depth,
                                  x_offset - outer_width/2 + frame_width/2, y_offset, z_offset)
        
        # Right vertical
        self._create_block_vertices(vertices, frame_width, outer_height - frame_width*2, depth,
                                  x_offset + outer_width/2 - frame_width/2, y_offset, z_offset)
    
    def _create_glass_pane(self, vertices, width, height, thickness,
                         x_offset=0, y_offset=0, z_offset=0,
                         x_rot=0, y_rot=0, z_rot=0):
        """
        Create vertices for a glass pane with enhanced realism
        
        Args:
            vertices: List to append vertices to
            width: Glass width
            height: Glass height
            thickness: Glass thickness
            x_offset, y_offset, z_offset: Position offsets
            x_rot, y_rot, z_rot: Rotation in degrees
        """
        # Create a thin block for the glass with slight variations for realism
        half_width = width / 2
        half_height = height / 2
        half_thickness = thickness / 2
        
        # Define the 8 corners of the glass
        corners = [
            # Front face corners
            [x_offset - half_width, y_offset - half_height, z_offset + half_thickness],  # Bottom-left
            [x_offset + half_width, y_offset - half_height, z_offset + half_thickness],  # Bottom-right
            [x_offset + half_width, y_offset + half_height, z_offset + half_thickness],  # Top-right
            [x_offset - half_width, y_offset + half_height, z_offset + half_thickness],  # Top-left
            
            # Back face corners (with very slight randomness for realism - microvariations)
            [x_offset - half_width - 0.0008, y_offset - half_height - 0.0008, z_offset - half_thickness],  # Bottom-left
            [x_offset + half_width + 0.0008, y_offset - half_height - 0.0008, z_offset - half_thickness],  # Bottom-right
            [x_offset + half_width + 0.0008, y_offset + half_height + 0.0008, z_offset - half_thickness],  # Top-right
            [x_offset - half_width - 0.0008, y_offset + half_height + 0.0008, z_offset - half_thickness],  # Top-left
        ]
        
        # Enhanced normals for better light interaction - adjusted for optimal Fresnel effect
        # Slight variations in normals create more realistic reflections and refractions
        normals = [
            [0, 0, 1.0],      # Front face - perfectly flat
            [0, 0, -1.0],     # Back face - perfectly flat
            [1.0, 0, 0.015],  # Right face - slight angle for better reflection
            [-1.0, 0, 0.015], # Left face - slight angle for better reflection
            [0, 1.0, 0.015],  # Top face - slight angle for better reflection
            [0, -1.0, 0.015], # Bottom face - slight angle for better reflection
        ]
        
        # Define the 6 faces using indices to corners
        faces = [
            [0, 1, 2, 3],  # Front face
            [5, 4, 7, 6],  # Back face
            [1, 5, 6, 2],  # Right face
            [4, 0, 3, 7],  # Left face
            [3, 2, 6, 7],  # Top face
            [1, 0, 4, 5],  # Bottom face
        ]
        
        # Add subtle randomness to texture coordinates for glass imperfections
        # This creates tiny distortions in reflections, simulating real glass irregularities
        def add_subtle_variation():
            return (np.random.random() - 0.5) * 0.005
            
        # Create vertices for each face as two triangles with enhanced texture mapping
        for face_idx, face in enumerate(faces):
            normal = normals[face_idx]
            
            # Different texture coordinate mapping for front/back vs sides for better reflections
            # Front/back faces use full texture range for proper environmental reflections
            tex_scale = 1.0
            if face_idx <= 1:  # Front or back face
                tex_coords = [
                    [0.0 + add_subtle_variation(), 0.0 + add_subtle_variation()], 
                    [1.0 + add_subtle_variation(), 0.0 + add_subtle_variation()], 
                    [1.0 + add_subtle_variation(), 1.0 + add_subtle_variation()], 
                    [0.0 + add_subtle_variation(), 1.0 + add_subtle_variation()]
                ]
            else:  # Side faces (specialized texture mapping for edge reflections)
                edge_factor = 0.05  # Smaller value for better edge highlight effect
                tex_coords = [
                    [0.0, 0.0], 
                    [thickness * tex_scale * edge_factor, 0.0], 
                    [thickness * tex_scale * edge_factor, 1.0], 
                    [0.0, 1.0]
                ]
            
            # First triangle
            vertices.extend([
                corners[face[0]][0], corners[face[0]][1], corners[face[0]][2],  # Position
                normal[0], normal[1], normal[2],  # Normal
                tex_coords[0][0], tex_coords[0][1]  # Enhanced texture coordinates
            ])
            
            vertices.extend([
                corners[face[1]][0], corners[face[1]][1], corners[face[1]][2],
                normal[0], normal[1], normal[2],
                tex_coords[1][0], tex_coords[1][1]
            ])
            
            vertices.extend([
                corners[face[2]][0], corners[face[2]][1], corners[face[2]][2],
                normal[0], normal[1], normal[2],
                tex_coords[2][0], tex_coords[2][1]
            ])
            
            # Second triangle
            vertices.extend([
                corners[face[0]][0], corners[face[0]][1], corners[face[0]][2],
                normal[0], normal[1], normal[2],
                tex_coords[0][0], tex_coords[0][1]
            ])
            
            vertices.extend([
                corners[face[2]][0], corners[face[2]][1], corners[face[2]][2],
                normal[0], normal[1], normal[2],
                tex_coords[2][0], tex_coords[2][1]
            ])
            
            vertices.extend([
                corners[face[3]][0], corners[face[3]][1], corners[face[3]][2],
                normal[0], normal[1], normal[2],
                tex_coords[3][0], tex_coords[3][1]
            ])
        
        # Add double-glazing effect (modern windows)
        # Distance between the panes - optimized for realistic refraction
        internal_offset = half_thickness * 0.5  # Slightly larger gap for more realistic appearance
        
        # Create inner glass pane for double-glazing effect
        # Slightly smaller than outer pane to create a visible edge
        scale_factor = 0.97  # Scale factor to create visible frame between panes
        inner_corners = [
            # Front face (inner)
            [x_offset - half_width * scale_factor, y_offset - half_height * scale_factor, z_offset + internal_offset],
            [x_offset + half_width * scale_factor, y_offset - half_height * scale_factor, z_offset + internal_offset],
            [x_offset + half_width * scale_factor, y_offset + half_height * scale_factor, z_offset + internal_offset],
            [x_offset - half_width * scale_factor, y_offset + half_height * scale_factor, z_offset + internal_offset],
            
            # Back face (inner)
            [x_offset - half_width * scale_factor, y_offset - half_height * scale_factor, z_offset - internal_offset],
            [x_offset + half_width * scale_factor, y_offset - half_height * scale_factor, z_offset - internal_offset],
            [x_offset + half_width * scale_factor, y_offset + half_height * scale_factor, z_offset - internal_offset],
            [x_offset - half_width * scale_factor, y_offset + half_height * scale_factor, z_offset - internal_offset],
        ]
        
        # Render all faces of the inner pane for complete double-glazing effect
        inner_faces = [
            [0, 1, 2, 3],  # Front face (inner)
            [5, 4, 7, 6],  # Back face (inner)
            [1, 5, 6, 2],  # Right face (inner)
            [4, 0, 3, 7],  # Left face (inner)
            [3, 2, 6, 7],  # Top face (inner)
            [1, 0, 4, 5],  # Bottom face (inner)
        ]
        
        # Slightly different normals for inner pane to create distinct optical properties
        inner_normals = [
            [0, 0, 1.0],       # Front face
            [0, 0, -1.0],      # Back face
            [1.0, 0, -0.01],   # Right face - reversed slight angle
            [-1.0, 0, -0.01],  # Left face - reversed slight angle
            [0, 1.0, -0.01],   # Top face - reversed slight angle
            [0, -1.0, -0.01],  # Bottom face - reversed slight angle
        ]
        
        # Add inner pane vertices
        for face_idx, face in enumerate(inner_faces):
            normal = inner_normals[face_idx]
            
            # Texture coordinates with subtle randomization for inner pane
            if face_idx <= 1:
                tex_coords = [
                    [0.0 + add_subtle_variation(), 0.0 + add_subtle_variation()], 
                    [1.0 + add_subtle_variation(), 0.0 + add_subtle_variation()], 
                    [1.0 + add_subtle_variation(), 1.0 + add_subtle_variation()], 
                    [0.0 + add_subtle_variation(), 1.0 + add_subtle_variation()]
                ]
            else:
                edge_factor = 0.02  # Smaller for inner pane edge
                tex_coords = [
                    [0.0, 0.0], 
                    [thickness * tex_scale * edge_factor, 0.0], 
                    [thickness * tex_scale * edge_factor, 1.0], 
                    [0.0, 1.0]
                ]
            
            # First triangle
            vertices.extend([
                inner_corners[face[0]][0], inner_corners[face[0]][1], inner_corners[face[0]][2],
                normal[0], normal[1], normal[2],
                tex_coords[0][0], tex_coords[0][1]
            ])
            
            vertices.extend([
                inner_corners[face[1]][0], inner_corners[face[1]][1], inner_corners[face[1]][2],
                normal[0], normal[1], normal[2],
                tex_coords[1][0], tex_coords[1][1]
            ])
            
            vertices.extend([
                inner_corners[face[2]][0], inner_corners[face[2]][1], inner_corners[face[2]][2],
                normal[0], normal[1], normal[2],
                tex_coords[2][0], tex_coords[2][1]
            ])
            
            # Second triangle
            vertices.extend([
                inner_corners[face[0]][0], inner_corners[face[0]][1], inner_corners[face[0]][2],
                normal[0], normal[1], normal[2],
                tex_coords[0][0], tex_coords[0][1]
            ])
            
            vertices.extend([
                inner_corners[face[2]][0], inner_corners[face[2]][1], inner_corners[face[2]][2],
                normal[0], normal[1], normal[2],
                tex_coords[2][0], tex_coords[2][1]
            ])
            
            vertices.extend([
                inner_corners[face[3]][0], inner_corners[face[3]][1], inner_corners[face[3]][2],
                normal[0], normal[1], normal[2],
                tex_coords[3][0], tex_coords[3][1]
            ])
            
        # Add frame spacer between glass panes (the thin aluminum strip in double-glazed windows)
        spacer_width = 0.01
        spacer_corners = [
            # Outer perimeter
            [x_offset - half_width + spacer_width, y_offset - half_height + spacer_width, z_offset + internal_offset * 0.8],
            [x_offset + half_width - spacer_width, y_offset - half_height + spacer_width, z_offset + internal_offset * 0.8],
            [x_offset + half_width - spacer_width, y_offset + half_height - spacer_width, z_offset + internal_offset * 0.8],
            [x_offset - half_width + spacer_width, y_offset + half_height - spacer_width, z_offset + internal_offset * 0.8],
            
            # Inner perimeter
            [x_offset - half_width + spacer_width, y_offset - half_height + spacer_width, z_offset - internal_offset * 0.8],
            [x_offset + half_width - spacer_width, y_offset - half_height + spacer_width, z_offset - internal_offset * 0.8],
            [x_offset + half_width - spacer_width, y_offset + half_height - spacer_width, z_offset - internal_offset * 0.8],
            [x_offset - half_width + spacer_width, y_offset + half_height - spacer_width, z_offset - internal_offset * 0.8],
        ]
        
        # Only create the edge frame (visible at the perimeter)
        spacer_faces = [
            [0, 1, 5, 4],  # Bottom edge
            [3, 2, 6, 7],  # Top edge
            [0, 3, 7, 4],  # Left edge
            [1, 2, 6, 5],  # Right edge
        ]
        
        # Silver/aluminum material for spacer
        spacer_normal = [0.1, 0.1, 0.1]  # Subtle normal for metallic appearance
        
        # Add spacer vertices
        for face_idx, face in enumerate(spacer_faces):
            tex_coords = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
            
            # First triangle
            vertices.extend([
                spacer_corners[face[0]][0], spacer_corners[face[0]][1], spacer_corners[face[0]][2],
                spacer_normal[0], spacer_normal[1], spacer_normal[2],
                tex_coords[0][0], tex_coords[0][1]
            ])
            
            vertices.extend([
                spacer_corners[face[1]][0], spacer_corners[face[1]][1], spacer_corners[face[1]][2],
                spacer_normal[0], spacer_normal[1], spacer_normal[2],
                tex_coords[1][0], tex_coords[1][1]
            ])
            
            vertices.extend([
                spacer_corners[face[2]][0], spacer_corners[face[2]][1], spacer_corners[face[2]][2],
                spacer_normal[0], spacer_normal[1], spacer_normal[2],
                tex_coords[2][0], tex_coords[2][1]
            ])
            
            # Second triangle
            vertices.extend([
                spacer_corners[face[0]][0], spacer_corners[face[0]][1], spacer_corners[face[0]][2],
                spacer_normal[0], spacer_normal[1], spacer_normal[2],
                tex_coords[0][0], tex_coords[0][1]
            ])
            
            vertices.extend([
                spacer_corners[face[2]][0], spacer_corners[face[2]][1], spacer_corners[face[2]][2],
                spacer_normal[0], spacer_normal[1], spacer_normal[2],
                tex_coords[2][0], tex_coords[2][1]
            ])
            
            vertices.extend([
                spacer_corners[face[3]][0], spacer_corners[face[3]][1], spacer_corners[face[3]][2],
                spacer_normal[0], spacer_normal[1], spacer_normal[2],
                tex_coords[3][0], tex_coords[3][1]
            ]) 