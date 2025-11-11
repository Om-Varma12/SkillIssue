"""
File Utilities
Handles reading PDF and text files
"""

import os
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
except ImportError:
    os.system('pip install pdfplumber')
    import pdfplumber


class FileUtils:
    """Utility class for file operations"""
    
    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        """
        Read file based on extension
        Supports .pdf and .txt files
        """
        path = Path(file_path)
        
        if not path.exists():
            return None
        
        if path.suffix.lower() == '.pdf':
            return FileUtils.extract_text_from_pdf(str(path))
        else:
            return FileUtils.read_text_file(str(path))
    
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> Optional[str]:
        """Extract text from PDF file using pdfplumber"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip() if text else None
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return None
    
    @staticmethod
    def read_text_file(file_path: str) -> Optional[str]:
        """Read plain text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            return text.strip() if text else None
        except Exception as e:
            print(f"Error reading text file: {e}")
            return None
    
    @staticmethod
    def find_resume_in_assets(assets_dir: Path) -> Optional[Path]:
        """Find resume file in assets directory"""
        for ext in ['.pdf', '.txt', '.docx']:
            candidate = assets_dir / f"resume{ext}"
            if candidate.exists():
                return candidate
        return None