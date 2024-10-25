import tkinter as tk
from ui.app import PDFViewerApp


def main():
    root = tk.Tk()
    app = PDFViewerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
