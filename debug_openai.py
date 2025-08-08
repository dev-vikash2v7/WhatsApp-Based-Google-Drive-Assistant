#!/usr/bin/env python3
"""
Diagnostic script to identify OpenAI client initialization issues
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_environment_variables():
    """Check for proxy-related environment variables"""
    print("=== Environment Variables Check ===")
    
    proxy_vars = [
        'HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy',
        'HTTP_PROXY_USER', 'HTTPS_PROXY_USER', 'HTTP_PROXY_PASS', 'HTTPS_PROXY_PASS',
        'NO_PROXY', 'no_proxy', 'ALL_PROXY', 'all_proxy'
    ]
    
    for var in proxy_vars:
        value = os.getenv(var)
        if value:
            print(f"⚠️  {var}: {value}")
        else:
            print(f"✅ {var}: Not set")
    
    print(f"\nOpenAI API Key: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")

def test_openai_initialization():
    """Test different OpenAI client initialization approaches"""
    print("\n=== OpenAI Client Initialization Tests ===")
    
    try:
        from openai import OpenAI
        
        # Test 1: Basic initialization
        print("Test 1: Basic initialization...")
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ No OpenAI API key found")
            return
        
        client = OpenAI(api_key=api_key)
        print("✅ Basic initialization successful")
        
        # Test 2: With explicit parameters
        print("Test 2: With explicit parameters...")
        client2 = OpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1"
        )
        print("✅ Explicit parameters initialization successful")
        
        # Test 3: Check client attributes
        print("Test 3: Checking client attributes...")
        print(f"Client type: {type(client)}")
        print(f"Has models attribute: {hasattr(client, 'models')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e)}")
        return False

def test_requests_library():
    """Test requests library behavior"""
    print("\n=== Requests Library Test ===")
    
    try:
        import requests
        
        # Check if requests is using any proxies
        session = requests.Session()
        print(f"Session proxies: {session.proxies}")
        
        # Test a simple request
        response = requests.get('https://httpbin.org/get', timeout=5)
        print(f"Test request status: {response.status_code}")
        print("✅ Requests library working normally")
        
    except Exception as e:
        print(f"❌ Requests error: {e}")

def main():
    """Main diagnostic function"""
    print("OpenAI Client Diagnostic Tool")
    print("=" * 40)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check environment variables
    check_environment_variables()
    
    # Test requests library
    test_requests_library()
    
    # Test OpenAI initialization
    success = test_openai_initialization()
    
    print("\n=== Recommendations ===")
    if success:
        print("✅ OpenAI client initialization is working correctly")
        print("The issue might be in the specific context where it's being called")
    else:
        print("❌ OpenAI client initialization is failing")
        print("Try the following solutions:")
        print("1. Check for proxy environment variables and clear them if not needed")
        print("2. Update the openai library: pip install --upgrade openai")
        print("3. Try using a different OpenAI client initialization approach")

if __name__ == "__main__":
    main()


