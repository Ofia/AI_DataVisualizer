import os
from .pdf_extractor import PDFExtractor
from .excel_extractor import ExcelExtractor
from .csv_extractor import CSVExtractor
from .image_extractor import ImageExtractor

class ExtractorFactory:
    """Factory to get the appropriate data extractor based on file type"""
    
    @staticmethod
    def get_extractor(filepath):
        """
        Get the appropriate extractor for the file
        
        Args:
            filepath: Path to the file
            
        Returns:
            Appropriate extractor instance
            
        Raises:
            ValueError: If file type is not supported
        """
        if not os.path.exists(filepath):
            raise ValueError(f"File not found: {filepath}")
        
        extension = os.path.splitext(filepath)[1].lower()
        
        if extension == '.pdf':
            return PDFExtractor(filepath)
        elif extension in ['.xlsx', '.xls']:
            return ExcelExtractor(filepath)
        elif extension == '.csv':
            return CSVExtractor(filepath)
        elif extension in ['.png', '.jpg', '.jpeg']:
            return ImageExtractor(filepath)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
