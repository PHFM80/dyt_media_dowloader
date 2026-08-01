#services\file_reader_service.py
from pathlib import Path
from typing import List
from docx import Document


class FileReaderService:
    """Servicio para leer URLs desde archivos"""
    
    @staticmethod
    def read_from_docx(file_path: str) -> List[str]:
        """Lee URLs desde un archivo DOCX"""
        try:
            doc = Document(file_path)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
            
            from services.url_cleaner_service import URLCleanerService
            return URLCleanerService.extract_urls_from_text(text)
        except Exception as e:
            raise Exception(f"Error al leer archivo DOCX: {str(e)}")
    
    @staticmethod
    def read_from_txt(file_path: str) -> List[str]:
        """Lee URLs desde un archivo TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            from services.url_cleaner_service import URLCleanerService
            return URLCleanerService.extract_urls_from_text(text)
        except Exception as e:
            raise Exception(f"Error al leer archivo TXT: {str(e)}")
    
    @staticmethod
    def read_file(file_path: str) -> List[str]:
        """Lee URLs desde un archivo (detecta formato automáticamente)"""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")
        
        extension = path.suffix.lower()
        
        if extension == '.docx':
            return FileReaderService.read_from_docx(file_path)
        elif extension == '.txt':
            return FileReaderService.read_from_txt(file_path)
        else:
            raise ValueError(f"Formato no soportado: {extension}")