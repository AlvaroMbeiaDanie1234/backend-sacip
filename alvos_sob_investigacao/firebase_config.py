"""
Firebase configuration for the SACIP system.
This module handles the configuration for connecting to Firebase Realtime Database.
"""

import os
import json
from typing import Dict, Any, Optional


class FirebaseConfig:
    """Configuration class for Firebase connection parameters."""
    
    @staticmethod
    def get_firebase_config() -> Dict[str, str]:
        """
        Returns Firebase configuration dictionary.
        Uses environment variables if available, otherwise uses hardcoded values.
        """
        return {
            "apiKey": os.getenv("FIREBASE_API_KEY", "AIzaSyBwkjtSZ1yru-3IQ94e0bhBz_WyMrzKSJY"),
            "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN", "nossacomunidade-1d62d.firebaseapp.com"),
            "databaseURL": os.getenv("FIREBASE_DATABASE_URL", "https://nossacomunidade-1d62d-default-rtdb.firebaseio.com"),
            "projectId": os.getenv("FIREBASE_PROJECT_ID", "nossacomunidade-1d62d"),
            "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET", "nossacomunidade-1d62d.firebasestorage.app"),
            "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID", "462025426895"),
            "appId": os.getenv("FIREBASE_APP_ID", "1:462025426895:web:58c474485398961161b4ba"),
            "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID", "G-M0MXM0H7G4")
        }
    
    @staticmethod
    def get_firestore_config() -> Dict[str, str]:
        """
        Returns Firestore-specific configuration.
        """
        return {
            "projectId": os.getenv("FIREBASE_PROJECT_ID", "nossacomunidade-1d62d")
        }
    
    @staticmethod
    def validate_config():
        """
        Validates that the required Firebase configuration parameters are present.
        """
        config = FirebaseConfig.get_firebase_config()
        
        required_fields = [
            'apiKey',
            'projectId'
        ]
        
        for field in required_fields:
            if not config.get(field) or config[field].startswith('YOUR_'):
                raise ValueError(f"Missing required Firebase configuration: {field}")
    
    @staticmethod
    def get_service_account_key() -> Optional[Dict[str, Any]]:
        """
        Returns the Firebase service account key from environment variable.
        This is used for server-side authentication with Firestore.
        """
        service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_JSON')
        if service_account_json:
            try:
                return json.loads(service_account_json)
            except json.JSONDecodeError:
                raise ValueError("Invalid JSON in FIREBASE_SERVICE_ACCOUNT_JSON environment variable")
        return None