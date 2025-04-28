import numpy as np
import OpenGL
from OpenGL import GL as gl
from OpenGL.GL import shaders
from OpenGL.GLU import *
import glm

from src.rendering.shaders import ShaderManager
from src.rendering.mesh_factory import MeshFactory
from src.models.room import Room
from src.models.door import Door
from src.models.window import Window
from src.models.furniture import Furniture
from src.rendering.matrix import length, vec3, value_ptr

class Renderer:
    """
    OpenGL renderer for the 3D scene
    """
    def __init__(self, scene_manager, camera):
        """
        Initialize the renderer
        
        Args:
            scene_manager: SceneManager instance
            camera: Camera instance
        """
        self.scene_manager = scene_manager
        self.camera = camera
        
        # Viewport dimensions
        self.width = 800
        self.height = 600
        
        # OpenGL setup
        self.setup_gl()
        
        # Create shader manager
        self.shader_manager = ShaderManager()
        
        # Create mesh factory
        self.mesh_factory = MeshFactory()
        
        # Initialize shader programs
        self.init_shaders()
        
        # Dictionary to store mesh VAOs
        self.mesh_cache = {}
    
    def setup_gl(self):
        """Set up OpenGL settings"""
        # Enable depth testing
        gl.glEnable(gl.GL_DEPTH_TEST)
        
        # Enable backface culling
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glCullFace(gl.GL_BACK)
        
        # Enable blending for transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Set default clear color (sky blue)
        gl.glClearColor(0.5, 0.7, 1.0, 1.0)
    
    def init_shaders(self):
        """Initialize shader programs"""
        try:
            # Default shader for opaque objects
            self.default_shader = self.shader_manager.create_shader_program("default")
            
            # Shader for transparent objects (like glass)
            self.transparent_shader = self.shader_manager.create_shader_program("transparent")
            
            # Shader for selected objects
            self.selection_shader = self.shader_manager.create_shader_program("selection")
            
            # Get uniform locations
            self.get_uniform_locations()
            
        except Exception as e:
            print(f"Error initializing shaders: {e}")
    
    def get_uniform_locations(self):
        """Get uniform locations from shaders"""
        # Default shader uniforms
        self.default_uniforms = {
            "model": gl.glGetUniformLocation(self.default_shader, "model"),
            "view": gl.glGetUniformLocation(self.default_shader, "view"),
            "projection": gl.glGetUniformLocation(self.default_shader, "projection"),
            "color": gl.glGetUniformLocation(self.default_shader, "color"),
            "use_texture": gl.glGetUniformLocation(self.default_shader, "use_texture"),
            "texture_sampler": gl.glGetUniformLocation(self.default_shader, "texture_sampler")
        }
        
        # Transparent shader uniforms (similar to default, but with alpha handling)
        self.transparent_uniforms = {
            "model": gl.glGetUniformLocation(self.transparent_shader, "model"),
            "view": gl.glGetUniformLocation(self.transparent_shader, "view"),
            "projection": gl.glGetUniformLocation(self.transparent_shader, "projection"),
            "color": gl.glGetUniformLocation(self.transparent_shader, "color"),
            "use_texture": gl.glGetUniformLocation(self.transparent_shader, "use_texture"),
            "texture_sampler": gl.glGetUniformLocation(self.transparent_shader, "texture_sampler")
        }
        
        # Selection shader uniforms
        self.selection_uniforms = {
            "model": gl.glGetUniformLocation(self.selection_shader, "model"),
            "view": gl.glGetUniformLocation(self.selection_shader, "view"),
            "projection": gl.glGetUniformLocation(self.selection_shader, "projection"),
            "highlight_color": gl.glGetUniformLocation(self.selection_shader, "highlight_color")
        }
    
    def resize(self, width, height):
        """
        Handle viewport resize
        
        Args:
            width: New viewport width
            height: New viewport height
        """
        self.width = max(1, width)
        self.height = max(1, height)
        
        # Update OpenGL viewport
        gl.glViewport(0, 0, self.width, self.height)
    
    def render(self):
        """Render the 3D scene"""
        # Clear the color and depth buffers
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        
        # Get camera matrices
        view_matrix = self.camera.view_matrix
        projection_matrix = self.camera.projection_matrix
        
        # Get all objects to render
        all_objects = self.scene_manager.get_all_objects()
        
        # Sort objects: room first, then opaque objects, then transparent objects
        room = None
        opaque_objects = []
        transparent_objects = []
        selected_objects = []
        
        for obj in all_objects:
            if not obj.visible:
                continue
                
            # Check if the object is selected
            if hasattr(obj, 'is_selected') and obj.is_selected:
                selected_objects.append(obj)
                
            if isinstance(obj, Room):
                room = obj
            elif isinstance(obj, Window):
                # Windows have transparent parts (glass)
                transparent_objects.append(obj)
            else:
                opaque_objects.append(obj)
        
        # First render the room
        if room is not None:
            self.render_room(room, view_matrix, projection_matrix)
        
        # Then render opaque objects
        for obj in opaque_objects:
            self.render_object(obj, view_matrix, projection_matrix)
        
        # Finally render transparent objects (back-to-front for proper blending)
        # Sort transparent objects back-to-front for correct alpha blending
        transparent_objects.sort(key=lambda obj: length(self.camera.position - obj.position), reverse=True)
        
        for obj in transparent_objects:
            self.render_transparent_object(obj, view_matrix, projection_matrix)
        
        # Render the selected object outline if any
        for obj in selected_objects:
            self.render_selected_object(obj, view_matrix, projection_matrix)
        
        # Swap buffers (done by the parent system)
    
    def render_room(self, room, view_matrix, projection_matrix):
        """
        Render a room with interior and exterior surfaces clearly distinguishable
        
        Args:
            room: Room object to render
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        # Ensure the room mesh exists
        room_key = f"room_{room.width}_{room.length}_{room.height}"
        if room_key not in self.mesh_cache:
            # Create room mesh and add to cache
            self.mesh_cache[room_key] = self.mesh_factory.create_room_mesh(
                room.width, room.length, room.height
            )
        
        # Get the room mesh
        room_mesh = self.mesh_cache[room_key]
        
        # Bind the default shader
        gl.glUseProgram(self.default_shader)
        
        # Set uniforms
        gl.glUniformMatrix4fv(self.default_uniforms["view"], 1, gl.GL_FALSE, value_ptr(view_matrix))
        gl.glUniformMatrix4fv(self.default_uniforms["projection"], 1, gl.GL_FALSE, value_ptr(projection_matrix))
        gl.glUniformMatrix4fv(self.default_uniforms["model"], 1, gl.GL_FALSE, value_ptr(room.get_model_matrix()))
        
        # Check if camera is inside the room to determine which faces to draw
        camera_pos = self.camera.position
        is_inside = (abs(camera_pos[0]) < room.width/2 and 
                    abs(camera_pos[2]) < room.length/2 and
                    camera_pos[1] < room.height and camera_pos[1] > 0)
        
        # Get vertex counts for main surfaces and borders
        floor_main_count = room_mesh["floor_main_vertex_count"]
        floor_border_count = room_mesh["floor_border_vertex_count"]
        walls_main_count_per_wall = room_mesh["walls_main_vertex_count_per_wall"] 
        walls_border_count_per_wall = room_mesh["walls_border_vertex_count_per_wall"]
        ceiling_main_count = room_mesh["ceiling_main_vertex_count"]
        ceiling_border_count = room_mesh["ceiling_border_vertex_count"]
        
        # Define labels for better visual identification (could be displayed in UI)
        wall_labels = ["West Wall", "East Wall", "North Wall", "South Wall"]
        
        # Choose colors based on camera position (inside or outside)
        if is_inside:
            # Using interior colors when inside the room
            floor_color = room.interior_floor_color
            ceiling_color = room.interior_ceiling_color
            
            wall_colors = [
                (room.interior_west_wall_color, room.wall_opacity, wall_labels[0]),   # -X (west/left) wall
                (room.interior_east_wall_color, room.wall_opacity, wall_labels[1]),   # +X (east/right) wall
                (room.interior_north_wall_color, room.wall_opacity, wall_labels[2]),  # -Z (north/back) wall
                (room.interior_south_wall_color, room.wall_opacity, wall_labels[3]),  # +Z (south/front) wall
            ]
            
            # Disable backface culling to see interior faces
            gl.glDisable(gl.GL_CULL_FACE)
        else:
            # Using exterior colors when outside the room
            floor_color = room.floor_color
            ceiling_color = room.ceiling_color
            
            wall_colors = [
                (room.west_wall_color, room.wall_opacity, wall_labels[0]),   # -X (west/left) wall
                (room.east_wall_color, room.wall_opacity, wall_labels[1]),   # +X (east/right) wall
                (room.north_wall_color, room.wall_opacity, wall_labels[2]),  # -Z (north/back) wall
                (room.south_wall_color, room.wall_opacity, wall_labels[3]),  # +Z (south/front) wall
            ]
            
            # Enable backface culling as normal when outside
            gl.glEnable(gl.GL_CULL_FACE)
        
        # Add wall label positions for identification (could be used for UI tooltips)
        wall_label_positions = [
            [-room.width/2 - 0.1, room.height/2, 0],               # West wall (-X)
            [room.width/2 + 0.1, room.height/2, 0],                # East wall (+X)
            [0, room.height/2, -room.length/2 - 0.1],              # North wall (-Z)
            [0, room.height/2, room.length/2 + 0.1],               # South wall (+Z)
        ]
        
        # For floor - includes main floor and border
        gl.glBindVertexArray(room_mesh["floor_vao"])
        
        # Draw main floor
        gl.glUniform4f(self.default_uniforms["color"], 
                    floor_color[0], floor_color[1], floor_color[2], room.floor_opacity)
        gl.glUniform1i(self.default_uniforms["use_texture"], 0)  # No texture for now
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, floor_main_count)
        
        # Draw floor border (use darker color for contrast)
        gl.glUniform4f(self.default_uniforms["color"], 0.1, 0.1, 0.1, 1.0)  # Dark border color
        gl.glDrawArrays(gl.GL_TRIANGLES, floor_main_count, floor_border_count)
        
        # For walls (draw each wall separately with its own color)
        gl.glBindVertexArray(room_mesh["walls_vao"])
        
        # Draw each wall with its color
        for i, (color, opacity, label) in enumerate(wall_colors):
            # Main wall
            offset = i * walls_main_count_per_wall
            gl.glUniform4f(self.default_uniforms["color"], color[0], color[1], color[2], opacity)
            gl.glDrawArrays(gl.GL_TRIANGLES, offset, walls_main_count_per_wall)
        
        # Draw wall borders (4 walls' worth after the main walls)
        border_start_offset = 4 * walls_main_count_per_wall
        gl.glUniform4f(self.default_uniforms["color"], 0.1, 0.1, 0.1, 1.0)  # Dark border color
        for i in range(4):
            offset = border_start_offset + i * walls_border_count_per_wall
            gl.glDrawArrays(gl.GL_TRIANGLES, offset, walls_border_count_per_wall)
        
        # For ceiling
        gl.glBindVertexArray(room_mesh["ceiling_vao"])
        
        # Draw main ceiling
        gl.glUniform4f(self.default_uniforms["color"], 
                    ceiling_color[0], ceiling_color[1], ceiling_color[2], room.ceiling_opacity)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, ceiling_main_count)
        
        # Draw ceiling border
        gl.glUniform4f(self.default_uniforms["color"], 0.1, 0.1, 0.1, 1.0)  # Dark border color
        gl.glDrawArrays(gl.GL_TRIANGLES, ceiling_main_count, ceiling_border_count)
        
        # Reset state
        gl.glBindVertexArray(0)
        gl.glEnable(gl.GL_CULL_FACE)  # Re-enable culling after rendering
    
    def render_object(self, obj, view_matrix, projection_matrix):
        """
        Render an opaque object
        
        Args:
            obj: Object to render
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        # Create a key for the mesh cache based on object type and dimensions
        mesh_key = None
        color = [1.0, 1.0, 1.0, 1.0]  # Default color
        
        if isinstance(obj, Door):
            # Include thickness in the mesh key for proper distinction
            mesh_key = f"door_{obj.door_type}_{obj.width}_{obj.height}_{obj.thickness}"
            if mesh_key not in self.mesh_cache:
                self.mesh_cache[mesh_key] = self.mesh_factory.create_door_mesh(
                    obj.door_type, obj.width, obj.height, obj.thickness
                )
            color = obj.color + [1.0]  # Add alpha
            
        elif isinstance(obj, Furniture):
            mesh_key = f"furniture_{obj.furniture_type}_{obj.width}_{obj.depth}_{obj.height}"
            if mesh_key not in self.mesh_cache:
                self.mesh_cache[mesh_key] = self.mesh_factory.create_furniture_mesh(
                    obj.furniture_type, obj.width, obj.depth, obj.height
                )
            color = obj.color + [1.0]  # Add alpha
        
        if mesh_key is None or mesh_key not in self.mesh_cache:
            return  # Skip rendering if no mesh
        
        # Get mesh
        mesh = self.mesh_cache[mesh_key]
        
        # Bind the default shader
        gl.glUseProgram(self.default_shader)
        
        # Set uniforms
        gl.glUniformMatrix4fv(self.default_uniforms["view"], 1, gl.GL_FALSE, value_ptr(view_matrix))
        gl.glUniformMatrix4fv(self.default_uniforms["projection"], 1, gl.GL_FALSE, value_ptr(projection_matrix))
        gl.glUniformMatrix4fv(self.default_uniforms["model"], 1, gl.GL_FALSE, value_ptr(obj.get_model_matrix()))
        
        # Door specific rendering
        if isinstance(obj, Door):
            # Get door states
            is_open = obj.is_open
            open_angle = obj.open_angle
            
            # Add custom rotational transform for door opening
            if is_open and open_angle > 0:
                # Get door model matrix
                model_matrix = obj.get_model_matrix()
                
                # Adjust model matrix based on door type and opening angle
                if obj.door_type == "Single Door":
                    # Apply rotation around Y axis
                    rotation_matrix = glm.rotate(glm.mat4(1.0), glm.radians(open_angle), glm.vec3(0, 1, 0))
                    model_matrix = model_matrix * rotation_matrix
                    gl.glUniformMatrix4fv(self.default_uniforms["model"], 1, gl.GL_FALSE, value_ptr(model_matrix))
                    
                elif obj.door_type == "Double Door":
                    # For double doors, we'll need to handle each door separately
                    # Not implemented in this example
                    pass
                    
                elif obj.door_type == "Sliding Door":
                    # For sliding doors, apply a translation instead of rotation
                    # Not implemented in this example
                    pass
        
        # Set material properties
        gl.glUniform4f(self.default_uniforms["color"], color[0], color[1], color[2], color[3])
        gl.glUniform1i(self.default_uniforms["use_texture"], 0)  # No texture for now
        
        # Bind the VAO and render
        gl.glBindVertexArray(mesh["vao"])
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh["vertex_count"])
        
        # Unbind VAO
        gl.glBindVertexArray(0)
    
    def render_transparent_object(self, obj, view_matrix, projection_matrix):
        """
        Render a transparent object
        
        Args:
            obj: Object to render
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        # Create a key for the mesh cache based on object type and dimensions
        mesh_key = None
        color = [1.0, 1.0, 1.0, 0.5]  # Default color with transparency
        
        if isinstance(obj, Window):
            mesh_key = f"window_{obj.window_type}_{obj.width}_{obj.height}"
            if mesh_key not in self.mesh_cache:
                self.mesh_cache[mesh_key] = self.mesh_factory.create_window_mesh(
                    obj.window_type, obj.width, obj.height, obj.thickness, obj.segments
                )
            
            # First render the frame (opaque)
            # Bind the default shader
            gl.glUseProgram(self.default_shader)
            
            # Set uniforms
            gl.glUniformMatrix4fv(self.default_uniforms["view"], 1, gl.GL_FALSE, value_ptr(view_matrix))
            gl.glUniformMatrix4fv(self.default_uniforms["projection"], 1, gl.GL_FALSE, value_ptr(projection_matrix))
            gl.glUniformMatrix4fv(self.default_uniforms["model"], 1, gl.GL_FALSE, value_ptr(obj.get_model_matrix()))
            
            # Set frame material properties (opaque)
            frame_color = obj.frame_color
            gl.glUniform4f(self.default_uniforms["color"], frame_color[0], frame_color[1], frame_color[2], 1.0)
            gl.glUniform1i(self.default_uniforms["use_texture"], 0)  # No texture for now
            
            # Bind the frame VAO and render
            mesh = self.mesh_cache[mesh_key]
            gl.glBindVertexArray(mesh["frame_vao"])
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh["frame_vertex_count"])
            
            # Now render the glass (transparent)
            # Bind the transparent shader
            gl.glUseProgram(self.transparent_shader)
            
            # Set uniforms
            gl.glUniformMatrix4fv(self.transparent_uniforms["view"], 1, gl.GL_FALSE, value_ptr(view_matrix))
            gl.glUniformMatrix4fv(self.transparent_uniforms["projection"], 1, gl.GL_FALSE, value_ptr(projection_matrix))
            gl.glUniformMatrix4fv(self.transparent_uniforms["model"], 1, gl.GL_FALSE, value_ptr(obj.get_model_matrix()))
            
            # Enhanced glass rendering with better visual properties
            
            # Enable blending for transparent glass
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            
            # Calculate view-dependent effects for realistic glass
            view_pos = self.camera.position
            obj_pos = obj.position
            
            # Vector from camera to object
            view_vector = [obj_pos[0] - view_pos[0], 
                          obj_pos[1] - view_pos[1], 
                          obj_pos[2] - view_pos[2]]
            
            # Normalize the viewing vector
            length = (view_vector[0]**2 + view_vector[1]**2 + view_vector[2]**2)**0.5
            if length > 0:
                view_vector = [v/length for v in view_vector]
            
            # Calculate view angle factors - simulating Fresnel effect
            # (how glass reflects more at steep angles)
            
            # Dot product with up vector [0,1,0] - simplification for vertical windows
            up_dot = abs(view_vector[1])
            
            # Dot product with normal vector [0,0,1] - for window face orientation
            # Assuming window normal is approximately aligned with z-axis
            normal_dot = abs(view_vector[2])
            
            # Calculate Fresnel factor - more reflective at grazing angles
            fresnel_factor = pow(1.0 - normal_dot, 3)
            
            # Get glass properties from object
            glass_color = obj.glass_color
            glass_transparency = obj.glass_transparency
            
            # Apply view-dependent effects            
            # 1. Transparency decreases (more reflection) at grazing angles (Fresnel effect)
            adjusted_transparency = glass_transparency * (1.0 - fresnel_factor * 0.8)
            
            # 2. Color shifts slightly towards blue/white at steep angles
            adjusted_color = [
                glass_color[0] + 0.1 * fresnel_factor,  # More white/blue at grazing angles
                glass_color[1] + 0.15 * fresnel_factor,
                glass_color[2] + 0.2 * fresnel_factor,  # Blue increases most
            ]
            
            # Ensure colors stay in valid range
            adjusted_color = [min(1.0, c) for c in adjusted_color]
            
            # Set final color for glass with adjusted transparency
            gl.glUniform4f(self.transparent_uniforms["color"], 
                         adjusted_color[0], adjusted_color[1], adjusted_color[2], 
                         1.0 - adjusted_transparency)
            
            # Set additional glass properties (if shader supports them)
            if "fresnel_factor" in self.transparent_uniforms:
                gl.glUniform1f(self.transparent_uniforms["fresnel_factor"], fresnel_factor)
                
            if "reflectivity" in self.transparent_uniforms:
                gl.glUniform1f(self.transparent_uniforms["reflectivity"], 0.3 + fresnel_factor * 0.6)
            
            if "refraction_index" in self.transparent_uniforms:
                gl.glUniform1f(self.transparent_uniforms["refraction_index"], 1.52)  # Glass refraction index
            
            # Set default texture parameters (if needed later for environmental reflections)
            gl.glUniform1i(self.transparent_uniforms["use_texture"], 0)
            
            # Render main glass pane
            gl.glBindVertexArray(mesh["glass_vao"])
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh["glass_vertex_count"])
            
            # Optional: Add subtle edge highlight effect for better depth perception
            # This makes window edges slightly more visible
            if "highlight_color" in self.transparent_uniforms:
                # Slightly different color for edges
                edge_color = [
                    adjusted_color[0] + 0.1,
                    adjusted_color[1] + 0.1,
                    adjusted_color[2] + 0.15,
                    (1.0 - adjusted_transparency) + 0.2  # Slightly more visible
                ]
                
                # Draw thin highlight around glass edges
                # This would ideally be a separate mesh, but simplified here
                gl.glLineWidth(1.5)  # Thin line for edge highlight
                
                # If we have separate edge highlight rendering, it would go here
                # For now, we're using the same mesh but with a different rendering mode
                # ...
                
                gl.glLineWidth(1.0)  # Reset line width
            
            # Disable blending after rendering transparent objects
            gl.glDisable(gl.GL_BLEND)
        
        # Unbind VAO
        gl.glBindVertexArray(0)
    
    def render_selected_object(self, obj, view_matrix, projection_matrix):
        """
        Render outline for selected object with enhanced visual feedback
        
        Args:
            obj: Selected object to highlight
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        # Skip room selection highlight
        if isinstance(obj, Room):
            return
            
        # Create a key for the mesh cache based on object type and dimensions
        mesh_key = None
        
        if isinstance(obj, Door):
            mesh_key = f"door_{obj.door_type}_{obj.width}_{obj.height}_{obj.thickness}"
        elif isinstance(obj, Window):
            mesh_key = f"window_{obj.window_type}_{obj.width}_{obj.height}"
        elif isinstance(obj, Furniture):
            mesh_key = f"furniture_{obj.furniture_type}_{obj.width}_{obj.depth}_{obj.height}"
        
        if mesh_key is None or mesh_key not in self.mesh_cache:
            return  # Skip rendering if no mesh
        
        # Get mesh
        mesh = self.mesh_cache[mesh_key]
        
        # Setup for selection rendering
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glCullFace(gl.GL_BACK)
        
        # Bind the selection shader
        gl.glUseProgram(self.selection_shader)
        
        # Set uniforms
        gl.glUniformMatrix4fv(self.selection_uniforms["view"], 1, gl.GL_FALSE, value_ptr(view_matrix))
        gl.glUniformMatrix4fv(self.selection_uniforms["projection"], 1, gl.GL_FALSE, value_ptr(projection_matrix))
        gl.glUniformMatrix4fv(self.selection_uniforms["model"], 1, gl.GL_FALSE, value_ptr(obj.get_model_matrix()))
        
        # Choose highlight color based on object type
        if isinstance(obj, Door):
            # Doors - orange highlight
            gl.glUniform4f(self.selection_uniforms["highlight_color"], 1.0, 0.6, 0.0, 0.8)
        elif isinstance(obj, Window):
            # Windows - blue highlight
            gl.glUniform4f(self.selection_uniforms["highlight_color"], 0.1, 0.6, 1.0, 0.7)
        elif isinstance(obj, Furniture):
            # Furniture - green highlight
            gl.glUniform4f(self.selection_uniforms["highlight_color"], 0.2, 0.8, 0.4, 0.8)
        else:
            # Default - yellow highlight
            gl.glUniform4f(self.selection_uniforms["highlight_color"], 1.0, 0.9, 0.0, 0.7)
        
        # First pass - draw outlines for all components
        gl.glDepthMask(gl.GL_FALSE)  # Don't write to depth buffer for transparent pass
        
        # Special handling for windows
        if isinstance(obj, Window):
            # Bind the frame VAO and render
            gl.glBindVertexArray(mesh["frame_vao"])
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh["frame_vertex_count"])
            
            # Bind the glass VAO and render
            gl.glBindVertexArray(mesh["glass_vao"])
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh["glass_vertex_count"])
        else:
            # Regular binding and rendering
            gl.glBindVertexArray(mesh["vao"])
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, mesh["vertex_count"])
        
        # Reset depth mask
        gl.glDepthMask(gl.GL_TRUE)
        
        # Unbind VAO and reset state
        gl.glBindVertexArray(0)
        gl.glUseProgram(0)
    
    def cleanup(self):
        """Clean up OpenGL resources"""
        # Delete all VAOs and VBOs in the mesh cache
        for mesh_data in self.mesh_cache.values():
            if isinstance(mesh_data, dict):
                # Delete room VAOs and VBOs
                if "floor_vao" in mesh_data:
                    gl.glDeleteVertexArrays(1, [mesh_data["floor_vao"]])
                if "walls_vao" in mesh_data:
                    gl.glDeleteVertexArrays(1, [mesh_data["walls_vao"]])
                if "ceiling_vao" in mesh_data:
                    gl.glDeleteVertexArrays(1, [mesh_data["ceiling_vao"]])
                
                # Delete object VAOs
                if "vao" in mesh_data:
                    gl.glDeleteVertexArrays(1, [mesh_data["vao"]])
                
                # Delete window component VAOs
                if "frame_vao" in mesh_data:
                    gl.glDeleteVertexArrays(1, [mesh_data["frame_vao"]])
                if "glass_vao" in mesh_data:
                    gl.glDeleteVertexArrays(1, [mesh_data["glass_vao"]])
                
                # Delete VBOs
                for key in mesh_data:
                    if key.endswith("_vbo"):
                        gl.glDeleteBuffers(1, [mesh_data[key]])
        
        # Delete shader programs
        if hasattr(self, 'default_shader'):
            gl.glDeleteProgram(self.default_shader)
        if hasattr(self, 'transparent_shader'):
            gl.glDeleteProgram(self.transparent_shader)
        if hasattr(self, 'selection_shader'):
            gl.glDeleteProgram(self.selection_shader)
        
        # Clear the mesh cache
        self.mesh_cache.clear() 