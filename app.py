from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
from config import config
from ai_providers.provider_factory import ProviderFactory
from data_extractors.extractor_factory import ExtractorFactory
from visualization.template_manager import TemplateManager
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE

# Create necessary directories
os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs('temp', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html',
                         templates=config.AVAILABLE_TEMPLATES)

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
        provider_name = data.get('provider', config.DEFAULT_AI_PROVIDER)
        template_name = data.get('template', config.DEFAULT_TEMPLATE)
        
        # Extract data
        extractor = ExtractorFactory.get_extractor(filepath)
        extracted_data = extractor.extract()
        
        # Get AI provider
        provider = ProviderFactory.get_provider(provider_name)
        
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

if __name__ == '__main__':
    # For production deployment (Hugging Face, etc.)
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
