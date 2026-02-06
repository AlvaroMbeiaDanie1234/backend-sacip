# Firebase/Firestore Integration Documentation

This document explains how to use the Firebase integration in the SACIP system, including both Realtime Database and Firestore capabilities.

## Firestore-Specific Endpoints

### GET /alvos-sob-investigacao/firestore-users/
Retrieves all users from Firestore 'users' collection.

**Headers:**
- `Authorization`: Token {your_auth_token}

**Example Request:**
```
GET /alvos-sob_investigacao/firestore-users/
```

**Example Response:**
```json
{
  "success": true,
  "collection": "users",
  "count": 3,
  "data": [
    {
      "id": "hWu861gV66a0cUuaDehWKujdXdY2",
      "nome": "Álvaro Mbeia Daniel Miguel",
      "email": "alvarombeiadanielmiguel@gmail.com",
      "fotoPerfil": "http://192.168.1.125:9000/nossacomunidade/user_photos/hWu861gV66a0cUuaDehWKujdXdY2/user_photos/hWu861gV66a0cUuaDehWKujdXdY2/profile.png",
      "bio": null,
      "morada": "Luanda",
      "dataNascimento": "2000-10-10T00:00:00.000",
      "lastActive": "2026-01-24T17:39:30Z",
      "fcmToken": "dNN0RPunSgOAEW7FkOX8xr:APA91bGJfBDkrlj595lu9KOTEg05mgZbfAjKd0YaCZRAAGknXsfJGECqdUnlCm-A8MNSqXVQMigfSKdT8Tp3RJ2HlL5ssOB5HjVhbcL9WooyGP9chyWiYkU",
      "telefone": "",
      "photos": [],
      "statuses": []
    }
  ]
}
```

### GET /monitorizacao-de-redes-sociais/nossa-comunidade/users/
Retrieves users from Firestore 'users' collection specifically for the 'Nossa Comunidade' section in social media monitoring.

**Headers:**
- `Authorization`: Token {your_auth_token}

**Example Request:**
```
GET /monitorizacao-de-redes-sociais/nossa-comunidade/users/
```

**Example Response:**
Same as above.

## Legacy Realtime Database Endpoints

### GET /alvos-sob-investigacao/firebase-data/
Retrieves data from Firebase Realtime Database.

**Query Parameters:**
- `path`: Path in the Firebase database (e.g., `/suspects`)

**Example Request:**
```
GET /alvos-sob_investigacao/firebase-data/?path=/suspects
```

**Example Response:**
```json
{
  "success": true,
  "path": "/suspects",
  "data": {
    "-Mabcdef123456": {
      "name": "John Doe",
      "crime_type": "Robbery",
      "date": "2023-01-15"
    },
    "-Mghijkl789012": {
      "name": "Jane Smith",
      "crime_type": "Fraud",
      "date": "2023-02-20"
    }
  }
}
```

### POST /alvos-sob-investigacao/firebase-data/
Performs various operations on Firebase data based on the action specified.

**Request Body:**
- `action`: Type of action to perform (`get`, `search`, `get_multiple`)
- `path`: Path in the Firebase database

**Actions:**

#### Action: `get`
Retrieves data from a specific path.

**Additional Request Body:**
- `record_id` (optional): Specific record ID to retrieve

**Example Request:**
```json
{
  "action": "get",
  "path": "/suspects",
  "record_id": "-Mabcdef123456"
}
```

#### Action: `search`
Searches data with query parameters.

**Additional Request Body:**
- `query_params`: Query parameters for filtering

**Example Request:**
```json
{
  "action": "search",
  "path": "/suspects",
  "query_params": {
    "orderBy": "\"crime_type\"",
    "equalTo": "\"Robbery\""
  }
}
```

#### Action: `get_multiple`
Retrieves data from multiple paths.

**Additional Request Body:**
- `paths`: Array of paths to retrieve

**Example Request:**
```json
{
  "action": "get_multiple",
  "paths": ["/suspects", "/crimes", "/reports"]
}
```

## Frontend Integration

### JavaScript Example
```javascript
// Fetch all suspects from Firebase
async function fetchFirebaseSuspects() {
  try {
    const response = await fetch('/alvos-sob-investigacao/firebase-data/?path=/suspects', {
      method: 'GET',
      headers: {
        'Authorization': 'Token YOUR_AUTH_TOKEN',
        'Content-Type': 'application/json',
      },
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('Firebase suspects:', data.data);
      // Process and display the data in your UI
      displayFirebaseData(data.data);
    } else {
      console.error('Error fetching Firebase data:', data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

// Search suspects by crime type
async function searchFirebaseSuspects(crimeType) {
  try {
    const response = await fetch('/alvos-sob-investigacao/firebase-data/', {
      method: 'POST',
      headers: {
        'Authorization': 'Token YOUR_AUTH_TOKEN',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        action: 'search',
        path: '/suspects',
        query_params: {
          orderBy: '"crime_type"',
          equalTo: `"${crimeType}"`
        }
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      console.log('Search results:', data.data);
      displayFirebaseData(data.data);
    } else {
      console.error('Error searching Firebase data:', data.error);
    }
  } catch (error) {
    console.error('Network error:', error);
  }
}

function displayFirebaseData(data) {
  // Example function to display data in your UI
  const container = document.getElementById('firebase-data-container');
  
  // Clear existing content
  container.innerHTML = '';
  
  // Iterate through the data and create UI elements
  Object.keys(data).forEach(key => {
    const item = data[key];
    const div = document.createElement('div');
    div.className = 'firebase-item';
    div.innerHTML = `
      <h3>${item.name || 'Unknown'}</h3>
      <p>Type: ${item.crime_type || 'N/A'}</p>
      <p>Date: ${item.date || 'N/A'}</p>
    `;
    container.appendChild(div);
  });
}
```

### React Example
```jsx
import { useState, useEffect } from 'react';

function FirebaseDataComponent() {
  const [firebaseData, setFirebaseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchFirebaseData();
  }, []);

  const fetchFirebaseData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('/alvos-sob-investigacao/firebase-data/?path=/suspects', {
        headers: {
          'Authorization': `Token ${localStorage.getItem('token')}`,
        },
      });
      
      const data = await response.json();
      
      if (data.success) {
        setFirebaseData(data.data);
      } else {
        setError(data.error);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading Firebase data...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h2>Firebase Data</h2>
      {firebaseData && Object.keys(firebaseData).map(key => (
        <div key={key} className="firebase-item">
          <h3>{firebaseData[key].name || 'Unknown'}</h3>
          <p>Type: {firebaseData[key].crime_type || 'N/A'}</p>
          <p>Date: {firebaseData[key].date || 'N/A'}</p>
        </div>
      ))}
    </div>
  );
}

export default FirebaseDataComponent;
```

## Environment Variables

Make sure the following environment variables are set in your `.env` file:

```
FIREBASE_API_KEY=AIzaSyBwkjtSZ1yru-3IQ94e0bhBz_WyMrzKSJY
FIREBASE_AUTH_DOMAIN=nossacomunidade-1d62d.firebaseapp.com
FIREBASE_DATABASE_URL=https://nossacomunidade-1d62d-default-rtdb.firebaseio.com
FIREBASE_PROJECT_ID=nossacomunidade-1d62d
FIREBASE_STORAGE_BUCKET=nossacomunidade-1d62d.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=462025426895
FIREBASE_APP_ID=1:462025426895:web:58c474485398961161b4ba
FIREBASE_MEASUREMENT_ID=G-M0MXM0H7G4
```

## Security Notes

1. The Firebase endpoints require authentication via the Authorization header
2. Only authenticated users can access the Firebase data
3. The Firebase configuration uses the Realtime Database rules for security
4. Make sure your Firebase Realtime Database rules are properly configured to restrict access