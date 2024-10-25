# ui/sidebar.py
import tkinter as tk
from tkinter import ttk
from models.pdf_item import PDFListItem
import platform

class Sidebar:
    def __init__(self, parent, file_handler):
        self.parent = parent
        self.file_handler = file_handler
        self.pdf_viewer = None
        self.current_pdf_index = -1
        self.list_items = {}
        
        # Link sidebar to file handler
        self.file_handler.sidebar = self
        
        self.setup_ui()

    def setup_ui(self):
        """Initialize the main UI components of the sidebar"""
        self.frame = ttk.Frame(self.parent, style="Sidebar.TFrame")
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH)

        sidebar_content = ttk.Frame(self.frame, style="Sidebar.TFrame", padding="10")
        sidebar_content.pack(fill=tk.BOTH, expand=True)

        # Directory selection button
        ttk.Button(
            sidebar_content,
            text="Select Directory",
            command=self.file_handler.select_directory,
            style="SidebarButton.TButton",
        ).pack(fill=tk.X, pady=(0, 5))

        # Counter label
        self.counter_label = ttk.Label(
            sidebar_content, text="No PDFs loaded", style="Counter.TLabel"
        )
        self.counter_label.pack(fill=tk.X, pady=5)

        # Scrollable list container
        self.setup_scrollable_list(sidebar_content)

    def setup_scrollable_list(self, parent):
        """Set up the scrollable list container with platform-specific scroll handling"""
        # Container frame
        self.list_container = ttk.Frame(parent, style="Sidebar.TFrame")
        self.list_container.pack(fill=tk.BOTH, expand=True)

        # Canvas and scrollbar
        self.canvas = tk.Canvas(
            self.list_container,
            bg="#2F2F2F",
            highlightthickness=0,
            width=200
        )
        self.scrollbar = ttk.Scrollbar(
            self.list_container,
            orient="vertical",
            command=self.canvas.yview
        )

        # Scrollable frame for content
        self.scrollable_frame = ttk.Frame(self.canvas, style="Sidebar.TFrame")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_width())

        # Configure canvas scroll
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack everything
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Platform-specific mousewheel bindings
        if platform.system() == "Windows":
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_windows)
        else:
            self.canvas.bind_all("<MouseWheel>", self._on_mousewheel_unix)
            self.canvas.bind_all("<Button-4>", self._on_mousewheel_unix)
            self.canvas.bind_all("<Button-5>", self._on_mousewheel_unix)
        
        # Bind canvas resize
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_mousewheel_windows(self, event):
        """Handle mousewheel events specifically for Windows"""
        self.canvas.yview_scroll(int(-1 * (event.delta/120)), "units")

    def _on_mousewheel_unix(self, event):
        """Handle mousewheel events for Unix-based systems (macOS and Linux)"""
        if hasattr(event, 'num'):  # Linux
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        elif hasattr(event, 'delta'):  # macOS
            self.canvas.yview_scroll(int(-1 * (event.delta/120)), "units")

    def _on_canvas_configure(self, event):
        """Handle canvas resize events"""
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

    def set_pdf_viewer(self, pdf_viewer):
        """Set the associated PDF viewer instance"""
        self.pdf_viewer = pdf_viewer

    def on_item_click(self, index):
        """Handle click events on PDF items"""
        self.current_pdf_index = index
        self.highlight_selected_item()
        if self.pdf_viewer:
            self.pdf_viewer.display_pdf(self.file_handler.pdf_files[index])

    def highlight_selected_item(self):
        """Update the appearance of all items to reflect the current selection"""
        for item in self.list_items.values():
            item.update_appearance()

    def update_pdf_list(self):
        """Refresh the list of PDF items"""
        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.list_items.clear()

        # Create new items
        for i, pdf in enumerate(self.file_handler.pdf_files):
            self.list_items[pdf] = PDFListItem(
                self.scrollable_frame,
                pdf,
                i,
                self.file_handler,
                self.on_item_click,
                self.on_flag_toggle
            )
        
        # Update the counter and scroll region
        self.update_counter_label()
        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_counter_label(self):
        """Update the counter showing progress through PDF files"""
        if not self.file_handler.pdf_files:
            self.counter_label.config(text="No PDFs loaded")
        else:
            completed_count = sum(
                1 for pdf in self.file_handler.pdf_files
                if pdf in self.file_handler.notes_dict and self.file_handler.notes_dict[pdf]
            )
            total = len(self.file_handler.pdf_files)
            self.counter_label.config(text=f"PDF {completed_count} of {total}")

    def next_pdf(self):
        """Move to the next PDF in the list"""
        if self.current_pdf_index < len(self.file_handler.pdf_files) - 1:
            self.on_item_click(self.current_pdf_index + 1)
        return "break"

    def previous_pdf(self):
        """Move to the previous PDF in the list"""
        if self.current_pdf_index > 0:
            self.on_item_click(self.current_pdf_index - 1)
        return "break"

    def toggle_flag(self):
        """Toggle the flag status of the current PDF"""
        if self.current_pdf_index >= 0:
            pdf_file = self.file_handler.pdf_files[self.current_pdf_index]
            current_flag = self.file_handler.flags_dict.get(pdf_file, False)
            self.file_handler.flags_dict[pdf_file] = not current_flag
            self.file_handler.save_to_csv()
            
            if pdf_file in self.list_items:
                item = self.list_items[pdf_file]
                item.var.set(not current_flag)
                item.update_appearance()
        return "break"

    def on_flag_toggle(self, pdf_file):
        """Handle flag toggle events from PDF items"""
        self.file_handler.save_to_csv()
        if pdf_file in self.list_items:
            self.list_items[pdf_file].update_appearance()