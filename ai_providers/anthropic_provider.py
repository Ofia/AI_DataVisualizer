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
                max_tokens=8192,  # Increased for full Plotly JSON
                messages=messages
            )
            
            # Parse the response
            analysis_text = response.content[0].text
            
            analysis = self._parse_analysis(analysis_text)
            
            return analysis
            
        except Exception as e:
            print(f"DEBUG: Anthropic API Error: {str(e)}")
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
        prompt = f"""You are a creative data visualization expert specializing in Plotly. Your task is to analyze data and generate FULL Plotly figure specifications (data and layout) for visually stunning charts.

Data Summary:
- Type: {data_summary['type']}
- Rows: {data_summary['row_count']}
- Columns: {data_summary['column_count']}
- Column names: {', '.join(data_summary['columns'])}

Sample Data (first few rows):
{self._safe_json_dumps(data_summary['sample_data'])}

YOUR MISSION:
1. Analyze the data to find the most interesting insights.
2. Generate 3 diverse and creative visualizations using Plotly. (Limit to 3 to ensure JSON fits in response)
3. For each chart, provide the FULL 'data' (traces) and 'layout' objects exactly as required by the Plotly.js library.
4. You MUST perform any necessary data aggregation or transformation yourself.
5. IMPORTANT: To save space, do not include thousands of data points. Aggregate data (e.g., monthly totals instead of daily) or use top 20 items.

CHART TYPES TO CONSIDER:
- 📊 Comparison: Bar (grouped/stacked), Waterfall, Funnel
- 📈 Trend: Line, Area, Scatter
- 🥧 Part-to-Whole: Pie, Donut, Sunburst, Treemap
- 🎯 Distribution: Histogram, Box, Violin
- 🫧 Multi-variable: Bubble chart (scatter with size/color)
- 🌡️ Correlation: Heatmap, Scatter Matrix

IMPORTANT GUIDELINES:
- **Creativity**: Don't just stick to bar charts. Use Bubble charts for 3 variables, Sunbursts for hierarchy, etc.
- **Data Transformation**: If the raw data needs processing (e.g., summing values by category), YOU must do it and put the calculated values in the chart data.
- **Styling**: Make them look professional and modern. Use a nice color palette.
- **Interactivity**: Enable tooltips and hover effects.

RESPONSE FORMAT (JSON ONLY):
{{
    "insights": [
        "Key insight 1",
        "Key insight 2",
        "Key insight 3"
    ],
    "charts": [
        {{
            "title": "Chart Title",
            "description": "Description of what this chart shows",
            "chart_type": "bar|line|pie|bubble|etc",
            "figure": {{
                "data": [
                    {{
                        "type": "bar",
                        "x": ["A", "B", "C"],
                        "y": [10, 20, 30],
                        "marker": {{ "color": "..." }}
                        // ... full plotly trace definition
                    }}
                ],
                "layout": {{
                    "title": "Chart Title",
                    "xaxis": {{ "title": "X Axis" }},
                    "yaxis": {{ "title": "Y Axis" }},
                    "showlegend": true
                    // ... full plotly layout definition
                }}
            }}
        }}
    ],
    "summary": "Overall summary..."
}}

Return ONLY the valid JSON. No markdown formatting, no explanations outside the JSON."""
        
        return prompt
    
    def _safe_json_dumps(self, data):
        """Safely convert data to JSON string, handling any remaining issues"""
        try:
            import json
            return json.dumps(data, indent=2, default=str)
        except Exception:
            return str(data)
    
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
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON Decode Error: {str(e)}")
            print(f"DEBUG: Failed text: {analysis_text[:200]}...")
            # Fallback if JSON parsing fails
            return {
                "insights": ["Data analysis completed"],
                "charts": [], # Return empty charts on failure
                "key_metrics": {},
                "summary": "Error parsing AI response. Please try again."
            }
    
    def is_available(self):
        """Check if Anthropic is properly configured"""
        return config.ANTHROPIC_API_KEY is not None and config.ANTHROPIC_API_KEY != ""
