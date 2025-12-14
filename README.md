---
title: AI Data Visualizer
emoji: 📊
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 5000
pinned: false
license: mit
---

# AI Data Visualizer 📊

Transform your data into beautiful, AI-generated visualizations using powerful language models!

## Features

- 📊 **Multi-Format Support**: Upload PDFs, Excel files, CSV files, or screenshots
- 🤖 **AI-Powered Analysis**: Uses Qwen 2.5 72B via Hugging Face Router API
- 🎨 **4 Beautiful Templates**: Professional, Vibrant, Minimal, or Dark Mode
- 🔄 **Live Template Switching**: Toggle between visualization styles in real-time
- 📄 **PDF Export**: Download professional reports with data-driven charts
- 🌐 **Modern Web Interface**: Drag-and-drop file upload

## How to Use

1. **Upload your data file**
   - Supported: PDF, Excel (.xlsx, .xls), CSV (.csv), Images (.png, .jpg)

2. **Choose a visualization style**
   - Professional, Vibrant, Minimal, or Dark

3. **Generate visualizations**
   - Click "Generate Visualizations"
   - AI analyzes your data and generates 3 diverse charts
   - View beautiful interactive Plotly charts!

4. **Switch templates** (optional)
   - Click any template to regenerate with different styling

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: Hugging Face Router API (Qwen/Qwen2.5-72B-Instruct)
- **Data Processing**: pandas, pdfplumber, openpyxl, pytesseract
- **Visualization**: Plotly (interactive charts)
- **Frontend**: HTML5, CSS3, JavaScript

## Setup for Local Development

### Prerequisites
- Python 3.10+
- Tesseract OCR (for image text extraction)

### Installation

1. Clone this repository
```bash
git clone <your-repo-url>
cd VisualizeData
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Get a Hugging Face API token
   - Go to https://huggingface.co/settings/tokens
   - Create a fine-grained token with "Make calls to Inference Providers" permission
   - **Note**: You need to add a payment method to use the Router API

4. Create `.env` file
```bash
HUGGINGFACE_API_KEY=your_token_here
DEFAULT_AI_PROVIDER=huggingface
```

5. Run the application
```bash
python app.py
```

6. Open your browser
```
http://localhost:5000
```

## Deployment

This app is deployed on Hugging Face Spaces using Docker. See `DEPLOYMENT_GUIDE.md` for details.

### Environment Variables Required:
- `HUGGINGFACE_API_KEY`: Your HF token with billing enabled
- `DEFAULT_AI_PROVIDER`: Set to `huggingface`

## Cost Notes

- Uses Hugging Face Router API which requires billing to be set up
- Cost is pay-per-token (very affordable for occasional use)
- Qwen 2.5 72B provides excellent quality for data analysis and JSON generation
- Free credits often provided when adding payment method

## Architecture

```
├── app.py                      # Flask application
├── config.py                   # Configuration settings
├── ai_providers/               # AI provider implementations
│   ├── huggingface_provider.py # HF Router integration
│   ├── anthropic_provider.py   # Claude integration (disabled)
│   └── provider_factory.py     # Provider selection logic
├── data_extractors/            # Data extraction from various formats
├── visualization/              # Chart generation and templates
├── static/                     # CSS, JS, assets
└── templates/                  # HTML templates
```

## License

MIT License - feel free to use and modify!

---

Built with ❤️ using Hugging Face, Flask, and Plotly
