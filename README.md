# HTML to Bricks Builder JSON Converter

A professional Streamlit web application that converts HTML or any content to Bricks Builder JSON format using the Cerebras AI API.

**Author:** [Ashraf Ali](https://ashrafali.net)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Cerebras](https://img.shields.io/badge/Cerebras-AI-blue?style=for-the-badge)

## Features

- 🏗️ **Three-pane interface**: Input content, JSON template, and converted output
- 🔄 **Real-time streaming**: See the conversion happen live using Streamlit's native streaming
- 📋 **Copy to clipboard**: Quick copy functionality for each panel
- 🗑️ **Clear panels**: Easy content management with clear buttons
- ⚙️ **Advanced configuration**: Multiple models, temperature, top-p, and token limits
- 🧹 **Smart output cleaning**: Automatically removes markdown blocks and thinking tags
- 💾 **Session persistence**: API key and content are remembered during the session
- 🔐 **Secure API key management**: Support for environment variables
- 🎨 **Syntax highlighting**: Professional code editors with HTML/JSON highlighting
- 📁 **Request/Response logging**: All conversions logged to timestamped files in `_history/` folder

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd cerebras-bricks-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your Cerebras API key (choose one method):
   - Set environment variable: `export CEREBRAS_API_KEY="your-api-key-here"`
   - Or enter it directly in the app's sidebar

## Usage

1. Start the Streamlit app:
```bash
streamlit run bricks_converter.py
```

2. Open your browser to the displayed URL (usually `http://localhost:8501`)

3. **Configure**: Enter your Cerebras API key in the sidebar

4. **Input**: Paste your HTML, CSS, or content in the left panel

5. **Template**: Modify the JSON template in the middle panel (default template provided)

6. **Convert**: Click "Convert to Bricks JSON" to generate the output

7. **Copy**: Use the copy buttons to transfer content between panels

## Configuration Options

- **Model**: Choose from multiple models:
  - `qwen-3-235b-a22b` - **Default** - High-performance Qwen model with 40K token support
  - `llama-3.3-70b` - Latest Llama model
  - `llama3.1-8b` - Smaller, faster model
  - `llama-4-scout-17b-16e-instruct` - Latest experimental model
  - `qwen-3-32b` - Medium-sized Qwen model
- **Temperature**: Control randomness (0.0-1.0, default 0.6)
- **Top P**: Nucleus sampling parameter (0.0-1.0, default 0.95)
- **Max Completion Tokens**: Set maximum response length (100-40,000, default 8,000)

## Example Usage

### Input Content (HTML):
```html
<div class="hero-section">
  <h1>Welcome to Our Site</h1>
  <p>This is a hero section with some content.</p>
  <button class="cta-button">Get Started</button>
</div>
```

### JSON Template:
```json
{
  "elements": [
    {
      "id": "unique-id",
      "name": "div",
      "component": "div",
      "settings": {
        "tag": "div",
        "_width": "100%",
        "_display": "block"
      },
      "elements": []
    }
  ]
}
```

### Converted Output:
The AI will generate a proper Bricks Builder JSON structure based on your input and template.

## Dependencies

- `streamlit>=1.28.0` - Web application framework
- `cerebras_cloud_sdk>=1.0.0` - Cerebras AI API client
- `pyperclip>=1.8.2` - Clipboard functionality

## Environment Variables

- `CEREBRAS_API_KEY` - Your Cerebras API key (required)

## Tips

- Use lower temperature values (0.1-0.3) for more consistent results
- Break complex HTML into smaller chunks for better conversion
- Modify the JSON template to match your specific Bricks Builder needs
- The streaming feature shows real-time conversion progress
- All conversions are automatically logged to the `_history/` folder with timestamps

## Request/Response Logging

Every conversion request and response is automatically saved to JSON files in the `_history/` folder with detailed timestamps. Each log file contains:

- **Request data**: Input content, JSON template, model parameters
- **Response data**: Raw AI output, cleaned JSON, success status, error details (if any)
- **Timestamps**: Precise timing for debugging and analysis
- **Model info**: Which model and parameters were used

This helps with:
- **Debugging**: Review what was sent and received
- **Analysis**: Track conversion patterns and success rates  
- **Backup**: Never lose your conversion results
- **Auditing**: Complete history of all API usage

## Troubleshooting

1. **API Key Issues**: Ensure your Cerebras API key is valid and has sufficient credits
2. **Clipboard Not Working**: Some browsers may block clipboard access; try copying manually
3. **Conversion Errors**: Check that your input content and template are properly formatted
4. **Slow Performance**: Try using the smaller `llama3.1-8b` model or reduce max tokens

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Author

**Ashraf Ali**
- Website: [ashrafali.net](https://ashrafali.net)
- Created this tool to simplify HTML to Bricks Builder JSON conversion

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [Cerebras](https://cerebras.ai/) for providing powerful AI models
- [Bricks Builder](https://bricksbuilder.io/) for the inspiration

## License

This project is open source and available under the MIT License.

---

⭐ **If this tool helps you, please give it a star!** ⭐