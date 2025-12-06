# AI Data Visualizer

Transform your data into beautiful, AI-generated visualizations using advanced language models.

## Features

- 📊 **Multi-Format Support**: Upload PDFs, Excel files, or screenshots
- 🤖 **AI-Powered Analysis**: Leverages Claude (Anthropic) to intelligently analyze your data
- 🎨 **4 Beautiful Templates**: Choose from Professional, Vibrant, Minimal, or Dark Mode themes
- 🔄 **Live Template Switching**: Toggle between visualization styles in real-time
- 📄 **PDF Export**: Download professional, high-quality reports with data-driven charts
- 🌐 **Modern Web Interface**: Drag-and-drop file upload with smooth animations

## Supported AI Providers

Currently Available:
- ✅ **Anthropic Claude** (Claude 3.5 Sonnet with vision capabilities)

Coming Soon:
- ⏳ OpenAI GPT-4 Vision
- ⏳ Google Gemini Pro
- ⏳ Local Llama Models

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd C:\Users\ofir\Desktop\Projects\VisualizeData
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Keys**
   - API keys are already configured in `.env` file
   - To use additional providers later, add their keys to `.env`

## Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open your browser**
   Navigate to: `http://localhost:5000`

3. **Upload your data**
   - Drag and drop a file, or click to browse
   - Supported formats: PDF, Excel (.xlsx, .xls), Images (.png, .jpg)

4. **Choose a visualization style**
   - Professional: Clean, business-oriented
   - Vibrant: Bold colors and modern gradients
   - Minimal: Simplified, elegant design
   - Dark: Dark background with high contrast

5. **Generate visualizations**
   - Click "Generate Visualizations"
   - AI will analyze your data and create beautiful charts
   - View insights, charts, and descriptions

6. **Switch templates** (optional)
   - Click any template to regenerate with a different style

## Project Structure

```
VisualizeData/
├── app.py                      # Main Flask application
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys)
├── ai_providers/               # AI integration modules
│   ├── base_provider.py
│   ├── anthropic_provider.py
│   └── provider_factory.py
├── data_extractors/            # File processing modules
│   ├── pdf_extractor.py
│   ├── excel_extractor.py
│   ├── image_extractor.py
│   └── extractor_factory.py
├── visualization/              # Visualization engine
│   ├── templates.py
│   ├── chart_generator.py
│   └── template_manager.py
├── static/                     # Frontend assets
│   ├── css/styles.css
│   └── js/app.js
└── templates/                  # HTML templates
    └── index.html
```

## Technology Stack

- **Backend**: Flask (Python web framework)
- **AI Integration**: Anthropic Claude API
- **Data Processing**: pandas, pdfplumber, pytesseract, openpyxl
- **Visualization**: Plotly (interactive charts)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)

## Features in Detail

### Burger Menu
- Access LLM API provider selection
- Shows current provider status
- Future providers displayed as "Coming Soon"

### Data Extraction
- **PDF**: Extracts tables and text automatically
- **Excel**: Reads all sheets and columns
- **Images**: Uses AI vision to analyze screenshots and tables

### AI Analysis
- Identifies data patterns and insights
- Recommends optimal chart types
- Generates descriptive text for each visualization
- Adapts to different data structures

### Visualization Templates
Each template includes:
- Custom color schemes
- Font styling
- Chart aesthetics
- Background and grid colors

### PDF Export (New)
- **Data-Driven Generation**: Builds PDFs programmatically for perfect layout.
- **High-Quality Charts**: Renders Plotly charts as crisp images.
- **Smart Layout**: Automatically handles page breaks and margins.

### Direct Plotly JSON (New)
- **Advanced Charts**: Supports complex visualizations (Bubble, Sunburst, etc.).
- **Creative Freedom**: AI generates full Plotly specifications directly.

## Troubleshooting

### OCR Issues
If tesseract is not installed, image OCR will be skipped. The AI vision will still work.
To install tesseract:
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Add to PATH

### API Errors
- Verify your Anthropic API key in `.env`
- Check your internet connection
- Ensure you have API credits

## Future Enhancements

- [x] PDF export functionality
- [ ] OpenAI GPT-4 Vision integration
- [ ] Google Gemini integration
- [ ] Local Llama model support
- [ ] More visualization templates
- [ ] Data editing capabilities
- [ ] Multi-file comparison
- [ ] Custom color schemes

## License

This project is for personal use.

## Support

For issues or questions, please create an issue in the repository.
