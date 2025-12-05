import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    
    # Default AI Provider
    DEFAULT_AI_PROVIDER = os.getenv('DEFAULT_AI_PROVIDER', 'anthropic')
    
    # File Upload Settings
    UPLOAD_FOLDER = 'uploads'
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'pdf', 'xlsx', 'xls', 'png', 'jpg', 'jpeg'}
    
    # Visualization Settings
    AVAILABLE_TEMPLATES = ['professional', 'vibrant', 'minimal', 'dark']
    DEFAULT_TEMPLATE = 'professional'
    
    # AI Providers Status
    AI_PROVIDERS = {
        'anthropic': {'name': 'Anthropic Claude', 'enabled': True},
        'openai': {'name': 'OpenAI GPT-4', 'enabled': False},
        'gemini': {'name': 'Google Gemini', 'enabled': False},
        'llama': {'name': 'Local Llama', 'enabled': False}
    }

config = Config()
