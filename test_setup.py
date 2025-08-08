#!/usr/bin/env python3
"""
Test script for WhatsApp Drive Assistant
"""

import os
import sys
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from python.command_parser import CommandParser
        from python.google_drive_client import GoogleDriveClient
        from python.document_summarizer import DocumentSummarizer
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_command_parser():
    """Test command parsing functionality"""
    print("🧪 Testing command parser...")
    
    try:
        from python.command_parser import CommandParser
        parser = CommandParser()
        
        # Test valid commands
        test_cases = [
            ("LIST /ProjectX", True),
            ("DELETE /ProjectX/file.pdf", True),
            ("MOVE /ProjectX/file.pdf /Archive", True),
            ("SUMMARY /ProjectX", True),
            ("HELP", True),
            ("INVALID", False),
            ("", False)
        ]
        
        for command, should_succeed in test_cases:
            result = parser.parse_message(command)
            success = result.get("success", False)
            
            if success == should_succeed:
                print(f"✅ {command}: {'PASS' if should_succeed else 'FAIL (expected)'}")
            else:
                print(f"❌ {command}: {'FAIL' if should_succeed else 'PASS (unexpected)'}")
        
        return True
    except Exception as e:
        print(f"❌ Command parser test failed: {e}")
        return False

def test_api_server():
    """Test API server endpoints"""
    print("🧪 Testing API server...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test test endpoint
        response = requests.get("http://localhost:5000/test", timeout=5)
        if response.status_code == 200:
            print("✅ Test endpoint working")
        else:
            print(f"❌ Test endpoint failed: {response.status_code}")
            return False
        
        return True
    except requests.exceptions.ConnectionError:
        print("⚠️ API server not running (start with: python python/api_server.py)")
        return False
    except Exception as e:
        print(f"❌ API server test failed: {e}")
        return False

def test_environment():
    """Test environment configuration"""
    print("🧪 Testing environment configuration...")
    
    required_vars = [
        "OPENAI_API_KEY",
        "TWILIO_ACCOUNT_SID", 
        "TWILIO_AUTH_TOKEN",
        "TWILIO_WHATSAPP_NUMBER"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment variables configured")
    return True

def test_credentials():
    """Test credential files"""
    print("🧪 Testing credentials...")
    
    # Check Google Drive credentials
    if not Path("credentials.json").exists():
        print("⚠️ credentials.json not found")
        print("   Download from Google Cloud Console and save as credentials.json")
        return False
    
    print("✅ Credentials file found")
    return True

def test_dependencies():
    """Test if all dependencies are installed"""
    print("🧪 Testing dependencies...")
    
    required_packages = [
        "google-auth",
        "google-api-python-client", 
        "twilio",
        "openai",
        "flask",
        "python-docx",
        "PyPDF2"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True

def main():
    """Run all tests"""
    print("🚀 WhatsApp Drive Assistant - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Environment", test_environment),
        ("Credentials", test_credentials),
        ("Imports", test_imports),
        ("Command Parser", test_command_parser),
        ("API Server", test_api_server)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Setup is complete.")
        print("\n📋 Next steps:")
        print("1. Start the API server: python python/api_server.py")
        print("2. Import the n8n workflow")
        print("3. Configure Twilio webhook")
        print("4. Test with WhatsApp messages")
    else:
        print("⚠️ Some tests failed. Please fix the issues above.")
        print("\n💡 Common fixes:")
        print("- Run: pip install -r requirements.txt")
        print("- Copy env.example to .env and update with your credentials")
        print("- Download Google Drive credentials as credentials.json")
        print("- Start the API server: python python/api_server.py")

if __name__ == "__main__":
    main()
