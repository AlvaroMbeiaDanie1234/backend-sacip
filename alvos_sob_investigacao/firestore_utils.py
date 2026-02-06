"""
Firestore utilities for the SACIP system.
This module handles connections to Firebase Firestore Database and data retrieval.
"""

import os
from typing import Dict, List, Any, Optional
from google.cloud import firestore
from google.oauth2 import service_account
from .firebase_config import FirebaseConfig


class FirestoreService:
    """Service class to handle Firebase Firestore operations."""
    
    def __init__(self):
        self.project_id = FirebaseConfig.get_firestore_config()['projectId']
        self.client = self._initialize_firestore_client()
    
    def _initialize_firestore_client(self) -> firestore.Client:
        """
        Initializes the Firestore client with authentication.
        """
        # Try to get service account key from environment
        service_account_key = FirebaseConfig.get_service_account_key()
        
        if service_account_key:
            # Use service account key for authentication
            credentials = service_account.Credentials.from_service_account_info(
                service_account_key
            )
            client = firestore.Client(
                credentials=credentials,
                project=self.project_id
            )
        else:
            # Try to use default credentials (for deployed environments)
            client = firestore.Client(project=self.project_id)
        
        return client
    
    def get_collection(self, collection_name: str) -> List[Dict[str, Any]]:
        """
        Retrieves all documents from a Firestore collection.
        
        Args:
            collection_name: Name of the collection to retrieve
            
        Returns:
            List of documents from the collection
        """
        try:
            collection_ref = self.client.collection(collection_name)
            docs = collection_ref.stream()
            
            documents = []
            for doc in docs:
                doc_dict = doc.to_dict()
                # Add the document ID to the data
                doc_dict['id'] = doc.id
                documents.append(doc_dict)
            
            return documents
        except Exception as e:
            print(f"❌ Error retrieving collection '{collection_name}': {str(e)}")
            raise
    
    def get_document(self, collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a specific document from a Firestore collection.
        
        Args:
            collection_name: Name of the collection
            document_id: ID of the specific document
            
        Returns:
            Document data or None if not found
        """
        try:
            doc_ref = self.client.collection(collection_name).document(document_id)
            doc_snapshot = doc_ref.get()
            
            if doc_snapshot.exists:
                doc_data = doc_snapshot.to_dict()
                # Add the document ID to the data
                doc_data['id'] = document_id
                return doc_data
            else:
                return None
        except Exception as e:
            print(f"❌ Error retrieving document '{document_id}' from collection '{collection_name}': {str(e)}")
            raise
    
    def query_collection(self, collection_name: str, filters: List[tuple]) -> List[Dict[str, Any]]:
        """
        Queries a Firestore collection with specific filters.
        
        Args:
            collection_name: Name of the collection to query
            filters: List of tuples containing (field, operator, value) for filtering
            
        Returns:
            List of documents matching the query
        """
        try:
            collection_ref = self.client.collection(collection_name)
            
            # Apply filters
            for field, operator, value in filters:
                collection_ref = collection_ref.where(field, operator, value)
            
            docs = collection_ref.stream()
            
            documents = []
            for doc in docs:
                doc_dict = doc.to_dict()
                # Add the document ID to the data
                doc_dict['id'] = doc.id
                documents.append(doc_dict)
            
            return documents
        except Exception as e:
            print(f"❌ Error querying collection '{collection_name}': {str(e)}")
            raise


# Global instance of FirestoreService
firestore_service = FirestoreService()


def get_firestore_collection(collection_name: str) -> List[Dict[str, Any]]:
    """
    Convenience function to get all documents from a Firestore collection.
    
    Args:
        collection_name: Name of the collection to retrieve
        
    Returns:
        List of documents from the collection
    """
    return firestore_service.get_collection(collection_name)


def get_firestore_document(collection_name: str, document_id: str) -> Optional[Dict[str, Any]]:
    """
    Convenience function to get a specific document from a Firestore collection.
    
    Args:
        collection_name: Name of the collection
        document_id: ID of the specific document
        
    Returns:
        Document data or None if not found
    """
    return firestore_service.get_document(collection_name, document_id)


def query_firestore_collection(collection_name: str, filters: List[tuple]) -> List[Dict[str, Any]]:
    """
    Convenience function to query a Firestore collection with specific filters.
    
    Args:
        collection_name: Name of the collection to query
        filters: List of tuples containing (field, operator, value) for filtering
        
    Returns:
        List of documents matching the query
    """
    return firestore_service.query_collection(collection_name, filters)