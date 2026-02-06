import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def send_sms_message(phone_number, message):
    """
    Sends an SMS message using the TelcoSMS API
    """
    # SMS configuration from environment variables
    api_key = os.getenv('TELCO_SMS_API_KEY')
    base_url = os.getenv('SMS_BASE_URL_TELCO', 'https://www.telcosms.co.ao/send_message')
    
    if not api_key:
        raise ValueError("SMS configuration is missing. Please set TELCO_SMS_API_KEY in environment variables.")
    
    # Format the phone number to ensure it's in the right format for Angola
    if phone_number.startswith('+'):
        # Remove the + and country code, keep only the local number
        if phone_number.startswith('+244'):
            phone_number = phone_number[4:]  # Remove '+244'
        else:
            # If it starts with + but not +244, we assume it's already in correct format
            phone_number = phone_number[1:]
    elif phone_number.startswith('00'):
        # Remove '00' and country code
        phone_number = phone_number[5:]  # Remove '00244'
    elif phone_number.startswith('244'):
        # Remove '244' country code
        phone_number = phone_number[3:]
    
    try:
        # Prepare the request for TelcoSMS API
        payload = {
            "message": {
                "api_key_app": api_key,
                "phone_number": phone_number,
                "message_body": message
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Send the request
        response = requests.post(base_url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ SMS sent successfully to {phone_number}")
            print(f"💬 Message: {message}")
            return True, response.json()
        else:
            print(f"❌ Error sending SMS: {response.status_code} - {response.text}")
            return False, response.json()
            
    except Exception as e:
        print(f"❌ Exception occurred while sending SMS: {str(e)}")
        return False, str(e)


def send_test_sms():
    """
    Sends a test SMS to verify SMS configuration
    """
    # Get test phone number from environment or use a default
    test_phone = os.getenv('TEST_PHONE_NUMBER', '936494411')
    
    message = "Test message from SACIP - Sistema de Análise Criminal Integrado de Polícia"
    
    return send_sms_message(test_phone, message)
