from OpenGL import GL as gl
from OpenGL.GL import shaders

class ShaderManager:
    """
    Manager for OpenGL shader programs
    """
    def __init__(self):
        # Dictionary of shader programs
        self.shader_programs = {}
        
        # Dictionary of shader sources (vertex and fragment)
        self.shader_sources = {
            "default": {
                "vertex": self._get_default_vertex_shader(),
                "fragment": self._get_default_fragment_shader()
            },
            "transparent": {
                "vertex": self._get_default_vertex_shader(),
                "fragment": self._get_transparent_fragment_shader()
            },
            "selection": {
                "vertex": self._get_selection_vertex_shader(),
                "fragment": self._get_selection_fragment_shader()
            }
        }
    
    def create_shader_program(self, shader_name):
        """
        Create a shader program
        
        Args:
            shader_name: Name of the shader to create
            
        Returns:
            int: OpenGL shader program ID
        """
        if shader_name in self.shader_programs:
            return self.shader_programs[shader_name]
        
        if shader_name not in self.shader_sources:
            raise ValueError(f"Unknown shader name: {shader_name}")
        
        # Get shader sources
        vertex_source = self.shader_sources[shader_name]["vertex"]
        fragment_source = self.shader_sources[shader_name]["fragment"]
        
        # Compile shaders
        vertex_shader = shaders.compileShader(vertex_source, gl.GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fragment_source, gl.GL_FRAGMENT_SHADER)
        
        # Create program
        shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
        
        # Store in dictionary
        self.shader_programs[shader_name] = shader_program
        
        return shader_program
    
    def _get_default_vertex_shader(self):
        """Get the default vertex shader source"""
        return """
        #version 330 core
        
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec2 texCoord;
        
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        
        out vec3 fragPos;
        out vec3 fragNormal;
        out vec2 fragTexCoord;
        
        void main() {
            fragPos = vec3(model * vec4(position, 1.0));
            fragNormal = mat3(transpose(inverse(model))) * normal;
            fragTexCoord = texCoord;
            
            gl_Position = projection * view * model * vec4(position, 1.0);
        }
        """
    
    def _get_default_fragment_shader(self):
        """Get the default fragment shader source"""
        return """
        #version 330 core
        
        in vec3 fragPos;
        in vec3 fragNormal;
        in vec2 fragTexCoord;
        
        uniform vec4 color;
        uniform bool use_texture;
        uniform sampler2D texture_sampler;
        
        out vec4 fragColor;
        
        void main() {
            // Primary light direction (directional light from above)
            vec3 lightDir1 = normalize(vec3(0.5, 1.0, 0.3));
            
            // Secondary light direction (interior light from below)
            vec3 lightDir2 = normalize(vec3(-0.5, -0.8, -0.3));
            
            // Ambient component (increased for better interior visibility)
            float ambientStrength = 0.4;
            vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);
            
            // Diffuse component for primary light
            vec3 normal = normalize(fragNormal);
            float diff1 = max(dot(normal, lightDir1), 0.0);
            vec3 diffuse1 = diff1 * vec3(1.0, 1.0, 0.9); // Slightly warm light from above
            
            // Diffuse component for secondary light (interior)
            float diff2 = max(dot(normal, lightDir2), 0.0);
            vec3 diffuse2 = diff2 * vec3(0.8, 0.8, 1.0) * 0.6; // Slightly cool light from below, less intense
            
            // Add a rim light effect to highlight edges
            vec3 viewDir = normalize(vec3(0.0, 0.0, 1.0) - fragPos);
            float rim = 1.0 - max(dot(viewDir, normal), 0.0);
            rim = smoothstep(0.6, 1.0, rim) * 0.3;
            vec3 rimLight = rim * vec3(0.9, 0.9, 1.0);
            
            // Combine lighting (primary + secondary + rim)
            vec3 lighting = ambient + diffuse1 + diffuse2 + rimLight;
            
            // Ensure lighting doesn't wash out colors completely
            lighting = min(lighting, vec3(1.2));
            
            // Final color (with or without texture)
            if (use_texture) {
                fragColor = texture(texture_sampler, fragTexCoord) * vec4(lighting, 1.0);
            } else {
                fragColor = color * vec4(lighting, 1.0);
            }
        }
        """
    
    def _get_transparent_fragment_shader(self):
        """Get the transparent fragment shader source"""
        return """
        #version 330 core
        
        in vec3 fragPos;
        in vec3 fragNormal;
        in vec2 fragTexCoord;
        
        uniform vec4 color;
        uniform bool use_texture;
        uniform sampler2D texture_sampler;
        
        out vec4 fragColor;
        
        void main() {
            // Light direction (directional light from above)
            vec3 lightDir = normalize(vec3(0.5, 1.0, 0.3));
            
            // Ambient component
            float ambientStrength = 0.3;
            vec3 ambient = ambientStrength * vec3(1.0, 1.0, 1.0);
            
            // Diffuse component
            vec3 normal = normalize(fragNormal);
            float diff = max(dot(normal, lightDir), 0.0);
            vec3 diffuse = diff * vec3(1.0, 1.0, 1.0);
            
            // Combine lighting
            vec3 lighting = ambient + diffuse;
            
            // Final color (with or without texture)
            if (use_texture) {
                fragColor = texture(texture_sampler, fragTexCoord) * vec4(lighting, 1.0);
                // Keep original alpha
                fragColor.a = texture(texture_sampler, fragTexCoord).a;
            } else {
                fragColor = color * vec4(lighting, 1.0);
                // Keep original alpha
                fragColor.a = color.a;
            }
        }
        """
    
    def _get_selection_vertex_shader(self):
        """Get the selection vertex shader source"""
        return """
        #version 330 core
        
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec2 texCoord;
        
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        
        out vec3 fragNormal;
        out vec3 fragPos;
        
        void main() {
            // Create a more visible outline effect with appropriate scaling
            // Use a dynamic scale factor that looks good from any distance
            vec3 scaledPos = position + normal * 0.015;
            
            // Pass data to fragment shader
            fragPos = vec3(model * vec4(position, 1.0));
            fragNormal = mat3(transpose(inverse(model))) * normal;
            
            gl_Position = projection * view * model * vec4(scaledPos, 1.0);
        }
        """
    
    def _get_selection_fragment_shader(self):
        """Get the selection fragment shader source"""
        return """
        #version 330 core
        
        in vec3 fragNormal;
        in vec3 fragPos;
        
        uniform vec4 highlight_color;
        
        out vec4 fragColor;
        
        void main() {
            // Create a more dynamic highlight effect
            // Light direction (same as in main shader)
            vec3 lightDir = normalize(vec3(0.5, 1.0, 0.3));
            
            // Normalize the normal
            vec3 normal = normalize(fragNormal);
            
            // Edge detection - highlight edges more
            float edge = 1.0 - max(dot(normal, normalize(vec3(0.0, 0.0, 1.0))), 0.0);
            edge = pow(edge, 3.0) * 0.5;
            
            // Lighting contribution
            float diffuse = max(dot(normal, lightDir), 0.0);
            
            // Apply lighting to highlight color
            vec3 finalColor = highlight_color.rgb * (0.7 + diffuse * 0.3);
            
            // Add edge highlighting
            finalColor += edge * vec3(1.0, 1.0, 1.0);
            
            // Ensure the highlight is visible through transparent objects
            fragColor = vec4(finalColor, highlight_color.a);
        }
        """
    
    def cleanup(self):
        """Clean up shader programs"""
        for program_id in self.shader_programs.values():
            gl.glDeleteProgram(program_id)
        
        self.shader_programs.clear() 