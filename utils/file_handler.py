# utils/file_handler.py
import os
import csv
from tkinter import filedialog

class FileHandler:
    def __init__(self):
        self.current_directory = None
        self.pdf_files = []
        self.notes_dict = {}
        self.flags_dict = {}
        self.directory_callback = None
        self.sidebar = None  # Add this line to store sidebar reference

    def set_directory_callback(self, callback):
        """Set callback function to be called when directory is selected"""
        self.directory_callback = callback

    def is_valid_pdf(self, filename):
        """Check if file is a valid PDF and not a hidden file"""
        # Exclude hidden files (starting with .)
        if filename.startswith('.'):
            return False
        # Exclude macOS metadata files
        if filename.startswith('._'):
            return False
        # Check for .pdf extension (case insensitive)
        return filename.lower().endswith('.pdf')

    def select_directory(self):
        """Select directory and load PDF files"""
        self.current_directory = filedialog.askdirectory()
        if self.current_directory:
            # Filter out hidden files and get only valid PDFs
            self.pdf_files = [
                f for f in os.listdir(self.current_directory)
                if self.is_valid_pdf(f)
            ]
            # Sort files alphabetically
            self.pdf_files.sort()
            
            self.load_existing_notes()
            
            if self.directory_callback:
                self.directory_callback()
            
            return True
        return False

    def get_pdf_path(self, pdf_file):
        """Get full path for a PDF file"""
        return os.path.join(self.current_directory, pdf_file)

    def save_to_csv(self):
        """Save notes and flags to CSV file"""
        if not self.current_directory:
            return

        csv_path = os.path.join(self.current_directory, "pdf_notes.csv")
        with open(csv_path, "w", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["PDF File", "Note", "Flagged"])
            for pdf_file in self.pdf_files:
                note = self.notes_dict.get(pdf_file, "")
                flagged = "1" if self.flags_dict.get(pdf_file, False) else "0"
                writer.writerow([pdf_file, note, flagged])

    def load_existing_notes(self):
        """Load existing notes and flags from CSV file"""
        csv_path = os.path.join(self.current_directory, "pdf_notes.csv")
        self.notes_dict = {}
        self.flags_dict = {}
        if os.path.exists(csv_path):
            with open(csv_path, "r", newline="", encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader)  # Skip header row
                for row in reader:
                    if len(row) >= 3:
                        pdf_file, note, flagged = row
                        if note:
                            self.notes_dict[pdf_file] = note
                        self.flags_dict[pdf_file] = flagged == "1"
                    elif len(row) == 2:
                        pdf_file, note = row
                        if note:
                            self.notes_dict[pdf_file] = note