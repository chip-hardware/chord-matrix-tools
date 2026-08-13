import pdfplumber
import re
from pathlib import Path
from typing import Dict, List, Optional
import json

class PDFExtractor:
    def __init__(self, pdf_path: str):
        self.pdf_path = Path(pdf_path)
        self.text = ""
    
    def extract_all_pages(self) -> str:
        """Витягує весь текст з PDF"""
        full_text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += f"\n--- PAGE {page.page_number} ---\n"
                    full_text += text
        self.text = full_text
        return self.text
    
    def extract_page_range(self, start: int, end: int) -> str:
        """Витягує діапазон сторінок"""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for i in range(start - 1, end):
                if i < len(pdf.pages):
                    text += pdf.pages[i].extract_text() or ""
        return text
    
    def extract_images(self, output_dir: str):
        """Витягує зображення (ноти, аплікатури)"""
        import fitz
        pdf = fitz.open(self.pdf_path)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for page_num in range(len(pdf)):
            page = pdf[page_num]
            images = page.get_images()
            for img_index, img in enumerate(images):
                xref = img[0]
                pix = fitz.Pixmap(pdf, xref)
                if pix.n - pix.alpha < 4:
                    pix.save(output_path / f"page_{page_num+1}_img_{img_index}.png")
        pdf.close()  # <-- Тут закриваємо PDF
    
    def save_text(self, output_path: str = "data/raw/extracted_text.txt"):
        """Зберігає витягнутий текст у файл"""
        if not self.text:
            self.extract_all_pages()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self.text)
        return output_path