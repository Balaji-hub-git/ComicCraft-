import os
from datetime import datetime
from fpdf import FPDF

class ComicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "ComicCraft - AI Generated Story", ln=True, align="C")
        self.ln(5)

def save_pdf(layout: list) -> str:
    """Compiles comic panels, titles, and narration into a PDF document."""
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    export_folder = os.path.join("static", "exports")
    os.makedirs(export_folder, exist_ok=True)

    for panel in layout:
        pdf.add_page()
        
        # Title
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", ln=True, align="C")
        pdf.ln(5)
        
        # Image Placement
        img_path = panel['image_path']
        if os.path.exists(img_path):
            pdf.image(img_path, x=25, y=35, w=160, h=100)
            pdf.set_y(145)
        else:
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 10, f"Image file missing: {img_path}", ln=True)
            pdf.set_y(50)
            
        # Narration Text
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 7, panel['text'])

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(export_folder, filename)
    pdf.output(pdf_path)
    
    return pdf_path