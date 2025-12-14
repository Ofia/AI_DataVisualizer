import os
from openai import OpenAI
from .base_provider import BaseProvider
from visualization.templates import get_template_config
from config import config
import json

class HuggingFaceProvider(BaseProvider):
    """
    Provider for Hugging Face Router API (OpenAI-compatible)
    Uses the new router.huggingface.co endpoint with automatic provider selection
    """

    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY', '')

        # Initialize OpenAI client with HF Router endpoint
        self.client = OpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=self.api_key
        )

        # Use :auto to let Hugging Face automatically select the best provider
        # You can also specify a provider explicitly: "model-name:provider"
        # Available providers: together, fireworks, replicate, sambanova, cohere, etc.
        self.model = "meta-llama/Llama-3.2-3B-Instruct:auto"

    def analyze_data(self, extracted_data, template_name='professional'):
        """Analyze data using Hugging Face Router API"""
        try:
            # Prepare the data for analysis
            data_summary = self._prepare_data_summary(extracted_data)

            # Create the prompt
            user_prompt = self._create_analysis_prompt(data_summary, extracted_data, template_name)

            # Call Hugging Face API using OpenAI-compatible format
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a data visualization expert. Analyze data and generate JSON responses with insights and Plotly chart specifications."
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7,
                top_p=0.95
            )

            # Extract the response text
            analysis_text = response.choices[0].message.content

            # Parse the response
            analysis = self._parse_analysis(analysis_text)

            return analysis

        except Exception as e:
            print(f"DEBUG: Hugging Face API Error: {str(e)}")
            raise Exception(f"Hugging Face API error: {str(e)}")

    def _prepare_data_summary(self, extracted_data):
        """Prepare a summary of the extracted data"""
        summary = {
            'type': extracted_data.get('type', 'unknown'),
            'row_count': extracted_data.get('row_count', 0),
            'column_count': extracted_data.get('column_count', 0),
            'columns': extracted_data.get('columns', []),
            'sample_data': extracted_data.get('sample_data', [])[:5]  # Only first 5 rows
        }
        return summary

    def _create_analysis_prompt(self, data_summary, extracted_data, template_name):
        """Create a prompt for data analysis"""
        template_config = get_template_config(template_name)
        colors = template_config.get('colors', [])
        color_instruction = f"Use this color palette: {', '.join(colors)}" if colors else "Use a professional color palette."

        prompt = f"""Analyze the following data and generate a JSON response with insights and chart specifications.

Data Summary:
- Type: {data_summary['type']}
- Rows: {data_summary['row_count']}
- Columns: {data_summary['column_count']}
- Column names: {', '.join(data_summary['columns'])}

Sample Data (first 5 rows):
{json.dumps(data_summary['sample_data'], indent=2)}

Task:
1. Analyze the data and find 3-4 key insights
2. Suggest 3 diverse chart types (bar, line, pie, etc.)
3. For each chart, provide full Plotly specifications

IMPORTANT: Respond with ONLY valid JSON in this exact format:
{{
    "insights": [
        "Insight 1",
        "Insight 2",
        "Insight 3"
    ],
    "charts": [
        {{
            "title": "Chart Title",
            "description": "What this chart shows",
            "chart_type": "bar",
            "figure": {{
                "data": [
                    {{
                        "type": "bar",
                        "x": ["A", "B", "C"],
                        "y": [10, 20, 30],
                        "marker": {{"color": "{colors[0] if colors else '#4A90E2'}"}}
                    }}
                ],
                "layout": {{
                    "title": "Chart Title",
                    "xaxis": {{"title": "X Axis"}},
                    "yaxis": {{"title": "Y Axis"}}
                }}
            }}
        }}
    ],
    "summary": "Overall summary of the data"
}}

{color_instruction}
Return ONLY the JSON, no other text."""

        return prompt

    def _parse_analysis(self, analysis_text):
        """Parse the analysis response"""
        try:
            # Try to extract JSON from the response
            # The model might include extra text before/after JSON

            # Look for JSON object
            start = analysis_text.find('{')
            end = analysis_text.rfind('}') + 1

            if start != -1 and end > start:
                json_str = analysis_text[start:end]
                analysis = json.loads(json_str)
                return analysis

            # If no JSON found, try to parse the whole thing
            analysis = json.loads(analysis_text)
            return analysis

        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON Decode Error: {str(e)}")
            print(f"DEBUG: Failed text: {analysis_text[:500]}...")
            # Fallback response
            return {
                "insights": [
                    "Data uploaded successfully",
                    "The model had difficulty parsing the data",
                    "Please try again or use a different template"
                ],
                "charts": [],
                "summary": "The AI model is processing your request. If you see this message repeatedly, the model may need more time to load."
            }

    def is_available(self):
        """Check if Hugging Face is properly configured"""
        return self.api_key is not None and self.api_key != ""
