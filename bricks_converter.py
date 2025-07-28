import streamlit as st
import os
import json
from cerebras.cloud.sdk import Cerebras
import pyperclip
from typing import Generator
from streamlit_ace import st_ace
from datetime import datetime
import traceback

# Page configuration
st.set_page_config(
    page_title="HTML to Bricks Builder JSON Converter",
    page_icon="🧱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.copy-button {
    float: right;
    margin-bottom: 10px;
}
.clear-button {
    float: left;
    margin-bottom: 10px;
}
.pane-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}
/* Streaming output styling */
.streaming-output {
    font-family: 'Fira Code', 'Monaco', 'Consolas', 'Courier New', monospace !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
    background-color: #0d1117 !important;
    color: #58a6ff !important;
    padding: 16px !important;
    border-radius: 6px !important;
    border: 1px solid #21262d !important;
    white-space: pre-wrap !important;
    overflow-x: auto !important;
}
/* Custom styling for ace editor containers */
.ace-editor-container {
    border-radius: 8px !important;
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

def clear_text_area(key: str):
    """Clear a text area by setting its value to empty string"""
    st.session_state[key] = ""

def copy_to_clipboard(text: str, success_message: str = "Copied to clipboard!"):
    """Copy text to clipboard and show success message"""
    try:
        pyperclip.copy(text)
        st.success(success_message)
    except Exception as e:
        st.error(f"Failed to copy to clipboard: {str(e)}")

def ensure_history_folder():
    """Ensure _history folder exists"""
    history_dir = "_history"
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)
    return history_dir

def log_conversion_request(input_content: str, json_template: str, model: str, temperature: float, top_p: float, max_tokens: int) -> str:
    """Log conversion request to history folder and return log filename"""
    history_dir = ensure_history_folder()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # microseconds to milliseconds
    log_file = os.path.join(history_dir, f"request_{timestamp}.json")
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "type": "request",
        "model": model,
        "parameters": {
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens
        },
        "input_content": input_content,
        "json_template": json_template
    }
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Failed to log request: {str(e)}")
    
    return log_file

def log_conversion_response(log_file: str, raw_response: str, cleaned_response: str, success: bool = True, error: str = None):
    """Log conversion response to the same file as request"""
    try:
        # Read existing log data
        with open(log_file, 'r', encoding='utf-8') as f:
            log_data = json.load(f)
        
        # Add response data
        log_data["response"] = {
            "timestamp": datetime.now().isoformat(),
            "success": success,
            "raw_response": raw_response,
            "cleaned_response": cleaned_response,
            "error": error
        }
        
        # Write back to file
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2, ensure_ascii=False)
            
    except Exception as e:
        st.error(f"Failed to log response: {str(e)}")

def clean_output(text: str) -> str:
    """Clean the output by removing markdown code blocks and thinking tags"""
    import re
    
    # Remove thinking tags and their content
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)
    
    # Remove markdown code block markers
    text = text.strip()
    
    # Remove ```json at the start
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    
    # Remove ``` at the end
    if text.endswith('```'):
        text = text[:-3]
    
    # Clean up extra whitespace but preserve JSON formatting
    text = text.strip()
    
    return text

def get_api_key() -> str:
    """Get API key from session state or environment variable"""
    if 'api_key' in st.session_state and st.session_state.api_key:
        return st.session_state.api_key
    return os.environ.get("CEREBRAS_API_KEY", "")

def initialize_cerebras_client():
    """Initialize Cerebras client with API key"""
    api_key = get_api_key()
    if not api_key:
        return None
    try:
        return Cerebras(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to initialize Cerebras client: {str(e)}")
        return None

def stream_conversion(client: Cerebras, input_content: str, json_template: str, model: str = "llama-3.3-70b", max_tokens: int = 8000, temperature: float = 0.6, top_p: float = 0.95) -> Generator[str, None, None]:
    """Stream the conversion process using Cerebras API"""
    
    user_prompt = f"""Please convert the following input content to Bricks Builder JSON format using the provided template as a reference.

INPUT CONTENT:
{input_content}

JSON TEMPLATE (use this structure as a guide):
{json_template}

INSTRUCTIONS:
1. Maintain the Bricks Builder JSON structure shown in the template
2. Convert HTML elements to appropriate Bricks Builder components
3. Preserve styling and layout as much as possible
4. Ensure the output is valid JSON
5. Return ONLY the JSON, no additional text or explanations
6. Do not wrap the JSON in markdown code blocks (no ```json or ```)

CONVERTED JSON:"""

    try:
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in Bricks Builder and perfect JSON."
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=model,
            stream=True,
            max_completion_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
                
    except Exception as e:
        yield f"Error during conversion: {str(e)}"

def main():
    st.title("🧱 HTML to Bricks Builder JSON Converter")
    st.markdown("Convert HTML or any content to Bricks Builder JSON format using Cerebras AI")
    
    # Sidebar for API key management
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key_input = st.text_input(
            "Cerebras API Key",
            value=get_api_key(),
            type="password",
            help="Enter your Cerebras API key or set CEREBRAS_API_KEY environment variable"
        )
        
        if api_key_input:
            st.session_state.api_key = api_key_input
        
        # Show API key status
        if get_api_key():
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ No API Key found")
            st.info("Set CEREBRAS_API_KEY environment variable or enter it above")
        
        st.markdown("---")
        
        # Model selection with session state persistence
        models = ["qwen-3-235b-a22b", "llama-3.3-70b", "llama3.1-8b", "llama-4-scout-17b-16e-instruct", "qwen-3-32b"]
        
        # Get the default index - either from session state or use first model (qwen-3-235b-a22b)
        if 'selected_model' in st.session_state:
            try:
                default_index = models.index(st.session_state.selected_model)
            except ValueError:
                default_index = 0  # fallback to first model
        else:
            default_index = 0  # qwen-3-235b-a22b is first
        
        model_choice = st.selectbox(
            "Model",
            models,
            index=default_index,
            help="Choose the Cerebras model for conversion"
        )
        
        # Store selected model in session state
        st.session_state.selected_model = model_choice
        
        # Temperature setting
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
            help="Lower values for more consistent output"
        )
        
        # Top P setting
        top_p = st.slider(
            "Top P",
            min_value=0.0,
            max_value=1.0,
            value=0.95,
            step=0.05,
            help="Nucleus sampling parameter"
        )
        
        # Max completion tokens
        max_tokens = st.number_input(
            "Max Completion Tokens",
            min_value=100,
            max_value=40000,
            value=8000,
            step=500,
            help="Maximum tokens in the response"
        )
    
    # Main three-column layout
    col1, col2, col3 = st.columns(3)
    
    # Left column - Input Content
    with col1:
        st.subheader("📝 Input Content")
        
        # Control buttons
        col_clear1, col_copy1 = st.columns([1, 1])
        with col_clear1:
            if st.button("🗑️ Clear", key="clear_input"):
                st.session_state.input_content = ""
        with col_copy1:
            if st.button("📋 Copy", key="copy_input"):
                if 'input_content' in st.session_state:
                    copy_to_clipboard(st.session_state.input_content, "Input copied!")
        
        # Input code editor
        input_content = st_ace(
            value=st.session_state.get("input_content", ""),
            language='html',
            theme='monokai',
            key="input_content",
            height=400,
            auto_update=True,
            font_size=14,
            tab_size=2,
            wrap=True,
            annotations=None,
            placeholder="Paste your HTML, CSS, or any content here..."
        )
    
    # Middle column - JSON Template
    with col2:
        st.subheader("📋 JSON Template")
        
        # Control buttons
        col_clear2, col_copy2 = st.columns([1, 1])
        with col_clear2:
            if st.button("🗑️ Clear", key="clear_template"):
                st.session_state.json_template = ""
        with col_copy2:
            if st.button("📋 Copy", key="copy_template"):
                if 'json_template' in st.session_state:
                    copy_to_clipboard(st.session_state.json_template, "Template copied!")
        
        # Template code editor with default example
        default_template = """{
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
}"""
        
        # Initialize template if not in session state
        if 'json_template' not in st.session_state:
            st.session_state.json_template = default_template
        
        json_template = st_ace(
            value=st.session_state.get("json_template", default_template),
            language='json',
            theme='monokai',
            key="json_template",
            height=400,
            auto_update=True,
            font_size=14,
            tab_size=2,
            wrap=True,
            annotations=None
        )
    
    # Right column - Converted Output
    with col3:
        st.subheader("🎯 Converted JSON")
        
        # Control buttons
        col_clear3, col_copy3 = st.columns([1, 1])
        with col_clear3:
            if st.button("🗑️ Clear", key="clear_output"):
                st.session_state.converted_output = ""
        with col_copy3:
            if st.button("📋 Copy", key="copy_output"):
                if 'converted_output' in st.session_state:
                    copy_to_clipboard(st.session_state.converted_output, "Output copied!")
        
        # Initialize output in session state if not exists
        if 'converted_output' not in st.session_state:
            st.session_state.converted_output = ""
        
        # Output code editor (editable)
        converted_output = st_ace(
            value=st.session_state.get("converted_output", ""),
            language='json',
            theme='monokai',
            key="output_display",
            height=400,
            auto_update=True,
            font_size=14,
            tab_size=2,
            wrap=True,
            annotations=None,
            placeholder="Converted JSON will appear here..."
        )
        
        # Update session state if user edits the output
        if converted_output != st.session_state.get("converted_output", ""):
            st.session_state.converted_output = converted_output
        
        # Force update the ace editor with session state value
        if st.session_state.get("converted_output", "") and converted_output != st.session_state.get("converted_output", ""):
            st.rerun()
    
    # Conversion controls
    st.markdown("---")
    col_convert, col_status = st.columns([1, 3])
    
    with col_convert:
        convert_button = st.button(
            "🚀 Convert to Bricks JSON",
            type="primary",
            disabled=not (get_api_key() and input_content and json_template)
        )
    
    with col_status:
        if not get_api_key():
            st.error("❌ Please provide a Cerebras API key")
        elif not input_content:
            st.warning("⚠️ Please enter content to convert")
        elif not json_template:
            st.warning("⚠️ Please provide a JSON template")
        else:
            st.success("✅ Ready to convert")
    
    # Handle conversion
    if convert_button and get_api_key() and input_content and json_template:
        client = initialize_cerebras_client()
        if client:
            # Log the request
            log_file = log_conversion_request(
                input_content, json_template, model_choice, 
                temperature, top_p, max_tokens
            )
            
            # Clear previous output
            st.session_state.converted_output = ""
            
            # Create placeholders for streaming
            streaming_placeholder = st.empty()
            output_placeholder = st.empty()
            
            with streaming_placeholder.container():
                st.info("🔄 Converting... (streaming response)")
                st.markdown("**🔄 Live Conversion Stream:**")
                stream_container = st.empty()
                
                try:
                    # Initialize streaming variables
                    full_response = ""
                    
                    # Create a generator that yields chunks and updates display
                    def conversion_generator():
                        nonlocal full_response
                        for chunk in stream_conversion(client, input_content, json_template, model_choice, max_tokens, temperature, top_p):
                            full_response += chunk
                            yield chunk
                    
                    # Stream the conversion
                    st.write_stream(conversion_generator())
                    
                    # Clean the output
                    cleaned_response = clean_output(full_response)
                    
                    # Log the response
                    log_conversion_response(log_file, full_response, cleaned_response, True)
                    
                    # Store cleaned result in session state
                    st.session_state.converted_output = cleaned_response
                    
                    # Show completion message
                    st.success("✅ Conversion completed! Output updated in the right panel.")
                    st.info(f"📁 Request/response logged to: {log_file}")
                    
                    # Wait a moment then clear streaming area
                    import time
                    time.sleep(2)
                    streaming_placeholder.empty()
                    
                    # Trigger rerun to update the ace editor
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"Conversion failed: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
                    st.error(error_msg)
                    
                    # Log the error
                    log_conversion_response(log_file, "", "", False, error_msg)
                    
                    streaming_placeholder.empty()
    
    # Footer with usage information
    st.markdown("---")
    with st.expander("ℹ️ How to use this tool"):
        st.markdown("""
        **Steps:**
        1. **Configure API Key**: Enter your Cerebras API key in the sidebar or set `CEREBRAS_API_KEY` environment variable
        2. **Input Content**: Paste your HTML, CSS, or any content in the left panel
        3. **JSON Template**: Provide or modify the Bricks Builder JSON template structure in the middle panel
        4. **Convert**: Click the convert button to generate the Bricks Builder JSON
        5. **Copy Results**: Use the copy buttons to easily transfer content between panels
        
        **Features:**
        - 🔄 **Real-time streaming**: See the conversion happen in real-time
        - 📋 **Copy to clipboard**: Quick copy functionality for each panel
        - 🗑️ **Clear panels**: Easy content management
        - ⚙️ **Configurable**: Adjust model settings in the sidebar
        - 💾 **Session persistence**: Your API key and content are remembered during the session
        
        **Tips:**
        - Use the default template as a starting point and modify as needed
        - Lower temperature values (0.1-0.3) give more consistent results
        - For complex conversions, consider breaking content into smaller chunks
        """)

if __name__ == "__main__":
    main()