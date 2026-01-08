from PIL import Image
import pytesseract
import os

class ImageExtractor:
    """Extract data from images using OCR"""
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def extract(self):
        """Extract text from image and return for AI vision analysis"""
        try:
            # For images, we'll primarily rely on AI vision
            # But we can also do basic OCR as fallback
            
            data = {
                'type': 'image',
                'image_path': self.filepath,
                'columns': [],
                'sample_data': [],
                'row_count': 0,
                'column_count': 0,
                'preview': 'Image ready for AI vision analysis'
            }
            
            # Try OCR (optional, as AI vision will be primary)
            try:
                image = Image.open(self.filepath)
                ocr_text = pytesseract.image_to_string(image)
                data['ocr_text'] = ocr_text
                data['preview'] = f"Image analyzed. OCR extracted {len(ocr_text)} characters"
            except Exception as ocr_error:
                # OCR might fail if tesseract is not installed
                # That's okay, we'll rely on AI vision
                data['ocr_text'] = ""
                data['preview'] = "Image ready for AI vision analysis (OCR not available)"
            
            return data
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
