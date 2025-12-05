import pdfplumber
import pandas as pd

class PDFExtractor:
    """Extract data from PDF files"""
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def extract(self):
        """Extract tables and text from PDF"""
        try:
            data = {
                'type': 'pdf',
                'tables': [],
                'text': '',
                'columns': [],
                'sample_data': [],
                'row_count': 0,
                'column_count': 0
            }
            
            with pdfplumber.open(self.filepath) as pdf:
                all_text = []
                
                for page in pdf.pages:
                    # Extract text
                    text = page.extract_text()
                    if text:
                        all_text.append(text)
                    
                    # Extract tables
                    tables = page.extract_tables()
                    for table in tables:
                        if table and len(table) > 0:
                            # Convert to DataFrame
                            df = pd.DataFrame(table[1:], columns=table[0])
                            data['tables'].append(df.to_dict('records'))
                            
                            # Update metadata from first table
                            if not data['columns']:
                                data['columns'] = list(df.columns)
                                data['sample_data'] = df.head(5).to_dict('records')
                                data['row_count'] = len(df)
                                data['column_count'] = len(df.columns)
                
                data['text'] = '\n'.join(all_text)
                data['preview'] = f"Extracted {len(data['tables'])} table(s) from PDF"
                
                return data
                
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
