# models/pdf_item.py
import tkinter as tk
from tkinter import ttk

class PDFListItem:
    def __init__(self, parent, pdf_file, index, file_handler, click_callback, flag_callback):
        self.parent = parent
        self.pdf_file = pdf_file
        self.index = index
        self.file_handler = file_handler
        self.click_callback = click_callback
        self.flag_callback = flag_callback
        
        # Colors
        self.completed_color = "#00FF00"    # Bright green
        self.flagged_color = "#FF0000"      # Bright red
        self.default_color = "white"
        self.separator_color = "#404040"     # Dark gray for separator
        self.selected_bg = "#0066cc"        # Bright blue for selection
        self.hover_bg = "#3a3a3a"           # Slightly lighter than default for hover
        self.default_bg = "#2F2F2F"         # Default background
        
        self.setup_ui()

    def setup_ui(self):
        # Create main frame
        self.frame = ttk.Frame(self.parent, style="Sidebar.TFrame")
        self.frame.pack(fill=tk.X)

        # Create content frame with background control
        self.content_frame = tk.Frame(
            self.frame,
            background=self.default_bg
        )
        self.content_frame.pack(fill=tk.X, pady=5)

        # Create checkbox with custom colors
        self.var = tk.BooleanVar(
            value=self.file_handler.flags_dict.get(self.pdf_file, False)
        )
        self.checkbox = tk.Checkbutton(
            self.content_frame,
            variable=self.var,
            bg=self.default_bg,
            fg=self.default_color,
            selectcolor=self.default_bg,
            activebackground=self.default_bg,
            command=self.on_flag_toggle,
            cursor="hand2"
        )
        self.checkbox.pack(side=tk.LEFT, padx=(5, 10))

        # Create label with initial state
        is_completed = (
            self.pdf_file in self.file_handler.notes_dict
            and self.file_handler.notes_dict[self.pdf_file]
        )
        prefix = "✓ " if is_completed else "  "
        
        # Label frame for background control
        self.label_frame = tk.Frame(
            self.content_frame,
            background=self.default_bg
        )
        self.label_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.label = tk.Label(
            self.label_frame,
            text=f"{prefix}{self.pdf_file}",
            background=self.default_bg,
            foreground=self.default_color,
            font=("Arial", 10),
            cursor="hand2",
            padx=5  # Add some padding for better text appearance
        )
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Add separator line
        self.separator = tk.Frame(
            self.frame,
            height=1,
            background=self.separator_color
        )
        self.separator.pack(fill=tk.X, side=tk.BOTTOM)

        # Bind click events to all relevant widgets
        for widget in [self.label, self.label_frame, self.content_frame]:
            widget.bind("<Button-1>", lambda e: self.on_click())
            widget.bind("<Enter>", lambda e: self.on_hover_enter())
            widget.bind("<Leave>", lambda e: self.on_hover_leave())

        # Initial appearance update
        self.update_appearance()

    def is_selected(self):
        """Check if this item is currently selected"""
        if hasattr(self.file_handler, 'sidebar'):
            return self.index == self.file_handler.sidebar.current_pdf_index
        return False

    def on_hover_enter(self):
        if not self.is_selected():
            self._update_background(self.hover_bg)

    def on_hover_leave(self):
        self.update_appearance()

    def _update_background(self, color):
        """Helper method to update background color of all relevant widgets"""
        for widget in [self.content_frame, self.label_frame, self.label, self.checkbox]:
            widget.configure(background=color)

    def on_click(self):
        if self.click_callback:
            self.click_callback(self.index)

    def on_flag_toggle(self):
        try:
            self.file_handler.flags_dict[self.pdf_file] = self.var.get()
            if self.flag_callback:
                self.flag_callback(self.pdf_file)
        except Exception as e:
            print(f"Error toggling flag: {e}")
            
    def toggle_flag(self):
        try:
            current_state = self.var.get()
            self.var.set(not current_state)
            self.on_flag_toggle()
        except Exception as e:
            print(f"Error in toggle_flag: {e}")

    def update_appearance(self):
        try:
            # Get current states
            is_completed = (
                self.pdf_file in self.file_handler.notes_dict
                and self.file_handler.notes_dict[self.pdf_file]
            )
            is_flagged = self.file_handler.flags_dict.get(self.pdf_file, False)
            is_selected = self.is_selected()
            
            # Update checkmark prefix
            prefix = "✓ " if is_completed else "  "
            
            # Update all components only if they still exist
            if self.label.winfo_exists():
                self.label.configure(text=f"{prefix}{self.pdf_file}")
                
                # Set background color based on selection
                bg_color = self.selected_bg if is_selected else self.default_bg
                
                # Update all widget backgrounds
                for widget in [self.content_frame, self.label_frame, self.label, self.checkbox]:
                    if widget.winfo_exists():
                        widget.configure(background=bg_color)
                
                # Update text colors based on status
                if is_flagged:
                    self.label.configure(foreground=self.flagged_color)
                    self.checkbox.configure(fg=self.flagged_color)
                elif is_completed:
                    self.label.configure(foreground=self.completed_color)
                    self.checkbox.configure(fg=self.completed_color)
                else:
                    self.label.configure(foreground=self.default_color)
                    self.checkbox.configure(fg=self.default_color)
        except Exception as e:
            print(f"Error updating appearance: {e}")