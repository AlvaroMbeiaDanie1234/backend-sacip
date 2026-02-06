"""
Firebase utilities for the SACIP system.
This module handles connections to Firebase Realtime Database and data retrieval.
"""

import os
import requests
import json
from typing import Dict, List, Any, Optional
from .firebase_config import FirebaseConfig


class FirebaseService:
    """Service class to handle Firebase Realtime Database operations."""
    
    def __init__(self):
        self.config = FirebaseConfig.get_firebase_config()
        self.database_url = self.config['databaseURL']
        self.api_key = self.config['apiKey']
        
        # Validate configuration
        FirebaseConfig.validate_config()
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Dict[Any, Any]:
        """
        Makes a request to Firebase Realtime Database.
        
        Args:
            endpoint: The database path (e.g., '/users.json')
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            data: Data to send in request body (for POST, PUT, PATCH)
        
        Returns:
            Response data from Firebase
        """
        url = f"{self.database_url.rstrip('/')}{endpoint}"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        params = {'key': self.api_key} if self.api_key else {}
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, params=params, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, params=params, headers=headers, json=data)
            elif method.upper() == 'PATCH':
                response = requests.patch(url, params=params, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, params=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json() if response.content else {}
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error making request to Firebase: {str(e)}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            raise
    
    def get_data(self, path: str) -> Dict[Any, Any]:
        """
        Retrieves data from Firebase Realtime Database at the specified path.
        
        Args:
            path: Path in the database (e.g., '/suspects', '/reports')
        
        Returns:
            Data from the specified path
        """
        if not path.endswith('.json'):
            path = f"{path}.json"
        
        return self._make_request(path, 'GET')
    
    def get_specific_record(self, path: str, record_id: str) -> Dict[Any, Any]:
        """
        Retrieves a specific record from Firebase Realtime Database.
        
        Args:
            path: Path in the database (e.g., '/suspects')
            record_id: ID of the specific record
        
        Returns:
            Specific record data
        """
        if not path.endswith('.json'):
            path = f"{path}.json"
        
        full_path = f"{path}/{record_id}"
        return self._make_request(full_path, 'GET')
    
    def get_multiple_paths(self, paths: List[str]) -> Dict[str, Any]:
        """
        Retrieves data from multiple paths in Firebase Realtime Database.
        
        Args:
            paths: List of paths in the database (e.g., ['/suspects', '/reports'])
        
        Returns:
            Dictionary mapping path names to their data
        """
        result = {}
        for path in paths:
            try:
                data = self.get_data(path)
                # Use the last part of the path as the key
                path_key = path.strip('/').split('/')[-1] or 'root'
                result[path_key] = data
            except Exception as e:
                print(f"❌ Error retrieving data from path '{path}': {str(e)}")
                result[path_key] = {}
        
        return result
    
    def search_data(self, path: str, query_params: Dict[str, Any]) -> Dict[Any, Any]:
        """
        Searches data in Firebase Realtime Database with query parameters.
        
        Args:
            path: Path in the database (e.g., '/suspects')
            query_params: Query parameters for filtering (e.g., {'orderBy': '"name"', 'equalTo': '"John"'})
        
        Returns:
            Filtered data based on query parameters
        """
        if not path.endswith('.json'):
            path = f"{path}.json"
        
        # Add query parameters to the path
        query_string = '&'.join([f"{key}={value}" for key, value in query_params.items()])
        full_path = f"{path}?{query_string}" if query_string else path
        
        return self._make_request(full_path, 'GET')


# Global instance of FirebaseService
firebase_service = FirebaseService()


def get_firebase_data(path: str) -> Dict[Any, Any]:
    """
    Convenience function to get data from Firebase.
    
    Args:
        path: Path in the Firebase database (e.g., '/suspects')
    
    Returns:
        Data from the specified path
    """
    return firebase_service.get_data(path)


def get_firebase_record(path: str, record_id: str) -> Dict[Any, Any]:
    """
    Convenience function to get a specific record from Firebase.
    
    Args:
        path: Path in the Firebase database (e.g., '/suspects')
        record_id: ID of the specific record
    
    Returns:
        Specific record data
    """
    return firebase_service.get_specific_record(path, record_id)


def search_firebase_data(path: str, query_params: Dict[str, Any]) -> Dict[Any, Any]:
    """
    Convenience function to search data in Firebase with query parameters.
    
    Args:
        path: Path in the Firebase database (e.g., '/suspects')
        query_params: Query parameters for filtering
    
    Returns:
        Filtered data based on query parameters
    """
    return firebase_service.search_data(path, query_params)


def get_multiple_firebase_paths(paths: List[str]) -> Dict[str, Any]:
    """
    Convenience function to get data from multiple Firebase paths.
    
    Args:
        paths: List of paths in the Firebase database
    
    Returns:
        Dictionary mapping path names to their data
    """
    return firebase_service.get_multiple_paths(paths)