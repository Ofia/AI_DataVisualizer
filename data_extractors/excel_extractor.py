import pandas as pd

class ExcelExtractor:
    """Extract data from Excel files"""
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def extract(self):
        """Extract data from Excel file"""
        try:
            # Read Excel file
            df = pd.read_excel(self.filepath)
            
            data = {
                'type': 'excel',
                'columns': list(df.columns),
                'sample_data': df.head(10).to_dict('records'),
                'row_count': len(df),
                'column_count': len(df.columns),
                'dataframe': df.to_dict('records'),
                'preview': f"Extracted {len(df)} rows and {len(df.columns)} columns from Excel"
            }
            
            return data
            
        except Exception as e:
            raise Exception(f"Error extracting Excel: {str(e)}")
