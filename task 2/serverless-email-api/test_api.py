import requests
import json

API_URL = 'http://localhost:3000/dev/send-email'

def test_valid_email():
    """Test sending valid email"""
    print("Test 1: Valid email send")
    payload = {
        'receiver_email': 'your-email@gmail.com',  # CHANGE THIS
        'subject': 'Test Email from Python Serverless',
        'body_text': 'This is a test email. If you receive this, the API works!'
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Error: {e}\n")

def test_missing_field():
    """Test missing required field"""
    print("Test 2: Missing field (should return 400)")
    payload = {
        'receiver_email': 'test@example.com',
        'subject': 'Test'
        # Missing body_text
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Error: {e}\n")

def test_invalid_email():
    """Test invalid email format"""
    print("Test 3: Invalid email format (should return 400)")
    payload = {
        'receiver_email': 'not-an-email',
        'subject': 'Test',
        'body_text': 'Test body'
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Error: {e}\n")

def test_empty_string():
    """Test empty string field"""
    print("Test 4: Empty string (should return 400)")
    payload = {
        'receiver_email': 'test@example.com',
        'subject': '',
        'body_text': 'Test'
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except Exception as e:
        print(f"Error: {e}\n")

if __name__ == '__main__':
    print("="*60)
    print("API TESTING")
    print("="*60 + "\n")
    
    test_valid_email()
    test_missing_field()
    test_invalid_email()
    test_empty_string()
    
    print("="*60)
    print("TESTS COMPLETE")
    print("="*60)