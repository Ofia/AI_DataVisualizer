from .chart_generator import ChartGenerator
from .templates import get_template_config
import pandas as pd

class TemplateManager:
    """Manage visualization generation with different templates"""
    
    def __init__(self, template_name):
        self.template_name = template_name
        self.template_config = get_template_config(template_name)
        self.chart_generator = ChartGenerator(template_name)
    
    def generate_visualizations(self, extracted_data, analysis):
        """
        Generate visualizations based on AI analysis and template
        
        Args:
            extracted_data: Dictionary with extracted data from file
            analysis: AI analysis results with chart recommendations
            
        Returns:
            Dictionary with generated visualizations and metadata
        """
        visualizations = {
            'template': self.template_name,
            'charts': [],
            'summary': analysis.get('summary', ''),
            'insights': analysis.get('insights', []),
            'key_metrics': analysis.get('key_metrics', {})
        }
        
        # Get data
        if 'dataframe' in extracted_data:
            data = extracted_data['dataframe']
        elif 'tables' in extracted_data and len(extracted_data['tables']) > 0:
            data = extracted_data['tables'][0]
        elif 'sample_data' in extracted_data:
            data = extracted_data['sample_data']
        else:
            data = []
        
        
        # Generate charts based on AI recommendations
        recommendations = analysis.get('chart_recommendations', [])
        
        # Get dataframe for column validation
        try:
            df = pd.DataFrame(data)
            available_columns = df.columns.tolist()
        except:
            available_columns = []
        
        for rec in recommendations[:4]:  # Maximum 4 charts
            chart_type = rec.get('type', 'bar')
            title = rec.get('title', 'Data Visualization')
            description = rec.get('description', '')
            x_column = rec.get('x_column', '')
            y_column = rec.get('y_column', '')
            
            # Validate columns exist in data
            if not x_column or not y_column:
                print(f"Skipping chart '{title}': missing column specification")
                continue
            
            # Check if x_column exists
            if x_column not in available_columns:
                print(f"Skipping chart '{title}': x_column '{x_column}' not found in data. Available: {available_columns}")
                continue
            
            # Check if y_column(s) exist
            if ',' in y_column:
                # Multiple columns
                y_columns = [col.strip() for col in y_column.split(',')]
                missing_cols = [col for col in y_columns if col not in available_columns]
                if missing_cols:
                    print(f"Skipping chart '{title}': y_columns {missing_cols} not found in data. Available: {available_columns}")
                    continue
            else:
                # Single column
                if y_column not in available_columns:
                    print(f"Skipping chart '{title}': y_column '{y_column}' not found in data. Available: {available_columns}")
                    continue
            
            try:
                if chart_type == 'bar':
                    chart = self.chart_generator.create_bar_chart(
                        data,
                        x_column,
                        y_column,
                        title,
                        description
                    )
                    visualizations['charts'].append(chart)
                
                elif chart_type == 'line':
                    chart = self.chart_generator.create_line_chart(
                        data,
                        x_column,
                        y_column,
                        title,
                        description
                    )
                    visualizations['charts'].append(chart)
                
                elif chart_type == 'pie' and rec.get('x_column') and rec.get('y_column'):
                    chart = self.chart_generator.create_pie_chart(
                        data,
                        rec['x_column'],
                        rec['y_column'],
                        title,
                        description
                    )
                    visualizations['charts'].append(chart)
                
                elif chart_type == 'scatter' and rec.get('x_column') and rec.get('y_column'):
                    chart = self.chart_generator.create_scatter_chart(
                        data,
                        rec['x_column'],
                        rec['y_column'],
                        title,
                        description
                    )
                    visualizations['charts'].append(chart)
                
                elif chart_type == 'heatmap':
                    chart = self.chart_generator.create_heatmap(
                        data,
                        title,
                        description
                    )
                    visualizations['charts'].append(chart)
            
            except Exception as e:
                # Skip charts that fail to generate
                print(f"Failed to generate {chart_type} chart: {str(e)}")
                continue
        
        # If no charts were generated, create a default one
        if len(visualizations['charts']) == 0:
            visualizations['charts'].append(
                self._create_default_chart(data)
            )
        
        return visualizations
    
    def _create_default_chart(self, data):
        """Create a default visualization if AI recommendations fail"""
        try:
            df = pd.DataFrame(data)
            if len(df.columns) >= 2:
                return self.chart_generator.create_bar_chart(
                    data,
                    df.columns[0],
                    df.columns[1],
                    "Data Overview",
                    "Basic visualization of your data"
                )
            else:
                return {
                    'type': 'info',
                    'html': '<div class="info-box">Data loaded successfully. Please provide more structured data for visualizations.</div>',
                    'description': 'Data preview available'
                }
        except:
            return {
                'type': 'info',
                'html': '<div class="info-box">Data loaded successfully.</div>',
                'description': 'Data ready for analysis'
            }
