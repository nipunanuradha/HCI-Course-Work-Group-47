import tkinter as tk
from src.ui.main_window import MainWindow

def main():
    """
    Main entry point for the 3D Room and Furniture Modeling System
    """
    root = tk.Tk()
    root.title("LifeFurniture 3D Room and Furniture Modeling System")
    root.geometry("1280x720")
    
    # Create main application window
    app = MainWindow(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()  