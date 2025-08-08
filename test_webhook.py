#!/usr/bin/env python3
"""
Test script for webhook endpoint
"""

import requests
import json

def test_webhook_with_form_data():
    """Test webhook with form data (like Twilio sends)"""
    print("Testing webhook with form data...")
    
    # Simulate Twilio form data
    form_data = {
        'Body': 'LIST /ProjectX',
        'From': 'whatsapp:+1234567890',
        'To': 'whatsapp:+14155238886',
        'MessageSid': 'test_message_sid'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/webhook',
            data=form_data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_webhook_with_json():
    """Test webhook with JSON data"""
    print("\nTesting webhook with JSON data...")
    
    # Simulate JSON data
    json_data = {
        'Body': 'HELP',
        'From': 'whatsapp:+1234567890',
        'To': 'whatsapp:+14155238886',
        'MessageSid': 'test_message_sid'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/webhook',
            json=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_api_execute():
    """Test the API execute endpoint"""
    print("\nTesting API execute endpoint...")
    
    json_data = {
        'message': 'LIST /ProjectX'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/api/execute',
            json=json_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.status_code == 200
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main test function"""
    print("Webhook Test Script")
    print("=" * 30)
    
    # Test form data (Twilio style)
    form_success = test_webhook_with_form_data()
    
    # Test JSON data
    json_success = test_webhook_with_json()
    
    # Test API execute
    api_success = test_api_execute()
    
    print("\n" + "=" * 30)
    print("Test Results:")
    print(f"Form Data Test: {'✅ PASS' if form_success else '❌ FAIL'}")
    print(f"JSON Data Test: {'✅ PASS' if json_success else '❌ FAIL'}")
    print(f"API Execute Test: {'✅ PASS' if api_success else '❌ FAIL'}")
    
    if form_success and json_success and api_success:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Check the server logs for details.")

if __name__ == "__main__":
    main()


