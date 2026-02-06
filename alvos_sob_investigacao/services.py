"""
Services for Firebase data integration in the SACIP system.
Provides helper functions to process and format Firebase data for the frontend.
"""

from .firebase_utils import get_firebase_data, get_firebase_record, search_firebase_data
from typing import Dict, Any, List, Optional


class FirebaseDataService:
    """Service class to handle processing of Firebase data for frontend consumption."""
    
    @staticmethod
    def get_formatted_firebase_data(path: str) -> Dict[str, Any]:
        """
        Gets Firebase data and formats it appropriately for frontend consumption.
        
        Args:
            path: Path in the Firebase database to retrieve data from
            
        Returns:
            Formatted data ready for frontend consumption
        """
        raw_data = get_firebase_data(path)
        
        # Format the data for frontend consumption
        formatted_data = {
            'raw_data': raw_data,
            'count': len(raw_data) if isinstance(raw_data, dict) else 0,
            'path': path,
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'formatted_items': FirebaseDataService._format_items(raw_data)
        }
        
        return formatted_data
    
    @staticmethod
    def _format_items(data: Any) -> List[Dict[str, Any]]:
        """
        Helper method to format Firebase data items for frontend display.
        
        Args:
            data: Raw Firebase data
            
        Returns:
            Formatted list of items
        """
        if not isinstance(data, dict):
            return []
        
        items = []
        for key, value in data.items():
            item = {
                'id': key,
                'data': value,
                'preview': FirebaseDataService._get_preview(value)
            }
            items.append(item)
        
        return items
    
    @staticmethod
    def _get_preview(data: Any) -> str:
        """
        Creates a preview string from Firebase data for frontend display.
        
        Args:
            data: Single Firebase data item
            
        Returns:
            Preview string
        """
        if isinstance(data, dict):
            # Look for common fields that might contain descriptive information
            for field in ['name', 'title', 'description', 'full_name', 'nome', 'titulo']:
                if field in data:
                    preview = str(data[field])
                    return preview[:100] + "..." if len(preview) > 100 else preview
            
            # If no common fields, return a string representation
            return str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
        
        return str(data)[:100] + "..." if len(str(data)) > 100 else str(data)
    
    @staticmethod
    def search_and_format(path: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Searches Firebase data with given parameters and formats the result.
        
        Args:
            path: Path in the Firebase database to search in
            query_params: Query parameters for the search
            
        Returns:
            Formatted search results
        """
        raw_data = search_firebase_data(path, query_params)
        
        formatted_data = {
            'raw_data': raw_data,
            'query_params': query_params,
            'path': path,
            'timestamp': __import__('datetime').datetime.now().isoformat(),
            'formatted_items': FirebaseDataService._format_items(raw_data)
        }
        
        return formatted_data


# Convenience functions
def get_firebase_data_for_frontend(path: str) -> Dict[str, Any]:
    """
    Convenience function to get and format Firebase data for frontend consumption.
    
    Args:
        path: Path in the Firebase database to retrieve data from
        
    Returns:
        Formatted data ready for frontend consumption
    """
    return FirebaseDataService.get_formatted_firebase_data(path)


def search_firebase_data_for_frontend(path: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to search and format Firebase data for frontend consumption.
    
    Args:
        path: Path in the Firebase database to search in
        query_params: Query parameters for the search
        
    Returns:
        Formatted search results
    """
    return FirebaseDataService.search_and_format(path, query_params)