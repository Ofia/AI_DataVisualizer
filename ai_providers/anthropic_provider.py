import anthropic
from .base_provider import BaseProvider
from config import config
import json
import base64

class AnthropicProvider(BaseProvider):
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = "claude-sonnet-4-5"
    
    def analyze_data(self, extracted_data):
        """Analyze data using Claude"""
        try:
            # Prepare the data for Claude
            data_summary = self._prepare_data_summary(extracted_data)
            
            # Create the prompt
            prompt = self._create_analysis_prompt(data_summary, extracted_data)
            
            # Check if there's an image
            messages = []
            if extracted_data.get('image_path'):
                messages = self._create_vision_message(extracted_data['image_path'], prompt)
            else:
                messages = [{"role": "user", "content": prompt}]
            
            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=messages
            )
            
            # Parse the response
            analysis_text = response.content[0].text
            analysis = self._parse_analysis(analysis_text)
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    def _prepare_data_summary(self, extracted_data):
        """Prepare a summary of the extracted data"""
        summary = {
            'type': extracted_data.get('type', 'unknown'),
            'row_count': extracted_data.get('row_count', 0),
            'column_count': extracted_data.get('column_count', 0),
            'columns': extracted_data.get('columns', []),
            'sample_data': extracted_data.get('sample_data', [])
        }
        return summary
    
    def _create_analysis_prompt(self, data_summary, extracted_data):
        """Create a comprehensive prompt for data analysis"""
        prompt = f"""You are a data visualization expert. Analyze the following data and provide recommendations for creating beautiful, informative visualizations.

Data Summary:
- Type: {data_summary['type']}
- Rows: {data_summary['row_count']}
- Columns: {data_summary['column_count']}
- Column names: {', '.join(data_summary['columns'])}

Sample Data (first few rows):
{json.dumps(data_summary['sample_data'], indent=2)}

IMPORTANT INSTRUCTIONS:
1. You MUST use the EXACT column names listed above. Do not modify or interpret them.
2. For x_column and y_column fields, use ONLY the exact column names from the list above.
3. For multi-line or grouped charts, you can specify multiple columns separated by commas (e.g., "Sales, Expenses, Profit").
4. Verify each column name you use exists in the columns list above.

Please provide your analysis in the following JSON format:
{{
    "insights": [
        "Key insight 1",
        "Key insight 2",
        "Key insight 3"
    ],
    "chart_recommendations": [
        {{
            "type": "bar|line|pie|scatter|heatmap",
            "title": "Chart title",
            "description": "What this chart shows and why it's useful",
            "x_column": "EXACT column name from the data",
            "y_column": "EXACT column name OR comma-separated list for multi-series (e.g., 'Col1, Col2, Col3')",
            "priority": 1
        }}
    ],
    "key_metrics": {{
        "metric_name": "value or description"
    }},
    "summary": "Overall summary of the data in 2-3 sentences"
}}

Provide 3-4 different chart recommendations that would best visualize this data. Focus on clarity and visual appeal.
Return ONLY the JSON, no other text."""
        
        return prompt
    
    def _create_vision_message(self, image_path, prompt):
        """Create a message with image for vision analysis"""
        with open(image_path, 'rb') as image_file:
            image_data = base64.standard_b64encode(image_file.read()).decode('utf-8')
        
        # Determine image media type
        if image_path.lower().endswith('.png'):
            media_type = "image/png"
        elif image_path.lower().endswith(('.jpg', '.jpeg')):
            media_type = "image/jpeg"
        else:
            media_type = "image/png"
        
        return [{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": f"{prompt}\n\nAnalyze the data shown in this image and provide visualization recommendations."
                }
            ]
        }]
    
    def _parse_analysis(self, analysis_text):
        """Parse the analysis response from Claude"""
        try:
            # Try to extract JSON from the response
            # Claude might wrap it in markdown code blocks
            if "```json" in analysis_text:
                json_start = analysis_text.find("```json") + 7
                json_end = analysis_text.find("```", json_start)
                analysis_text = analysis_text[json_start:json_end].strip()
            elif "```" in analysis_text:
                json_start = analysis_text.find("```") + 3
                json_end = analysis_text.find("```", json_start)
                analysis_text = analysis_text[json_start:json_end].strip()
            
            analysis = json.loads(analysis_text)
            return analysis
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "insights": ["Data analysis completed"],
                "chart_recommendations": [
                    {
                        "type": "bar",
                        "title": "Data Overview",
                        "description": "Basic visualization of the data",
                        "priority": 1
                    }
                ],
                "key_metrics": {},
                "summary": "Data has been processed and is ready for visualization."
            }
    
    def is_available(self):
        """Check if Anthropic is properly configured"""
        return config.ANTHROPIC_API_KEY is not None and config.ANTHROPIC_API_KEY != ""
