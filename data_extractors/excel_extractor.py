import pandas as pd

class ExcelExtractor:
    """Extract data from Excel files"""
    
    def __init__(self, filepath):
        self.filepath = filepath
    
    def extract(self):
        """Extract data from Excel file with robust JSON sanitization"""
        try:
            # Read Excel file
            df = pd.read_excel(self.filepath)
            
            # Sanitize dataframe for JSON serialization
            df_sanitized = self._sanitize_dataframe(df)
            
            data = {
                'type': 'excel',
                'columns': list(df_sanitized.columns),
                'sample_data': df_sanitized.head(10).to_dict('records'),
                'row_count': len(df_sanitized),
                'column_count': len(df_sanitized.columns),
                'dataframe': df_sanitized.to_dict('records'),
                'preview': f"Extracted {len(df_sanitized)} rows and {len(df_sanitized.columns)} columns from Excel"
            }
            
            return data
            
        except Exception as e:
            raise Exception(f"Error extracting Excel: {str(e)}")
    
    def _sanitize_dataframe(self, df):
        """Sanitize dataframe to ensure JSON-safe values"""
        import numpy as np
        from datetime import datetime, date
        
        df_copy = df.copy()
        
        for col in df_copy.columns:
            # Convert column to appropriate type
            if df_copy[col].dtype == 'object':
                # Handle datetime objects
                df_copy[col] = df_copy[col].apply(lambda x: 
                    x.isoformat() if isinstance(x, (datetime, date)) 
                    else str(x) if x is not None and not (isinstance(x, float) and np.isnan(x))
                    else None
                )
            elif df_copy[col].dtype in ['float64', 'float32']:
                # Handle NaN and infinity
                df_copy[col] = df_copy[col].apply(lambda x: 
                    None if np.isnan(x) or np.isinf(x) 
                    else float(x)
                )
            elif df_copy[col].dtype in ['int64', 'int32', 'int16', 'int8']:
                # Ensure integers are Python int, not numpy int
                df_copy[col] = df_copy[col].apply(lambda x: 
                    int(x) if not (isinstance(x, float) and np.isnan(x))
                    else None
                )
        
        # Convert column names to strings (in case they're not)
        df_copy.columns = [str(col) for col in df_copy.columns]
        
        return df_copy
