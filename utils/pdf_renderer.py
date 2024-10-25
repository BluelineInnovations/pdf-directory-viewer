# utils/pdf_renderer.py
import fitz
from PIL import Image, ImageTk


class PDFRenderer:
    def __init__(self):
        self.zoom = 30
        self.target_width = 1200

    def render_pdf(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            page = doc[0]
            rect = page.rect

            # Focus on top-right portion
            top_right_rect = fitz.Rect(
                rect.width * 0.5, 0, rect.width, rect.height * 0.3
            )

            # Create matrix for zoom
            mat = fitz.Matrix(self.zoom, self.zoom)

            # Get pixmap
            pix = page.get_pixmap(matrix=mat, clip=top_right_rect)

            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Resize if needed
            if img.width > self.target_width:
                ratio = self.target_width / img.width
                target_height = int(img.height * ratio)
                img = img.resize(
                    (self.target_width, target_height), Image.Resampling.LANCZOS
                )

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)

            doc.close()
            return photo

        except Exception as e:
            print(f"Error rendering PDF: {e}")
            return None
