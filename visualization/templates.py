"""
Template configurations for the 4 visualization styles
"""

TEMPLATES = {
    'professional': {
        'name': 'Professional',
        'description': 'Clean, business-oriented design',
        'colors': ['#2E4D8C', '#5B7DB1', '#8AADD6', '#B8D4F1', '#4A5568'],
        'background': '#FFFFFF',
        'text_color': '#2D3748',
        'font_family': 'Arial, sans-serif',
        'chart_style': {
            'plot_bgcolor': '#F7FAFC',
            'paper_bgcolor': '#FFFFFF',
            'gridcolor': '#E2E8F0'
        }
    },
    'vibrant': {
        'name': 'Vibrant',
        'description': 'Bold colors and modern gradients',
        'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'],
        'background': '#FFFFFF',
        'text_color': '#2C3E50',
        'font_family': 'Segoe UI, Tahoma, sans-serif',
        'chart_style': {
            'plot_bgcolor': '#FFF5F5',
            'paper_bgcolor': '#FFFFFF',
            'gridcolor': '#FFE0E0'
        }
    },
    'minimal': {
        'name': 'Minimal',
        'description': 'Simplified, elegant design',
        'colors': ['#333333', '#666666', '#999999', '#CCCCCC', '#E74C3C'],
        'background': '#FAFAFA',
        'text_color': '#333333',
        'font_family': 'Helvetica Neue, Helvetica, sans-serif',
        'chart_style': {
            'plot_bgcolor': '#FFFFFF',
            'paper_bgcolor': '#FAFAFA',
            'gridcolor': '#EEEEEE'
        }
    },
    'dark': {
        'name': 'Dark Mode',
        'description': 'Dark background with high contrast',
        'colors': ['#00D9FF', '#FF61E6', '#FFEB3B', '#4AFF88', '#FF6B9D'],
        'background': '#1A1A2E',
        'text_color': '#EAEAEA',
        'font_family': 'Roboto, Arial, sans-serif',
        'chart_style': {
            'plot_bgcolor': '#16213E',
            'paper_bgcolor': '#1A1A2E',
            'gridcolor': '#2C3E50'
        }
    }
}

def get_template_config(template_name):
    """Get configuration for a specific template"""
    return TEMPLATES.get(template_name, TEMPLATES['professional'])

def get_all_templates():
    """Get all available templates"""
    return {name: config['name'] for name, config in TEMPLATES.items()}
