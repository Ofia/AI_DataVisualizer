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

Transform your data into beautiful, AI-generated visualizations using free open-source models!

## Features

- 📊 **Multi-Format Support**: Upload PDFs, Excel files, CSV files, or screenshots
- 🤖 **Free AI Analysis**: Uses Hugging Face's free inference API (Mistral-7B)
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
   - AI analyzes your data (takes 30-40 seconds)
   - View beautiful interactive charts!

4. **Switch templates** (optional)
   - Click any template to regenerate with different styling

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: Hugging Face Inference API (Mistral-7B-Instruct)
- **Data Processing**: pandas, pdfplumber, openpyxl
- **Visualization**: Plotly (interactive charts)
- **Frontend**: HTML5, CSS3, JavaScript

## Setup for Local Development

1. Clone this space
2. Install dependencies: `pip install -r requirements.txt`
3. Get a free Hugging Face API token from https://huggingface.co/settings/tokens
4. Create `.env` file with: `HUGGINGFACE_API_KEY=your_token_here`
5. Run: `python app.py`
6. Open: http://localhost:5000

## Notes

- First analysis may take longer as the model loads (20-30 seconds)
- Uses free Hugging Face Inference API - no cost!
- For faster results, you can upgrade to a paid API tier

## License

MIT License - feel free to use and modify!
