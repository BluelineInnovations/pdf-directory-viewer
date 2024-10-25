# ui/pdf_viewer.py
import tkinter as tk
from tkinter import ttk, messagebox
from utils.pdf_renderer import PDFRenderer

class PDFViewer:
    def __init__(self, parent, file_handler):
        self.parent = parent
        self.file_handler = file_handler
        self.sidebar = None
        self.pdf_renderer = PDFRenderer()
        self.current_image = None  # Keep track of the current image
        
        self.setup_ui()

    def setup_ui(self):
        self.frame = ttk.Frame(self.parent, padding="20")
        self.frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Note input area
        self.setup_note_input()

        # Note display
        self.note_display = ttk.Label(
            self.frame,
            text="",
            wraplength=800,
            font=("Consolas", 32, "bold"),
            justify="center",
        )
        self.note_display.pack(pady=(20, 20))

        # Create a frame to contain the canvas
        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.pack(pady=5, anchor="center")

        # PDF display canvas with fixed initial size
        self.pdf_canvas = tk.Canvas(
            self.canvas_frame,
            bg="white",
            width=1200,
            height=400,
            highlightthickness=0
        )
        self.pdf_canvas.pack(pady=5, anchor="center")

        # Shortcuts display
        self.show_shortcuts()

    def setup_note_input(self):
        input_container = ttk.Frame(self.frame)
        input_container.pack(fill=tk.X, pady=(0, 10))

        input_frame = ttk.Frame(input_container)
        input_frame.pack(anchor="center")

        # Create StringVar to handle text transformation
        self.note_var = tk.StringVar()
        self.note_var.trace('w', self._enforce_uppercase)

        self.note_input = ttk.Entry(
            input_frame,
            width=150,
            font=("Consolas", 24),
            style="Consolas.TEntry",
            textvariable=self.note_var  # Bind to StringVar
        )
        self.note_input.pack(side=tk.LEFT, padx=5)
        self.note_input.bind("<Return>", self.handle_enter)

        ttk.Button(
            input_frame,
            text="Save Note",
            command=self.save_note
        ).pack(side=tk.LEFT)

    def _enforce_uppercase(self, *args):
        """Convert input text to uppercase"""
        value = self.note_var.get()
        if value != value.upper():
            self.note_var.set(value.upper())

    def show_shortcuts(self):
        shortcuts = """
        Keyboard Shortcuts:
        ↑: Previous PDF
        ↓: Next PDF
        Ctrl+N: Next PDF
        Ctrl+P: Previous PDF
        Enter: Save Note & Next PDF
        Ctrl+F: Toggle Flag
        """
        ttk.Label(self.frame, text=shortcuts).pack(pady=10)

    def set_sidebar(self, sidebar):
        self.sidebar = sidebar

    def display_pdf(self, pdf_file):
        try:
            # Clear existing note input and set focus
            existing_note = self.file_handler.notes_dict.get(pdf_file, "")
            self.note_var.set(existing_note.upper())  # Use StringVar and ensure uppercase
            self.note_input.focus_set()

            # Render PDF
            img = self.pdf_renderer.render_pdf(self.file_handler.get_pdf_path(pdf_file))

            if img:
                # Store the PhotoImage reference
                self.current_image = img
                
                # Get the image dimensions
                width = img.width()
                height = img.height()

                # Update canvas size if needed
                if width > 0 and height > 0:
                    self.pdf_canvas.configure(width=width, height=height)
                
                # Clear existing content and display new image
                self.pdf_canvas.delete("all")
                self.pdf_canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
                
            self.update_note_display()

        except Exception as e:
            print(f"Error displaying PDF: {e}")
            messagebox.showerror("Error", f"Failed to display PDF: {str(e)}")

    def handle_enter(self, event):
        self.save_note()
        if self.sidebar:
            self.sidebar.next_pdf()
        return "break"

    def save_note(self):
        note = self.note_var.get().strip()  # Use StringVar instead of direct get()
        if note and self.sidebar.current_pdf_index >= 0:
            current_pdf = self.file_handler.pdf_files[self.sidebar.current_pdf_index]
            self.file_handler.notes_dict[current_pdf] = note
            self.file_handler.save_to_csv()
            self.note_var.set("")  # Clear using StringVar
            self.update_note_display()
            if self.sidebar:
                self.sidebar.update_pdf_list()
                self.sidebar.highlight_selected_item()

    def update_note_display(self):
        if hasattr(self.sidebar, 'current_pdf_index') and self.sidebar.current_pdf_index >= 0:
            current_pdf = self.file_handler.pdf_files[self.sidebar.current_pdf_index]
            note = self.file_handler.notes_dict.get(current_pdf, "")
            self.note_display.config(text=note.upper())  # Ensure displayed note is uppercase