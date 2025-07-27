# 3D Room and Furniture Modeling System

A Python-based 3D modeling system for designing and visualizing room layouts with furniture.

## Features

- **3D Room Modeling**: Create and customize different types of rooms (Dining Room, Living Room, Master Bedroom, Office Room)
- **Furniture Placement**: Add and position various furniture items in the 3D scene
- **Door and Window Customization**: Add different types of doors and windows to your room
- **Interactive Controls**: Rotate, move, and manipulate objects within the 3D environment
- **Modern UI**: User-friendly desktop interface built with Python and tkinter
- **Save/Load Functionality**: Save your designs and load them later for further editing
- **Export Capability**: Export your designs to common 3D formats

## Room Types

- Dining Room
- Living Room
- Master Bedroom
- Office Room

## Object Types

### Doors
- Single Door
- Double Door
- Sliding Door

### Windows
- Single Window
- Double Window
- Bay Window

### Furniture
- **Chairs**: Dining Chair, Office Chair, Armchair
- **Tables**: Dining Table, Coffee Table, Desk
- **Sofas**: 2-Seater Sofa, 3-Seater Sofa, L-Shaped Sofa
- **Beds**: Single Bed, Double Bed, King Size Bed

## Installation

### Prerequisites
- Python 3.7+
- OpenGL support on your system

### Setup

1. Clone this repository:
```
git clone <repository-url>
cd 3d-room-modeling-system
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

## System Requirements

- Operating System: Windows 10/11, macOS, or Linux
- Graphics: OpenGL 3.3+ compatible graphics card
- RAM: 4GB minimum, 8GB+ recommended
- Processor: Any modern dual-core CPU or better

## Usage

### Basic Controls

- **Left Mouse Button + Drag**: Rotate camera
- **Right Mouse Button + Drag**: Pan camera
- **Mouse Wheel**: Zoom in/out
- **Ctrl + Left Click**: Select object
- **Delete Key**: Delete selected object
- **Arrow Keys**: Move selected object
- **R + Arrow Keys**: Rotate selected object

### Adding Items

1. Select the type of item (Room, Door, Window, Furniture) from the sidebar
2. Configure the dimensions and properties
3. Click the "Add" button to place it in the scene

### Manipulating Objects

1. Select an object by clicking on it
2. Use the Properties panel to adjust position, rotation, etc.
3. Alternatively, use keyboard shortcuts for movement and rotation

### Saving and Loading

- Use File → Save to save your current layout
- Use File → Open to load a previously saved layout
- Use File → Export to export your design to other formats

## Project Structure

```
src/
  ├── ui/              # User interface components
  ├── rendering/       # OpenGL rendering code
  ├── interaction/     # User input handling
  ├── models/          # 3D object models and data
  └── storage/         # Save/load functionality
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with PyOpenGL and tkinter
- Inspired by the need for simple, accessible 3D room planning tools 
