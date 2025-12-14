import os
from .base_provider import BaseProvider
from visualization.templates import get_template_config
from config import config
import json
import requests

class HuggingFaceProvider(BaseProvider):
    """
    Provider for Hugging Face Inference API
    Uses free models like Llama, Mistral, etc.
    """

    def __init__(self):
        self.api_key = os.getenv('HUGGINGFACE_API_KEY', '')
        # Free model options (you can change this)
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"  # Free & fast
        # Alternative models:
        # - "meta-llama/Llama-2-7b-chat-hf" (requires approval)
        # - "HuggingFaceH4/zephyr-7b-beta" (good alternative)
        # - "mistralai/Mixtral-8x7B-Instruct-v0.1" (powerful but slower)

        self.api_url = f"https://router.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def analyze_data(self, extracted_data, template_name='professional'):
        """Analyze data using Hugging Face model"""
        try:
            # Prepare the data for analysis
            data_summary = self._prepare_data_summary(extracted_data)

            # Create the prompt
            prompt = self._create_analysis_prompt(data_summary, extracted_data, template_name)

            # Call Hugging Face API
            response = self._call_huggingface_api(prompt)

            # Parse the response
            analysis = self._parse_analysis(response)

            return analysis

        except Exception as e:
            print(f"DEBUG: Hugging Face API Error: {str(e)}")
            raise Exception(f"Hugging Face API error: {str(e)}")

    def _call_huggingface_api(self, prompt):
        """Call the Hugging Face Inference API"""
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 2000,
                "temperature": 0.7,
                "top_p": 0.95,
                "return_full_text": False
            }
        }

        # Make request
        response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)

        if response.status_code == 503:
            # Model is loading, wait and retry
            import time
            print("Model is loading, waiting 20 seconds...")
            time.sleep(20)
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=60)

        if response.status_code != 200:
            raise Exception(f"API returned status {response.status_code}: {response.text}")

        result = response.json()

        if isinstance(result, list) and len(result) > 0:
            return result[0].get('generated_text', '')

        return result.get('generated_text', str(result))

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

        prompt = f"""<s>[INST] You are a data visualization expert. Analyze the following data and generate a JSON response with insights and chart specifications.

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
Return ONLY the JSON, no other text. [/INST]"""

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
