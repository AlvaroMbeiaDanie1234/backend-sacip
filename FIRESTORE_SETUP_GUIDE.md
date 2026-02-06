# Firestore Setup Guide for SACIP

## Authentication Configuration

To connect to your Firestore database, you need to configure authentication credentials.

### Option 1: Service Account Key File (Recommended for Development)

1. **Get your service account key:**
   - Go to Firebase Console: https://console.firebase.google.com/
   - Select your project "nossacomunidade-1d62d"
   - Go to Project Settings (gear icon) → Service Accounts
   - Click "Generate new private key"
   - Save the JSON file to a secure location

2. **Set the environment variable:**
   ```bash
   # Windows Command Prompt
   set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\your\serviceAccountKey.json
   
   # Windows PowerShell
   $env:GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\serviceAccountKey.json"
   ```

### Option 2: Environment Variable with JSON Content

Alternatively, you can set the entire service account JSON as an environment variable:

```bash
# Windows Command Prompt
set FIREBASE_SERVICE_ACCOUNT_JSON={"type": "service_account", ...your_full_json_content...}

# Windows PowerShell
$env:FIREBASE_SERVICE_ACCOUNT_JSON='{"type": "service_account", ...your_full_json_content...}'
```

### Option 3: Using .env file

Add to your `.env` file in the backend-v2 directory:
```
FIREBASE_SERVICE_ACCOUNT_JSON={"type": "service_account", ...your_full_json_content...}
```

## Testing the Connection

After setting up authentication, you can test the connection:

1. **Run the Django development server:**
   ```bash
   cd backend-v2
   python manage.py runserver
   ```

2. **Access the endpoints:**
   - Users from Firestore: `GET /alvos-sob-investigacao/firestore-users/`
   - Nossa Comunidade: `GET /monitorizacao-de-redes-sociais/nossa-comunidade/users/`

## Troubleshooting

### Common Issues:

1. **Authentication Error**: Make sure your service account key is valid and has Firestore access permissions
2. **Project ID Mismatch**: Ensure the project ID in the service account matches your Firebase project ID
3. **Network Issues**: Verify your internet connection and firewall settings

### Verification Steps:

1. Check that your service account key JSON contains:
   - `project_id` field matching "nossacomunidade-1d62d"
   - Valid `private_key` and `client_email` fields

2. Test the authentication separately:
   ```python
   from google.oauth2 import service_account
   import json
   
   # Load your service account key
   with open('path/to/serviceAccountKey.json', 'r') as f:
       key_data = json.load(f)
   
   credentials = service_account.Credentials.from_service_account_info(key_data)
   print("Credentials loaded successfully:", credentials.project_id)
   ```

## Production Deployment

For production deployment:
1. Store the service account key securely (never commit to version control)
2. Use environment variables or cloud secret management
3. Ensure the deployed environment has access to the credentials

## Frontend Integration

Once the backend is properly configured:
1. The "Nossa Comunidade" tab will appear in the "Monitorização de Redes Sociais" section
2. It will fetch users from your Firestore 'users' collection
3. Users will be displayed with their profile information (name, photo, location, etc.)

## Security Notes

- Keep your service account key secure and never expose it in client-side code
- Limit the permissions of the service account to only necessary Firestore operations
- Regularly rotate your service account keys for security