from flask import Flask, render_template, request, jsonify, send_file, session
import os
import sys
import traceback
from werkzeug.utils import secure_filename
from config import config
from ai_providers.provider_factory import ProviderFactory
from data_extractors.extractor_factory import ExtractorFactory
from visualization.template_manager import TemplateManager
import json
import secrets

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE

# Session configuration for BYOK (Bring Your Own Key) feature
# Generate or load a persistent SECRET_KEY
SECRET_KEY_FILE = '.flask_secret_key'
if os.environ.get('FLASK_SECRET_KEY'):
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
elif os.path.exists(SECRET_KEY_FILE):
    with open(SECRET_KEY_FILE, 'r') as f:
        app.config['SECRET_KEY'] = f.read().strip()
else:
    # Generate new key and save it
    new_key = secrets.token_hex(32)
    with open(SECRET_KEY_FILE, 'w') as f:
        f.write(new_key)
    app.config['SECRET_KEY'] = new_key
# Use default Flask sessions (secure signed cookies)
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent XSS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
# Don't require HTTPS for cookies (HF Spaces handles SSL at proxy level)
app.config['SESSION_COOKIE_SECURE'] = False

# Create necessary directories
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs('temp', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract data from file
            extractor = ExtractorFactory.get_extractor(filepath)
            data = extractor.extract()
            
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'data_preview': data.get('preview', 'Data extracted successfully')
            })
        else:
            return jsonify({'error': 'File type not allowed'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_data():
    try:
        data = request.json
        filepath = data.get('filepath')
        # Use session-stored provider if available, otherwise use default
        provider_name = session.get('selected_provider', data.get('provider', config.DEFAULT_AI_PROVIDER))
        template_name = data.get('template', config.DEFAULT_TEMPLATE)

        # Debug logging
        print(f"DEBUG: provider_name = {provider_name}")
        print(f"DEBUG: session keys = {list(session.keys())}")
        print(f"DEBUG: has anthropic_api_key = {'anthropic_api_key' in session}")

        # Extract data
        extractor = ExtractorFactory.get_extractor(filepath)
        extracted_data = extractor.extract()

        # Get AI provider (with session API key if available)
        api_key = session.get('anthropic_api_key') if provider_name == 'anthropic' else None
        print(f"DEBUG: api_key present = {api_key is not None}")
        sys.stdout.flush()
        provider = ProviderFactory.get_provider(provider_name, api_key=api_key)
        
        # Analyze data with AI
        analysis = provider.analyze_data(extracted_data, template_name)
        
        # Generate visualizations
        template_manager = TemplateManager(template_name)
        visualizations = template_manager.generate_visualizations(
            extracted_data, 
            analysis
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'visualizations': visualizations
        })
        
    except Exception as e:
        print(f"ERROR in /analyze: {str(e)}")
        traceback.print_exc()
        sys.stdout.flush()
        return jsonify({'error': str(e)}), 500

@app.route('/regenerate', methods=['POST'])
def regenerate_visualization():
    try:
        data = request.json
        filepath = data.get('filepath')
        template_name = data.get('template')
        previous_analysis = data.get('analysis')
        
        # Extract data
        extractor = ExtractorFactory.get_extractor(filepath)
        extracted_data = extractor.extract()
        
        # Generate visualizations with new template
        template_manager = TemplateManager(template_name)
        visualizations = template_manager.generate_visualizations(
            extracted_data, 
            previous_analysis
        )
        
        return jsonify({
            'success': True,
            'visualizations': visualizations
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.json
        # TODO: Implement PDF export
        return jsonify({'success': True, 'message': 'PDF export coming soon'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/set-api-key', methods=['POST'])
def set_api_key():
    """Store user's Anthropic API key in session for BYOK feature"""
    try:
        data = request.json
        api_key = data.get('api_key', '').strip()

        # Validate API key format
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400

        if not api_key.startswith('sk-ant-'):
            return jsonify({'error': 'Invalid API key format. Anthropic keys start with "sk-ant-"'}), 400

        # Test the API key by making a simple request
        from ai_providers.anthropic_provider import AnthropicProvider
        try:
            test_provider = AnthropicProvider(api_key=api_key)
            # Quick validation - just initialize, actual test happens on first use
            session['anthropic_api_key'] = api_key
            session['selected_provider'] = 'anthropic'

            return jsonify({
                'success': True,
                'message': 'API key saved successfully',
                'provider': 'anthropic'
            })
        except Exception as e:
            return jsonify({'error': f'API key validation failed: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get-current-provider', methods=['GET'])
def get_current_provider():
    """Get the currently selected AI provider"""
    try:
        # Check if user has a session-stored provider
        selected_provider = session.get('selected_provider', config.DEFAULT_AI_PROVIDER)
        has_api_key = 'anthropic_api_key' in session

        return jsonify({
            'success': True,
            'provider': selected_provider,
            'has_api_key': has_api_key,
            'default_provider': config.DEFAULT_AI_PROVIDER
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/select-provider', methods=['POST'])
def select_provider():
    """Switch between Qwen (free) and Claude (BYOK)"""
    try:
        data = request.json
        provider = data.get('provider', '').lower()

        if provider not in ['huggingface', 'anthropic']:
            return jsonify({'error': 'Invalid provider'}), 400

        # If selecting Anthropic, check if API key exists
        if provider == 'anthropic' and 'anthropic_api_key' not in session:
            return jsonify({
                'success': False,
                'needs_api_key': True,
                'message': 'Please provide your Anthropic API key'
            })

        session['selected_provider'] = provider

        return jsonify({
            'success': True,
            'provider': provider,
            'message': f'Switched to {provider}'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For production deployment (Hugging Face, etc.)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
