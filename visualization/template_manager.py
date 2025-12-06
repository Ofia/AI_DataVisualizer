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
        
        # Get data (kept for reference, though AI now handles data transformation)
        if 'dataframe' in extracted_data:
            data = extracted_data['dataframe']
        elif 'tables' in extracted_data and len(extracted_data['tables']) > 0:
            data = extracted_data['tables'][0]
        elif 'sample_data' in extracted_data:
            data = extracted_data['sample_data']
        else:
            data = []
        
        # Generate charts based on AI recommendations
        # New format: 'charts' list with full Plotly specs
        recommendations = analysis.get('charts', [])
        
        # Fallback for backward compatibility with old prompt format
        if not recommendations and 'chart_recommendations' in analysis:
            print("Warning: Received old format from AI, using fallback")
            recommendations = analysis.get('chart_recommendations', [])
        
        for rec in recommendations:
            try:
                # Check if this is a full Plotly JSON spec (new format)
                if 'figure' in rec:
                    chart = self.chart_generator.create_chart_from_json(rec)
                    visualizations['charts'].append(chart)
                else:
                    # Fallback or error for unrecognized format
                    print(f"Skipping chart '{rec.get('title', 'Unknown')}': missing figure specification")
                    continue
            
            except Exception as e:
                # Skip charts that fail to generate
                print(f"Failed to generate chart: {str(e)}")
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
