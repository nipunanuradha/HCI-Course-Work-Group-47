import tkinter as tk
from tkinter import ttk

class Sidebar(ttk.Frame):
    def __init__(self, parent, main_window):
        """
        Initialize the sidebar panel
        
        Args:
            parent: Parent tkinter widget
            main_window: MainWindow instance
        """
        ttk.Frame.__init__(self, parent, relief=tk.RAISED, borderwidth=1)
        
        self.parent = parent
        self.main_window = main_window
        self.scene_manager = main_window.scene_manager
        
        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs for different categories
        self.rooms_tab = ttk.Frame(self.notebook)
        self.doors_tab = ttk.Frame(self.notebook)
        self.windows_tab = ttk.Frame(self.notebook)
        self.furniture_tab = ttk.Frame(self.notebook)
        self.properties_tab = ttk.Frame(self.notebook)
        self.materials_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.rooms_tab, text="Rooms")
        self.notebook.add(self.doors_tab, text="Doors")
        self.notebook.add(self.windows_tab, text="Windows")
        self.notebook.add(self.furniture_tab, text="Furniture")
        self.notebook.add(self.properties_tab, text="Properties")
        self.notebook.add(self.materials_tab, text="Materials")
        
        # Populate tabs
        self.create_rooms_panel()
        self.create_doors_panel()
        self.create_windows_panel()
        self.create_furniture_panel()
        self.create_properties_panel()
        self.create_materials_panel()
    
    def create_rooms_panel(self):
        """Create room selection panel"""
        # Room type label
        ttk.Label(self.rooms_tab, text="Room Type:").pack(anchor=tk.W, padx=5, pady=5)
        
        # Room type selection
        room_types = ["Dining Room", "Living Room", "Master Bedroom", "Office Room"]
        self.room_type_var = tk.StringVar(value=room_types[0])
        
        for room_type in room_types:
            ttk.Radiobutton(self.rooms_tab, text=room_type, value=room_type, 
                          variable=self.room_type_var,
                          command=self.on_room_type_changed).pack(anchor=tk.W, padx=20, pady=2)
        
        # Room dimensions
        dim_frame = ttk.LabelFrame(self.rooms_tab, text="Room Dimensions")
        dim_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Width
        width_frame = ttk.Frame(dim_frame)
        width_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(width_frame, text="Width (m):").pack(side=tk.LEFT)
        self.width_var = tk.DoubleVar(value=5.0)
        width_spinbox = ttk.Spinbox(width_frame, from_=2.0, to=15.0, increment=0.1, 
                                  textvariable=self.width_var,
                                  command=lambda: self.on_dimension_changed("width"))
        width_spinbox.pack(side=tk.RIGHT)
        
        # Length
        length_frame = ttk.Frame(dim_frame)
        length_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(length_frame, text="Length (m):").pack(side=tk.LEFT)
        self.length_var = tk.DoubleVar(value=6.0)
        length_spinbox = ttk.Spinbox(length_frame, from_=2.0, to=15.0, increment=0.1, 
                                   textvariable=self.length_var,
                                   command=lambda: self.on_dimension_changed("length"))
        length_spinbox.pack(side=tk.RIGHT)
        
        # Height
        height_frame = ttk.Frame(dim_frame)
        height_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(height_frame, text="Height (m):").pack(side=tk.LEFT)
        self.height_var = tk.DoubleVar(value=2.5)
        height_spinbox = ttk.Spinbox(height_frame, from_=2.0, to=5.0, increment=0.1, 
                                   textvariable=self.height_var,
                                   command=lambda: self.on_dimension_changed("height"))
        height_spinbox.pack(side=tk.RIGHT)
        
        # Apply button
        ttk.Button(self.rooms_tab, text="Apply Room Settings", 
                 command=self.apply_room_settings).pack(pady=10)
    
    def create_doors_panel(self):
        """Create door selection panel"""
        # Door type label
        ttk.Label(self.doors_tab, text="Door Type:").pack(anchor=tk.W, padx=5, pady=5)
        
        # Door type selection
        door_types = ["Single Door", "Double Door", "Sliding Door"]
        self.door_type_var = tk.StringVar(value=door_types[0])
        
        for door_type in door_types:
            ttk.Radiobutton(self.doors_tab, text=door_type, value=door_type, 
                          variable=self.door_type_var).pack(anchor=tk.W, padx=20, pady=2)
        
        # Door dimensions
        dim_frame = ttk.LabelFrame(self.doors_tab, text="Door Dimensions")
        dim_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Width
        width_frame = ttk.Frame(dim_frame)
        width_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(width_frame, text="Width (m):").pack(side=tk.LEFT)
        self.door_width_var = tk.DoubleVar(value=0.9)
        door_width_spinbox = ttk.Spinbox(width_frame, from_=0.6, to=2.0, increment=0.1, 
                                       textvariable=self.door_width_var)
        door_width_spinbox.pack(side=tk.RIGHT)
        
        # Height
        height_frame = ttk.Frame(dim_frame)
        height_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(height_frame, text="Height (m):").pack(side=tk.LEFT)
        self.door_height_var = tk.DoubleVar(value=2.0)
        door_height_spinbox = ttk.Spinbox(height_frame, from_=1.8, to=2.4, increment=0.1, 
                                        textvariable=self.door_height_var)
        door_height_spinbox.pack(side=tk.RIGHT)
        
        # Thickness/Length
        thickness_frame = ttk.Frame(dim_frame)
        thickness_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(thickness_frame, text="Thickness (m):").pack(side=tk.LEFT)
        self.door_thickness_var = tk.DoubleVar(value=0.05)
        door_thickness_spinbox = ttk.Spinbox(thickness_frame, from_=0.01, to=0.2, increment=0.01, 
                                           textvariable=self.door_thickness_var)
        door_thickness_spinbox.pack(side=tk.RIGHT)
        
        # Create a frame for buttons
        button_frame = ttk.Frame(self.doors_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Add button
        ttk.Button(button_frame, text="Add Door", 
                 command=self.add_door).pack(side=tk.LEFT, padx=5)
                 
        # Remove button
        ttk.Button(button_frame, text="Remove Door", 
                 command=self.remove_selected_door).pack(side=tk.RIGHT, padx=5)
    
    def create_windows_panel(self):
        """Create window selection panel"""
        # Window type label
        ttk.Label(self.windows_tab, text="Window Type:").pack(anchor=tk.W, padx=5, pady=5)
        
        # Window type selection
        window_types = ["Single Window", "Double Window", "Bay Window"]
        self.window_type_var = tk.StringVar(value=window_types[0])
        
        for window_type in window_types:
            ttk.Radiobutton(self.windows_tab, text=window_type, value=window_type, 
                          variable=self.window_type_var).pack(anchor=tk.W, padx=20, pady=2)
        
        # Window dimensions
        dim_frame = ttk.LabelFrame(self.windows_tab, text="Window Dimensions")
        dim_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Width
        width_frame = ttk.Frame(dim_frame)
        width_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(width_frame, text="Width (m):").pack(side=tk.LEFT)
        self.window_width_var = tk.DoubleVar(value=1.2)
        window_width_spinbox = ttk.Spinbox(width_frame, from_=0.5, to=2.5, increment=0.1, 
                                         textvariable=self.window_width_var)
        window_width_spinbox.pack(side=tk.RIGHT)
        
        # Height
        height_frame = ttk.Frame(dim_frame)
        height_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(height_frame, text="Height (m):").pack(side=tk.LEFT)
        self.window_height_var = tk.DoubleVar(value=1.0)
        window_height_spinbox = ttk.Spinbox(height_frame, from_=0.5, to=2.0, increment=0.1, 
                                          textvariable=self.window_height_var)
        window_height_spinbox.pack(side=tk.RIGHT)
        
        # Create a frame for buttons
        button_frame = ttk.Frame(self.windows_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Add button
        ttk.Button(button_frame, text="Add Window", 
                 command=self.add_window).pack(side=tk.LEFT, padx=5)
                 
        # Remove button
        ttk.Button(button_frame, text="Remove Window", 
                 command=self.remove_selected_window).pack(side=tk.RIGHT, padx=5)
    
    def create_furniture_panel(self):
        """Create furniture selection panel"""
        # Furniture category label
        ttk.Label(self.furniture_tab, text="Furniture Category:").pack(anchor=tk.W, padx=5, pady=5)
        
        # Furniture category selection
        categories = ["Chairs", "Tables", "Sofas", "Beds", "Cupboards"]
        self.furniture_category_var = tk.StringVar(value=categories[0])
        category_combobox = ttk.Combobox(self.furniture_tab, textvariable=self.furniture_category_var, 
                                       values=categories, state="readonly")
        category_combobox.pack(fill=tk.X, padx=5, pady=5)
        category_combobox.bind("<<ComboboxSelected>>", self.on_furniture_category_changed)
        
        # Furniture items frame
        self.furniture_items_frame = ttk.LabelFrame(self.furniture_tab, text="Furniture Items")
        self.furniture_items_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Populate with initial category
        self.populate_furniture_items(categories[0])
        
        # Create a frame for buttons
        button_frame = ttk.Frame(self.furniture_tab)
        button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Add button
        ttk.Button(button_frame, text="Add Selected Furniture", 
                 command=self.add_furniture).pack(side=tk.LEFT, padx=5)
                 
        # Remove button
        ttk.Button(button_frame, text="Remove Furniture", 
                 command=self.remove_selected_furniture).pack(side=tk.RIGHT, padx=5)
    
    def create_properties_panel(self):
        """Create properties panel for selected objects"""
        ttk.Label(self.properties_tab, text="Selected Object Properties").pack(anchor=tk.W, padx=5, pady=5)
        
        # No selection message
        self.no_selection_label = ttk.Label(self.properties_tab, text="No object selected")
        self.no_selection_label.pack(pady=20)
        
        # Properties frame (hidden initially)
        self.properties_frame = ttk.Frame(self.properties_tab)
        
        # Position controls
        pos_frame = ttk.LabelFrame(self.properties_frame, text="Position")
        pos_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # X position
        x_frame = ttk.Frame(pos_frame)
        x_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(x_frame, text="X:").pack(side=tk.LEFT)
        self.pos_x_var = tk.DoubleVar(value=0.0)
        x_spinbox = ttk.Spinbox(x_frame, from_=-10.0, to=10.0, increment=0.1, 
                              textvariable=self.pos_x_var,
                              command=lambda: self.on_property_changed("position", "x"))
        x_spinbox.pack(side=tk.RIGHT)
        
        # Y position
        y_frame = ttk.Frame(pos_frame)
        y_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(y_frame, text="Y:").pack(side=tk.LEFT)
        self.pos_y_var = tk.DoubleVar(value=0.0)
        y_spinbox = ttk.Spinbox(y_frame, from_=-10.0, to=10.0, increment=0.1, 
                              textvariable=self.pos_y_var,
                              command=lambda: self.on_property_changed("position", "y"))
        y_spinbox.pack(side=tk.RIGHT)
        
        # Z position
        z_frame = ttk.Frame(pos_frame)
        z_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(z_frame, text="Z:").pack(side=tk.LEFT)
        self.pos_z_var = tk.DoubleVar(value=0.0)
        z_spinbox = ttk.Spinbox(z_frame, from_=-10.0, to=10.0, increment=0.1, 
                              textvariable=self.pos_z_var,
                              command=lambda: self.on_property_changed("position", "z"))
        z_spinbox.pack(side=tk.RIGHT)
        
        # Rotation controls
        rot_frame = ttk.LabelFrame(self.properties_frame, text="Rotation (degrees)")
        rot_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # X rotation
        rot_x_frame = ttk.Frame(rot_frame)
        rot_x_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(rot_x_frame, text="X:").pack(side=tk.LEFT)
        self.rot_x_var = tk.DoubleVar(value=0.0)
        rot_x_spinbox = ttk.Spinbox(rot_x_frame, from_=0, to=359, increment=15, 
                                  textvariable=self.rot_x_var,
                                  command=lambda: self.on_property_changed("rotation", "x"))
        rot_x_spinbox.pack(side=tk.RIGHT)
        
        # Y rotation
        rot_y_frame = ttk.Frame(rot_frame)
        rot_y_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(rot_y_frame, text="Y:").pack(side=tk.LEFT)
        self.rot_y_var = tk.DoubleVar(value=0.0)
        rot_y_spinbox = ttk.Spinbox(rot_y_frame, from_=0, to=359, increment=15, 
                                  textvariable=self.rot_y_var,
                                  command=lambda: self.on_property_changed("rotation", "y"))
        rot_y_spinbox.pack(side=tk.RIGHT)
        
        # Z rotation
        rot_z_frame = ttk.Frame(rot_frame)
        rot_z_frame.pack(fill=tk.X, padx=5, pady=3)
        ttk.Label(rot_z_frame, text="Z:").pack(side=tk.LEFT)
        self.rot_z_var = tk.DoubleVar(value=0.0)
        rot_z_spinbox = ttk.Spinbox(rot_z_frame, from_=0, to=359, increment=15, 
                                  textvariable=self.rot_z_var,
                                  command=lambda: self.on_property_changed("rotation", "z"))
        rot_z_spinbox.pack(side=tk.RIGHT)
        
        # Delete button
        ttk.Button(self.properties_frame, text="Delete Selected Object", 
                 command=self.delete_selected_object,
                 style="Accent.TButton").pack(pady=10)
    
    def create_materials_panel(self):
        """Create materials and color selection panel with scrollable view"""
        # Create a canvas and a vertical scrollbar for the materials tab
        canvas = tk.Canvas(self.materials_tab, borderwidth=0, highlightthickness=0)
        vscroll = ttk.Scrollbar(self.materials_tab, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a frame inside the canvas to hold the actual content
        self.materials_inner_frame = ttk.Frame(canvas)
        self.materials_inner_frame_id = canvas.create_window((0, 0), window=self.materials_inner_frame, anchor="nw")

        # Make sure the canvas scrolls with the mousewheel and resizes properly
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.materials_inner_frame.bind("<Configure>", _on_frame_configure)
        def _on_canvas_configure(event):
            canvas.itemconfig(self.materials_inner_frame_id, width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.materials_inner_frame.bind_all("<MouseWheel>", _on_mousewheel)

        # Main label
        ttk.Label(self.materials_inner_frame, text="Color Selection").pack(anchor=tk.W, padx=5, pady=5)
        # Object type selection
        object_frame = ttk.LabelFrame(self.materials_inner_frame, text="Object Type")
        object_frame.pack(fill=tk.X, padx=5, pady=5)
        object_types = ["Room", "Door", "Window", "Furniture", "Selected Object"]
        self.object_type_var = tk.StringVar(value=object_types[0])
        for obj_type in object_types:
            ttk.Radiobutton(object_frame, text=obj_type, value=obj_type, 
                          variable=self.object_type_var, 
                          command=self.update_material_options).pack(anchor=tk.W, padx=10, pady=2)
        
        # Create a frame for view selection (interior/exterior)
        self.view_type_frame = ttk.LabelFrame(self.materials_inner_frame, text="View Type")
        view_types = ["Exterior", "Interior"]
        self.view_type_var = tk.StringVar(value=view_types[0])
        for view_type in view_types:
            ttk.Radiobutton(self.view_type_frame, text=view_type, value=view_type,
                          variable=self.view_type_var,
                          command=self.update_material_options).pack(anchor=tk.W, padx=10, pady=2)
        
        # Room components (for when Room is selected)
        self.room_component_frame = ttk.LabelFrame(self.materials_inner_frame, text="Room Component")
        self.exterior_component_var = tk.StringVar(value="walls")
        self.interior_component_var = tk.StringVar(value="walls")
        
        # We'll populate this frame based on view type in update_material_options
        
        # Color options
        color_frame = ttk.LabelFrame(self.materials_inner_frame, text="Color Options")
        color_frame.pack(fill=tk.X, padx=5, pady=5)
        predefined_colors = [
            ("White", "#FFFFFF"), 
            ("Light Gray", "#D3D3D3"),
            ("Dark Gray", "#A9A9A9"),
            ("Black", "#000000"),
            ("Red", "#FF0000"),
            ("Green", "#00FF00"),
            ("Blue", "#0000FF"),
            ("Yellow", "#FFFF00"),
            ("Orange", "#FFA500"),
            ("Purple", "#800080"),
            ("Teal", "#008080"),
            ("Brown", "#A52A2A"),
            ("Beige", "#F5F5DC"),
            ("Navy", "#000080")
        ]
        swatch_frame = ttk.Frame(color_frame)
        swatch_frame.pack(fill=tk.X, padx=5, pady=5)
        row, col = 0, 0
        for color_name, color_hex in predefined_colors:
            color_swatch = tk.Frame(swatch_frame, width=40, height=20, bg=color_hex, 
                                    relief=tk.RAISED, borderwidth=1)
            color_swatch.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            color_swatch.bind("<Button-1>", lambda e, c=color_hex, n=color_name: self.select_color(c, n))
            ttk.Label(swatch_frame, text=color_name, font=("Arial", 7)).grid(row=row+1, column=col, padx=2, pady=0)
            col += 1
            if col > 2:
                col = 0
                row += 2
        custom_frame = ttk.Frame(color_frame)
        custom_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(custom_frame, text="Custom Color...", 
                 command=self.choose_custom_color).pack(side=tk.LEFT, padx=5)
        self.current_color_display = tk.Frame(custom_frame, width=30, height=20, 
                                            bg="#FFFFFF", relief=tk.SUNKEN, borderwidth=2)
        self.current_color_display.pack(side=tk.RIGHT, padx=5)
        transparency_frame = ttk.LabelFrame(self.materials_inner_frame, text="Transparency")
        transparency_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(transparency_frame, text="Opacity: ").pack(side=tk.LEFT, padx=5)
        self.opacity_var = tk.IntVar(value=100)
        opacity_scale = ttk.Scale(transparency_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                variable=self.opacity_var, length=150)
        opacity_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        opacity_label = ttk.Label(transparency_frame, text="100%")
        opacity_label.pack(side=tk.RIGHT, padx=5)
        def update_opacity_label(*args):
            opacity_label.config(text=f"{self.opacity_var.get()}%")
        self.opacity_var.trace_add("write", update_opacity_label)
        ttk.Button(self.materials_inner_frame, text="Apply Color Settings", 
                 command=self.apply_color_settings).pack(pady=10)
        
        # --- Interior Surfaces Section ---
        interior_frame = ttk.LabelFrame(self.materials_inner_frame, text="Interior Surfaces")
        interior_frame.pack(fill=tk.X, padx=5, pady=10)
        self.interior_surface_vars = {}
        self.interior_opacity_vars = {}
        surfaces = [
            ("North Wall", "interior_north_wall_color", "wall_opacity"),
            ("South Wall", "interior_south_wall_color", "wall_opacity"),
            ("East Wall", "interior_east_wall_color", "wall_opacity"),
            ("West Wall", "interior_west_wall_color", "wall_opacity"),
            ("Ceiling", "interior_ceiling_color", "ceiling_opacity"),
            ("Floor", "interior_floor_color", "floor_opacity"),
        ]
        for label, color_attr, opacity_attr in surfaces:
            row_frame = ttk.Frame(interior_frame)
            row_frame.pack(fill=tk.X, padx=2, pady=2)
            ttk.Label(row_frame, text=label+":").pack(side=tk.LEFT, padx=2)
            color_var = tk.StringVar()
            self.interior_surface_vars[color_attr] = color_var
            color_btn = tk.Button(row_frame, width=3, bg="#FFFFFF", relief=tk.RAISED, command=lambda ca=color_attr: self.choose_surface_color(ca))
            color_btn.pack(side=tk.LEFT, padx=2)
            def safe_update_btn_bg(var=color_var, btn=color_btn):
                color = var.get()
                if color and color.startswith('#') and (len(color) == 7 or len(color) == 4):
                    try:
                        btn.config(bg=color)
                    except Exception:
                        pass
            color_var.trace_add("write", lambda *args, var=color_var, btn=color_btn: safe_update_btn_bg(var, btn))
            # Opacity slider
            opacity_var = tk.DoubleVar(value=100)
            self.interior_opacity_vars[opacity_attr] = opacity_var
            ttk.Label(row_frame, text="Opacity:").pack(side=tk.LEFT, padx=2)
            opacity_scale = ttk.Scale(row_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=opacity_var, length=80)
            opacity_scale.pack(side=tk.LEFT, padx=2)
            opacity_label = ttk.Label(row_frame, text="100%")
            opacity_label.pack(side=tk.LEFT, padx=2)
            def update_opacity_label(var=opacity_var, label=opacity_label):
                label.config(text=f"{int(var.get())}%")
            opacity_var.trace_add("write", lambda *args, v=opacity_var, l=opacity_label: update_opacity_label(v, l))
        # Button to apply all interior surface settings
        ttk.Button(interior_frame, text="Apply Interior Surface Settings", command=self.apply_interior_surface_settings).pack(pady=5)
        
        # --- Exterior Surfaces Section ---
        exterior_frame = ttk.LabelFrame(self.materials_inner_frame, text="Exterior Surfaces")
        exterior_frame.pack(fill=tk.X, padx=5, pady=10)
        self.exterior_surface_vars = {}
        self.exterior_opacity_vars = {}
        surfaces = [
            ("North Wall", "north_wall_color", "wall_opacity"),
            ("South Wall", "south_wall_color", "wall_opacity"),
            ("East Wall", "east_wall_color", "wall_opacity"),
            ("West Wall", "west_wall_color", "wall_opacity"),
            ("Ceiling", "ceiling_color", "ceiling_opacity"),
            ("Floor", "floor_color", "floor_opacity"),
        ]
        for label, color_attr, opacity_attr in surfaces:
            row_frame = ttk.Frame(exterior_frame)
            row_frame.pack(fill=tk.X, padx=2, pady=2)
            ttk.Label(row_frame, text=label+":").pack(side=tk.LEFT, padx=2)
            color_var = tk.StringVar()
            self.exterior_surface_vars[color_attr] = color_var
            color_btn = tk.Button(row_frame, width=3, bg="#FFFFFF", relief=tk.RAISED, command=lambda ca=color_attr: self.choose_exterior_surface_color(ca))
            color_btn.pack(side=tk.LEFT, padx=2)
            def safe_update_btn_bg(var=color_var, btn=color_btn):
                color = var.get()
                if color and color.startswith('#') and (len(color) == 7 or len(color) == 4):
                    try:
                        btn.config(bg=color)
                    except Exception:
                        pass
            color_var.trace_add("write", lambda *args, var=color_var, btn=color_btn: safe_update_btn_bg(var, btn))
            # Opacity slider
            opacity_var = tk.DoubleVar(value=100)
            self.exterior_opacity_vars[opacity_attr] = opacity_var
            ttk.Label(row_frame, text="Opacity:").pack(side=tk.LEFT, padx=2)
            opacity_scale = ttk.Scale(row_frame, from_=0, to=100, orient=tk.HORIZONTAL, variable=opacity_var, length=80)
            opacity_scale.pack(side=tk.LEFT, padx=2)
            opacity_label = ttk.Label(row_frame, text="100%")
            opacity_label.pack(side=tk.LEFT, padx=2)
            def update_opacity_label(var=opacity_var, label=opacity_label):
                label.config(text=f"{int(var.get())}%")
            opacity_var.trace_add("write", lambda *args, v=opacity_var, l=opacity_label: update_opacity_label(v, l))
        # Button to apply all exterior surface settings
        ttk.Button(exterior_frame, text="Apply Exterior Surface Settings", command=self.apply_exterior_surface_settings).pack(pady=5)
        
        self.update_material_options()
        self.current_color = "#FFFFFF"
        self.current_color_name = "White"
    
    def update_material_options(self):
        """Update material options based on selected object type and view type"""
        object_type = self.object_type_var.get()
        
        # Only show view type selection for Room objects
        if object_type == "Room":
            self.view_type_frame.pack(fill=tk.X, padx=5, pady=5, after=self.materials_inner_frame.winfo_children()[1])
            
            # Update room component options based on view type (interior/exterior)
            view_type = self.view_type_var.get()
            
            # Clear existing components
            for widget in self.room_component_frame.winfo_children():
                widget.destroy()
                
            # Create appropriate components based on view type
            if view_type == "Exterior":
                # Exterior room components
                room_components = [
                    ("All Walls", "walls"),
                    ("North Wall", "north_wall"),
                    ("South Wall", "south_wall"),
                    ("East Wall", "east_wall"),
                    ("West Wall", "west_wall"),
                    ("Floor", "floor"),
                    ("Ceiling", "ceiling"),
                    ("All", "all")
                ]
                for label, value in room_components:
                    ttk.Radiobutton(self.room_component_frame, text=label, value=value,
                                  variable=self.exterior_component_var,
                                  command=self.update_current_color).pack(anchor=tk.W, padx=10, pady=2)
                
                # Use exterior component variable
                self.room_component_var = self.exterior_component_var
                
            else:  # Interior view
                # Interior room components
                room_components = [
                    ("All Interior Walls", "interior_walls"),
                    ("North Interior Wall", "interior_north_wall"),
                    ("South Interior Wall", "interior_south_wall"),
                    ("East Interior Wall", "interior_east_wall"),
                    ("West Interior Wall", "interior_west_wall"),
                    ("Interior Floor", "interior_floor"),
                    ("Interior Ceiling", "interior_ceiling"),
                    ("All Interior", "interior_all")
                ]
                for label, value in room_components:
                    ttk.Radiobutton(self.room_component_frame, text=label, value=value,
                                  variable=self.interior_component_var,
                                  command=self.update_current_color).pack(anchor=tk.W, padx=10, pady=2)
                
                # Use interior component variable
                self.room_component_var = self.interior_component_var
            
            # Show room component frame
            self.room_component_frame.pack(fill=tk.X, padx=5, pady=5, after=self.view_type_frame)
        else:
            # Hide room component and view type frames for non-room objects
            self.room_component_frame.pack_forget()
            self.view_type_frame.pack_forget()
        
        # Update current color based on selection
        self.update_current_color()
    
    def update_current_color(self):
        """Update current color display based on selection"""
        object_type = self.object_type_var.get()
        if object_type == "Selected Object" and self.scene_manager.selected_object:
            obj = self.scene_manager.selected_object
            if hasattr(obj, 'color'):
                self.current_color = obj.color
            else:
                self.current_color = "#FFFFFF"
        elif object_type == "Room":
            view_type = self.view_type_var.get()
            component = self.room_component_var.get()
            
            if self.scene_manager.room:
                room = self.scene_manager.room
                
                # Handle interior and exterior components differently
                if view_type == "Interior":
                    if component == "interior_walls" and hasattr(room, 'interior_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.interior_wall_color)
                    elif component == "interior_north_wall" and hasattr(room, 'interior_north_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.interior_north_wall_color)
                    elif component == "interior_south_wall" and hasattr(room, 'interior_south_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.interior_south_wall_color)
                    elif component == "interior_east_wall" and hasattr(room, 'interior_east_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.interior_east_wall_color)
                    elif component == "interior_west_wall" and hasattr(room, 'interior_west_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.interior_west_wall_color)
                    elif component == "interior_floor" and hasattr(room, 'interior_floor_color'):
                        self.current_color = self._convert_color_to_hex(room.interior_floor_color)
                    elif component == "interior_ceiling" and hasattr(room, 'interior_ceiling_color'):
                        self.current_color = self._convert_color_to_hex(room.interior_ceiling_color)
                    else:
                        self.current_color = "#FFFFFF"
                else:  # Exterior
                    if component == "walls" and hasattr(room, 'wall_color'):
                        self.current_color = self._convert_color_to_hex(room.wall_color)
                    elif component == "north_wall" and hasattr(room, 'north_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.north_wall_color)
                    elif component == "south_wall" and hasattr(room, 'south_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.south_wall_color)
                    elif component == "east_wall" and hasattr(room, 'east_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.east_wall_color)
                    elif component == "west_wall" and hasattr(room, 'west_wall_color'):
                        self.current_color = self._convert_color_to_hex(room.west_wall_color)
                    elif component == "floor" and hasattr(room, 'floor_color'):
                        self.current_color = self._convert_color_to_hex(room.floor_color)
                    elif component == "ceiling" and hasattr(room, 'ceiling_color'):
                        self.current_color = self._convert_color_to_hex(room.ceiling_color)
                    else:
                        self.current_color = "#FFFFFF"
        else:
            self.current_color = "#FFFFFF"
            
        if not isinstance(self.current_color, str):
            self.current_color = self._convert_color_to_hex(self.current_color)
        self.current_color_display.config(bg=self.current_color)
    
    def _convert_color_to_hex(self, color):
        """Convert RGB color array to hex format
        
        Args:
            color: RGB color as list/array [r, g, b] with values 0-1
            
        Returns:
            Hex color string (#RRGGBB)
        """
        # Check if already a hex string
        if isinstance(color, str) and color.startswith('#'):
            return color
        
        # Convert from RGB array (0-1 values) to hex string
        try:
            r, g, b = color
            return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        except:
            # Return white as default if conversion fails
            return "#FFFFFF"
    
    def select_color(self, color_hex, color_name):
        """Select a color from the palette"""
        self.current_color = color_hex
        self.current_color_name = color_name
        self.current_color_display.config(bg=color_hex)
        
        # Update status bar with color information
        if hasattr(self.main_window, 'update_status'):
            self.main_window.update_status(f"Selected color: {color_name} ({color_hex})")
    
    def choose_custom_color(self):
        """Open a color chooser dialog for custom colors"""
        from tkinter import colorchooser
        
        # Open color chooser dialog
        color = colorchooser.askcolor(initialcolor=self.current_color, 
                                     title="Choose Custom Color")
        
        # Update if color was selected (not cancelled)
        if color[1]:
            self.current_color = color[1]
            self.current_color_name = "Custom"
            self.current_color_display.config(bg=color[1])
            
            # Update status
            if hasattr(self.main_window, 'update_status'):
                self.main_window.update_status(f"Selected custom color: {color[1]}")
    
    def apply_color_settings(self):
        """Apply color settings to the selected object or type"""
        object_type = self.object_type_var.get()
        opacity = self.opacity_var.get() / 100.0
        if object_type == "Selected Object":
            if self.scene_manager.selected_object:
                self.scene_manager.set_object_color(
                    self.scene_manager.selected_object,
                    self.current_color,
                    opacity
                )
                if hasattr(self.main_window, 'update_status'):
                    obj_name = getattr(self.scene_manager.selected_object, 'name', 'object')
                    self.main_window.update_status(
                        f"Applied {self.current_color_name} color to {obj_name}"
                    )
            else:
                if hasattr(self.main_window, 'update_status'):
                    self.main_window.update_status("No object selected to apply color")
        elif object_type == "Room":
            view_type = self.view_type_var.get()
            component = self.room_component_var.get()
            
            if self.scene_manager.room:
                # Apply settings based on view type
                if view_type == "Interior":
                    if component == "interior_all":
                        # Apply to all interior surfaces
                        self.scene_manager.set_room_interior_color(
                            self.current_color, opacity, "interior_walls"
                        )
                        self.scene_manager.set_room_interior_color(
                            self.current_color, opacity, "interior_floor"
                        )
                        self.scene_manager.set_room_interior_color(
                            self.current_color, opacity, "interior_ceiling"
                        )
                    else:
                        # Apply to specific interior component
                        self.scene_manager.set_room_interior_color(
                            self.current_color, opacity, component
                        )
                else:  # Exterior
                    if component == "all":
                        # Apply to all exterior surfaces
                        self.scene_manager.set_room_color(
                            self.current_color, opacity, "walls"
                        )
                        self.scene_manager.set_room_color(
                            self.current_color, opacity, "floor"
                        )
                        self.scene_manager.set_room_color(
                            self.current_color, opacity, "ceiling"
                        )
                    else:
                        # Map component value to actual properties used in set_room_color
                        component_map = {
                            "north_wall": "north_wall",
                            "south_wall": "south_wall",
                            "east_wall": "east_wall",
                            "west_wall": "west_wall",
                            "walls": "walls",
                            "floor": "floor",
                            "ceiling": "ceiling"
                        }
                        # Apply to specific exterior component
                        self.scene_manager.set_room_color(
                            self.current_color, opacity, component_map.get(component, component)
                        )
                
                # Update status message based on view type and component
                component_name = component.replace('_', ' ').title()
                if hasattr(self.main_window, 'update_status'):
                    self.main_window.update_status(
                        f"Applied {self.current_color_name} color to {view_type} {component_name}"
                    )
        else:
            if object_type == "Door":
                self.scene_manager.set_color_by_type(
                    "door", self.current_color, opacity
                )
            elif object_type == "Window":
                self.scene_manager.set_color_by_type(
                    "window", self.current_color, opacity
                )
            elif object_type == "Furniture":
                self.scene_manager.set_color_by_type(
                    "furniture", self.current_color, opacity
                )
            if hasattr(self.main_window, 'update_status'):
                self.main_window.update_status(
                    f"Applied {self.current_color_name} color to all {object_type}s"
                )
    
    def on_room_type_changed(self):
        """Handle room type selection change"""
        room_type = self.room_type_var.get()
        self.main_window.update_status(f"Selected room type: {room_type}")
    
    def on_dimension_changed(self, dimension):
        """Handle room dimension change"""
        # This will be called when dimensions are changed via spinbox
        pass
    
    def apply_room_settings(self):
        """Apply room settings to the scene"""
        room_type = self.room_type_var.get()
        width = self.width_var.get()
        length = self.length_var.get()
        height = self.height_var.get()
        
        # Update scene with room settings
        self.scene_manager.set_room(room_type, width, length, height)
        self.main_window.update_status(f"Applied {room_type} settings: {width}m x {length}m x {height}m")
    
    def add_door(self):
        """Add door to the scene"""
        door_type = self.door_type_var.get()
        width = self.door_width_var.get()
        height = self.door_height_var.get()
        thickness = self.door_thickness_var.get()
        
        # Add door to scene with thickness parameter
        door = self.scene_manager.add_door(door_type, width, height, thickness=thickness)
        self.main_window.update_status(f"Added {door_type} ({width}m x {height}m x {thickness}m)")
    
    def add_window(self):
        """Add window to the scene"""
        window_type = self.window_type_var.get()
        width = self.window_width_var.get()
        height = self.window_height_var.get()
        
        # Add window to scene
        self.scene_manager.add_window(window_type, width, height)
        self.main_window.update_status(f"Added {window_type} ({width}m x {height}m)")
    
    def remove_selected_window(self):
        """Remove the selected window from the scene"""
        # Check if an object is selected
        if self.scene_manager.selected_object is None:
            self.main_window.update_status("No window selected")
            return
            
        # Check if the selected object is a window
        from src.models.window import Window
        if not isinstance(self.scene_manager.selected_object, Window):
            self.main_window.update_status("Selected object is not a window")
            return
            
        # Delete the selected window
        object_id = self.scene_manager.selected_object.get_id()
        if self.scene_manager.delete_object(object_id):
            self.main_window.update_status("Window removed")
            # Hide properties panel since object is gone
            self.properties_frame.pack_forget()
            self.no_selection_label.pack(pady=20)
    
    def on_furniture_category_changed(self, event):
        """Handle furniture category change"""
        category = self.furniture_category_var.get()
        self.populate_furniture_items(category)
    
    def populate_furniture_items(self, category):
        """Populate furniture items based on category"""
        # Clear existing items
        for widget in self.furniture_items_frame.winfo_children():
            widget.destroy()
        
        # Add items based on category
        items = []
        if category == "Chairs":
            items = ["Dining Chair", "Office Chair", "Armchair"]
        elif category == "Tables":
            items = ["Dining Table", "Coffee Table", "Desk"]
        elif category == "Sofas":
            items = ["2-Seater Sofa", "3-Seater Sofa", "L-Shaped Sofa"]
        elif category == "Beds":
            items = ["Single Bed", "Double Bed", "King Size Bed"]
        elif category == "Cupboards":
            items = ["Single Door Cupboard", "Double Door Cupboard", "Sliding Door Cupboard"]
        
        # Create a variable to store selection
        self.furniture_item_var = tk.StringVar(value=items[0] if items else "")
        
        # Create radio buttons for each item
        for item in items:
            ttk.Radiobutton(self.furniture_items_frame, text=item, value=item, 
                          variable=self.furniture_item_var).pack(anchor=tk.W, padx=10, pady=2)
    
    def add_furniture(self):
        """Add selected furniture to the scene"""
        furniture_type = self.furniture_item_var.get()
        
        if furniture_type:
            # Get default dimensions for this furniture type
            dimensions = self.scene_manager._get_furniture_dimensions(furniture_type)
            
            # Add furniture to scene with proper dimensions
            category = self.furniture_category_var.get()
            self.scene_manager.add_furniture(
                furniture_type=furniture_type,
                width=dimensions["width"],
                depth=dimensions["depth"],
                height=dimensions["height"],
                position=None,
                rotation=None
            )
            self.main_window.update_status(f"Added {furniture_type} to scene")
    
    def on_property_changed(self, property_type, axis):
        """Handle property change for selected object"""
        # Handle property change based on type and axis
        if property_type == "position":
            x = self.pos_x_var.get()
            y = self.pos_y_var.get()
            z = self.pos_z_var.get()
            self.scene_manager.set_selected_object_position(x, y, z)
        elif property_type == "rotation":
            x_rot = self.rot_x_var.get()
            y_rot = self.rot_y_var.get()
            z_rot = self.rot_z_var.get()
            self.scene_manager.set_selected_object_rotation(x_rot, y_rot, z_rot)
    
    def delete_selected_object(self):
        """Delete the selected object from the scene"""
        if self.scene_manager.delete_selected_object():
            self.main_window.update_status("Object deleted")
            # Hide properties panel
            self.properties_frame.pack_forget()
            self.no_selection_label.pack(pady=20)
    
    def show_object_properties(self, obj):
        """Show properties for selected object"""
        # Hide no selection message
        self.no_selection_label.pack_forget()
        
        # Update position values
        self.pos_x_var.set(obj.position[0])
        self.pos_y_var.set(obj.position[1])
        self.pos_z_var.set(obj.position[2])
        
        # Update rotation values
        self.rot_x_var.set(obj.rotation[0])
        self.rot_y_var.set(obj.rotation[1])
        self.rot_z_var.set(obj.rotation[2])
        
        # Show properties frame
        self.properties_frame.pack(fill=tk.BOTH, expand=True)
    
    def remove_selected_door(self):
        """Remove the selected door from the scene"""
        # Check if an object is selected
        if self.scene_manager.selected_object is None:
            self.main_window.update_status("No door selected")
            return
            
        # Check if the selected object is a door
        from src.models.door import Door
        if not isinstance(self.scene_manager.selected_object, Door):
            self.main_window.update_status("Selected object is not a door")
            return
            
        # Delete the selected door
        object_id = self.scene_manager.selected_object.get_id()
        if self.scene_manager.delete_object(object_id):
            self.main_window.update_status("Door removed")
            # Hide properties panel since object is gone
            self.properties_frame.pack_forget()
            self.no_selection_label.pack(pady=20)
    
    def remove_selected_furniture(self):
        """Remove the selected furniture from the scene"""
        # Check if an object is selected
        if self.scene_manager.selected_object is None:
            self.main_window.update_status("No furniture selected")
            return
            
        # Check if the selected object is furniture
        from src.models.furniture import Furniture
        if not isinstance(self.scene_manager.selected_object, Furniture):
            self.main_window.update_status("Selected object is not furniture")
            return
            
        # Delete the selected furniture
        object_id = self.scene_manager.selected_object.get_id()
        if self.scene_manager.delete_object(object_id):
            self.main_window.update_status("Furniture removed")
            # Hide properties panel since object is gone
            self.properties_frame.pack_forget()
            self.no_selection_label.pack(pady=20)
    
    def choose_surface_color(self, color_attr):
        """Choose color for interior surface"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Choose Interior Color")
        if color[1]:
            self.interior_surface_vars[color_attr].set(color[1])
    
    def choose_exterior_surface_color(self, color_attr):
        """Choose color for exterior surface"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Choose Exterior Color")
        if color[1]:
            self.exterior_surface_vars[color_attr].set(color[1])
    
    def apply_interior_surface_settings(self):
        """Apply interior surface settings"""
        room = self.scene_manager.room
        if not room:
            return
        # Set color and opacity for each interior surface
        for color_attr, color_var in self.interior_surface_vars.items():
            hex_color = color_var.get()
            if hex_color:
                setattr(room, color_attr, self._hex_to_rgb(hex_color))
        for opacity_attr, opacity_var in self.interior_opacity_vars.items():
            value = opacity_var.get() / 100.0
            setattr(room, opacity_attr, value)
        if hasattr(self.main_window, 'update_status'):
            self.main_window.update_status("Applied interior surface settings.")
    
    def apply_exterior_surface_settings(self):
        """Apply exterior surface settings"""
        room = self.scene_manager.room
        if not room:
            return
            
        # Track if we've modified individual walls
        modified_walls = False
            
        # Set color and opacity for each exterior surface
        for color_attr, color_var in self.exterior_surface_vars.items():
            hex_color = color_var.get()
            if hex_color:
                setattr(room, color_attr, self._hex_to_rgb(hex_color))
                
                # Track if individual walls were modified
                if color_attr in ["north_wall_color", "south_wall_color", "east_wall_color", "west_wall_color"]:
                    modified_walls = True
                    
        for opacity_attr, opacity_var in self.exterior_opacity_vars.items():
            value = opacity_var.get() / 100.0
            setattr(room, opacity_attr, value)
            
        # Force an update to ensure the renderer reflects the changes
        # This ensures the room model gets refreshed in the 3D view
        if modified_walls:
            # If any individual wall color was changed, make sure the general wall color
            # is changed too, so it displays correctly in the scene
            avg_color = [0.0, 0.0, 0.0]
            count = 0
            
            # Average the wall colors that have been explicitly set
            if room._north_wall_color is not None:
                avg_color = [a+b for a,b in zip(avg_color, room.north_wall_color)]
                count += 1
            if room._south_wall_color is not None:
                avg_color = [a+b for a,b in zip(avg_color, room.south_wall_color)]
                count += 1
            if room._east_wall_color is not None:
                avg_color = [a+b for a,b in zip(avg_color, room.east_wall_color)]
                count += 1
            if room._west_wall_color is not None:
                avg_color = [a+b for a,b in zip(avg_color, room.west_wall_color)]
                count += 1
                
            # If at least one wall was explicitly set, update the general wall color
            if count > 0:
                avg_color = [c/count for c in avg_color]
                room.wall_color = avg_color
                
        # Save state for undo
        self.scene_manager._save_state("Apply exterior surface settings")
                
        if hasattr(self.main_window, 'update_status'):
            self.main_window.update_status("Applied exterior surface settings.")

    def _hex_to_rgb(self, hex_color):
        """Convert hex color string to RGB array with values 0-1"""
        if isinstance(hex_color, (list, tuple)) and len(hex_color) >= 3:
            return hex_color
        hex_color = hex_color.lstrip('#')
        try:
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16) / 255.0
                g = int(hex_color[2:4], 16) / 255.0
                b = int(hex_color[4:6], 16) / 255.0
                return [r, g, b]
            elif len(hex_color) == 3:
                r = int(hex_color[0] + hex_color[0], 16) / 255.0
                g = int(hex_color[1] + hex_color[1], 16) / 255.0
                b = int(hex_color[2] + hex_color[2], 16) / 255.0
                return [r, g, b]
        except:
            pass
        return [1.0, 1.0, 1.0] 