#!/usr/bin/env python3
"""
Demo script to test the HTML to Bricks Builder JSON conversion functionality
"""

import os
from cerebras.cloud.sdk import Cerebras

# Set the API key
API_KEY = "csk-rd5w454692pm56vwkwykvffprvdwhkrjcjmtycn958x3k82j"

def demo_conversion():
    """Demonstrate the conversion functionality"""
    
    # Sample HTML input
    input_html = """
    <div class="hero-section" style="background: #667eea; padding: 40px; text-align: center; color: white;">
        <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Welcome to Our Site</h1>
        <p style="font-size: 1.2rem; margin-bottom: 2rem;">This is a beautiful hero section</p>
        <button style="background: #ff6b6b; color: white; padding: 12px 24px; border: none; border-radius: 6px;">
            Get Started
        </button>
    </div>
    """
    
    # Sample Bricks Builder JSON template
    json_template = """{
      "elements": [
        {
          "id": "unique-id",
          "name": "div",
          "component": "div",
          "settings": {
            "tag": "div",
            "_width": "100%",
            "_display": "block",
            "_background": "#ffffff",
            "_padding": "20px"
          },
          "elements": []
        }
      ]
    }"""
    
    print("🧱 HTML to Bricks Builder JSON Conversion Demo")
    print("=" * 50)
    
    print("\n📝 INPUT HTML:")
    print(input_html.strip())
    
    print("\n📋 JSON TEMPLATE:")
    print(json_template.strip())
    
    print("\n🔄 Converting with Cerebras API...")
    
    # Initialize Cerebras client
    client = Cerebras(api_key=API_KEY)
    
    # Create conversion prompt
    prompt = f"""You are an expert at converting HTML/content to Bricks Builder JSON format.

Please convert the following input content to Bricks Builder JSON format using the provided template as a reference.

INPUT CONTENT:
{input_html}

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
        # Test streaming conversion with new model and parameters
        print("📡 Streaming response...")
        stream = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert in Bricks Builder and perfect JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="qwen-3-235b-a22b",
            stream=True,
            max_completion_tokens=8000,
            temperature=0.6,
            top_p=0.95
        )
        
        print("\n🎯 CONVERTED OUTPUT:")
        print("-" * 30)
        
        full_response = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="", flush=True)
                full_response += content
        
        print("\n" + "-" * 30)
        
        # Clean the output using comprehensive cleaning function
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
        
        cleaned_response = clean_output(full_response)
        
        print("🧹 CLEANED JSON OUTPUT:")
        print("-" * 30)
        print(cleaned_response)
        print("-" * 30)
        print("✅ Conversion completed successfully!")
        
        # Verify JSON validity
        try:
            import json
            parsed = json.loads(cleaned_response)
            print("✅ Output is valid JSON")
            print(f"📊 Elements found: {len(parsed.get('elements', []))}")
        except json.JSONDecodeError:
            print("⚠️  Output may not be valid JSON (but conversion completed)")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def main():
    """Run the demo"""
    success = demo_conversion()
    
    if success:
        print(f"\n🎉 Demo completed successfully!")
        print("\nTo run the full Streamlit app:")
        print("export CEREBRAS_API_KEY=\"{0}\"".format(API_KEY))
        print("streamlit run bricks_converter.py")
    else:
        print("\n❌ Demo failed. Please check the error messages above.")

if __name__ == "__main__":
    main()