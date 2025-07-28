#!/usr/bin/env python3
"""
Test script to verify the Streamlit app can be imported and basic functions work
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import streamlit as st
        import cerebras.cloud.sdk
        import pyperclip
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_structure():
    """Test that the main app file can be imported"""
    try:
        import bricks_converter
        print("✅ App module imports successfully")
        
        # Check if main functions exist
        functions_to_check = [
            'get_api_key',
            'initialize_cerebras_client', 
            'stream_conversion',
            'main'
        ]
        
        for func_name in functions_to_check:
            if hasattr(bricks_converter, func_name):
                print(f"✅ Function '{func_name}' exists")
            else:
                print(f"❌ Function '{func_name}' missing")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import app module: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing app structure: {e}")
        return False

def test_environment():
    """Test environment setup"""
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Check if app file exists
    if os.path.exists('bricks_converter.py'):
        print("✅ App file exists")
    else:
        print("❌ App file missing")
        return False
    
    # Check if requirements file exists
    if os.path.exists('requirements.txt'):
        print("✅ Requirements file exists")
    else:
        print("❌ Requirements file missing")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Bricks Converter App")
    print("=" * 40)
    
    tests = [
        ("Environment", test_environment),
        ("Imports", test_imports),
        ("App Structure", test_app_structure)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}...")
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name} test passed")
            else:
                print(f"❌ {test_name} test failed")
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! App is ready to run.")
        print("\nTo start the app, run:")
        print("streamlit run bricks_converter.py")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)