# ui/app.py
import tkinter as tk
from tkinter import ttk
from .sidebar import Sidebar
from .pdf_viewer import PDFViewer
from utils.file_handler import FileHandler

class PDFViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Directory Viewer")
        self.root.geometry("1400x800")
        
        self.file_handler = FileHandler()
        self.file_handler.set_directory_callback(self.on_directory_selected)
        
        self.setup_styles()
        self.setup_ui()
        self.bind_shortcuts()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('Consolas.TEntry', font=('Consolas', 24))
        style.configure('Sidebar.TFrame', background='#2F2F2F')
        style.configure('SidebarButton.TButton', font=('Arial', 10))
        style.configure('Counter.TLabel', 
                       background='#2F2F2F',
                       foreground='white',
                       font=('Arial', 16, 'bold'))
        # Add separator style
        style.configure('Separator.TFrame', 
                       background='#404040',  # Dark gray color for the separator
                       height=1)
        
    def setup_ui(self):
        # Create sidebar
        self.sidebar = Sidebar(self.root, self.file_handler)
        
        # Create PDF viewer
        self.pdf_viewer = PDFViewer(self.root, self.file_handler)
        
        # Connect sidebar and PDF viewer
        self.sidebar.set_pdf_viewer(self.pdf_viewer)
        self.pdf_viewer.set_sidebar(self.sidebar)
    
    def bind_shortcuts(self):
        self.root.bind('<Control-n>', lambda e: self.sidebar.next_pdf())
        self.root.bind('<Control-N>', lambda e: self.sidebar.next_pdf())
        self.root.bind('<Control-p>', lambda e: self.sidebar.previous_pdf())
        self.root.bind('<Control-P>', lambda e: self.sidebar.previous_pdf())
        self.root.bind('<Up>', lambda e: self.sidebar.previous_pdf())
        self.root.bind('<Down>', lambda e: self.sidebar.next_pdf())
        self.root.bind('<Control-f>', lambda e: self.sidebar.toggle_flag())
        self.root.bind('<Control-F>', lambda e: self.sidebar.toggle_flag())
    
    def on_directory_selected(self):
        # Update sidebar when directory is selected
        self.sidebar.update_pdf_list()
        self.sidebar.update_counter_label()
        
        # Select first PDF if available
        if self.file_handler.pdf_files:
            self.sidebar.on_item_click(0)