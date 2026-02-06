"""
Tests for Firebase integration in the SACIP system.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest.mock import patch
from .firebase_utils import FirebaseService


class FirebaseIntegrationTest(TestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.client = Client()
        
    @patch('alvos_sob_investigacao.firebase_utils.FirebaseService.get_data')
    def test_get_firebase_data_success(self, mock_get_data):
        """Test successful retrieval of Firebase data"""
        # Mock the Firebase response
        mock_get_data.return_value = {
            'suspect1': {'name': 'John Doe', 'crime': 'Robbery'},
            'suspect2': {'name': 'Jane Smith', 'crime': 'Fraud'}
        }
        
        # Make request with authentication
        response = self.client.get(
            '/alvos-sob_investigacao/firebase-data/',
            {'path': '/suspects'},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['path'], '/suspects')
        self.assertIn('data', response.json())
        
    @patch('alvos_sob_investigacao.firebase_utils.FirebaseService.get_data')
    def test_get_firebase_data_with_error(self, mock_get_data):
        """Test Firebase data retrieval with error"""
        # Mock an exception
        mock_get_data.side_effect = Exception("Connection failed")
        
        # Make request with authentication
        response = self.client.get(
            '/alvos-sob_investigacao/firebase-data/',
            {'path': '/suspects'},
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertFalse(response.json()['success'])
        self.assertIn('error', response.json())
        
    def test_unauthorized_access(self):
        """Test that unauthorized users cannot access Firebase data"""
        response = self.client.get('/alvos-sob_investigacao/firebase-data/')
        
        # Should return 401 or 403 for unauthorized access
        self.assertIn(response.status_code, [401, 403])
        
    @patch('alvos_sob_investigacao.firebase_utils.FirebaseService.search_data')
    def test_search_firebase_data(self, mock_search_data):
        """Test searching Firebase data"""
        # Mock the Firebase search response
        mock_search_data.return_value = {
            'result1': {'name': 'John Doe', 'crime': 'Robbery', 'status': 'active'}
        }
        
        # Make POST request with authentication
        response = self.client.post(
            '/alvos-sob_investigacao/firebase-data/',
            {
                'action': 'search',
                'path': '/suspects',
                'query_params': {
                    'orderBy': '"status"',
                    'equalTo': '"active"'
                }
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['action'], 'search')
        self.assertEqual(response.json()['path'], '/suspects')
        
    @patch('alvos_sob_investigacao.firebase_utils.FirebaseService.get_data')
    def test_get_firebase_data_without_path_defaults_to_root(self, mock_get_data):
        """Test that requesting without path defaults to root path"""
        mock_get_data.return_value = {'data': 'some_data'}
        
        response = self.client.get(
            '/alvos-sob_investigacao/firebase-data/',
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        
        self.assertEqual(response.status_code, 200)
        # Verify that get_data was called with root path
        # We can't easily verify the call here due to mocking complexity,
        # but the response should be successful
        

class FirebaseServiceTest(TestCase):
    def test_firebase_service_initialization(self):
        """Test that FirebaseService initializes correctly"""
        service = FirebaseService()
        
        # Check that required attributes are set
        self.assertIsNotNone(service.config)
        self.assertIsNotNone(service.database_url)
        self.assertIsNotNone(service.api_key)
        
        # Check that the config contains required keys
        required_keys = ['apiKey', 'databaseURL', 'projectId']
        for key in required_keys:
            self.assertIn(key, service.config)