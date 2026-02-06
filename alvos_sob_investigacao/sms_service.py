import requests
import os
from typing import List, Dict, Any
from django.conf import settings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SMSService:
    """
    Service class for sending SMS messages using TelcoSMS API
    """
    
    def __init__(self):
        self.api_key = os.getenv('TELCO_SMS_API_KEY')
        self.base_url = os.getenv('SMS_BASE_URL_TELCO', 'https://www.telcosms.co.ao/send_message')
        
        if not self.api_key:
            raise ValueError("TELCO_SMS_API_KEY must be set in environment variables")
    
    def send_sms(self, recipients: List[str], message: str) -> Dict[str, Any]:
        """
        Send SMS to one or more recipients using TelcoSMS API
        
        Args:
            recipients: List of phone numbers (e.g., ['936494411'])
            message: The message content to send
            
        Returns:
            Dict containing the API response
        """
        if not recipients or not message:
            raise ValueError("Recipients and message cannot be empty")
        
        # Prepare the payload according to TelcoSMS API
        payload = {
            "message": {
                "api_key_app": self.api_key,
                "phone_number": recipients[0] if recipients else '',  # TelcoSMS expects single number
                "message_body": message
            }
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Log the error appropriately in production
            print(f"SMS sending failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'status_code': getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }

# Create a singleton instance
sms_service = SMSService()