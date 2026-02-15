# Spyware Integration Documentation

## Overview
This document describes the integration of spyware functionality into the Police Intelligence System backend for educational/study purposes.

## ⚠️ Important Legal Notice
This code is for **EDUCATIONAL AND STUDY PURPOSES ONLY**. Unauthorized surveillance is illegal in most jurisdictions.

## System Components

### 1. Core Files
- `spyware_utils.py` - Main spyware functionality
- `spyware_views.py` - Django REST API endpoints
- `spyware_requirements.txt` - Required dependencies

### 2. API Endpoints

#### Start Surveillance
```
POST /api/informacoes-suspeitas/surveillance/start/
```
**Request Body:**
```json
{
    "suspect_id": 1,
    "operation_name": "Target Monitoring",
    "duration": 300
}
```

**Response:**
```json
{
    "message": "Surveillance session started successfully",
    "session_id": "uuid-here",
    "informacao_id": 123,
    "operation_name": "Target Monitoring",
    "suspect_id": 1,
    "duration": 300
}
```

#### Get Session Status
```
GET /api/informacoes-suspeitas/surveillance/status/<session_id>/
```

#### List All Operations
```
GET /api/informacoes-suspeitas/surveillance/list/
```

#### Stop Surveillance
```
POST /api/informacoes-suspeitas/surveillance/stop/<session_id>/
```

#### Decrypt Collected Data
```
POST /api/informacoes-suspeitas/surveillance/decrypt/
```
**Request Body:**
```json
{
    "session_id": "uuid-here",
    "decryption_key": "MujBTqtZ4QCQW_fmlMHVWBmTVRW8IGZSuxFctu_D3d0="
}
```

## Installation

### 1. Install Dependencies
```bash
pip install -r informacoes_suspeitas/spyware_requirements.txt
```

### 2. Required System Permissions
- Camera access
- Microphone access
- File system access
- Network access

### 3. Configuration
Update the following in `spyware_utils.py`:
- `EMAIL_ADDRESS` - Your email for data transmission
- `EMAIL_PASSWORD` - Email password
- `ENCRYPTION_KEY` - Keep secure, used for file encryption

## Data Collection Features

### What Gets Collected:
1. **Keystrokes** - All keyboard input logging
2. **Screenshots** - Periodic screen captures (every 5 seconds)
3. **Audio Recording** - Microphone capture (10-second segments)
4. **Webcam Images** - Camera snapshots (every 5 seconds)
5. **Network Information** - WiFi profiles, IP addresses, network stats
6. **System Information** - Hardware specs, running processes
7. **Clipboard Data** - Copied/pasted content
8. **Browser History** - Web browsing activity

### Data Storage:
- Files stored in: `C:/Users/Public/Logs/session_<UUID>/`
- All files encrypted with Fernet encryption
- Original files deleted after encryption
- Encrypted files can be sent via email

## Security Features

### Encryption
- Uses Fernet symmetric encryption
- All collected data is encrypted before storage
- Decryption requires the correct key

### Data Management
- Automatic cleanup of original files
- Session-based organization
- Secure file handling

## Usage Examples

### Starting a Surveillance Session
```python
import requests

# Start surveillance
response = requests.post(
    'http://localhost:8000/api/informacoes-suspeitas/surveillance/start/',
    headers={'Authorization': 'Bearer your-token'},
    json={
        'suspect_id': 1,
        'operation_name': 'Study Session Monitoring',
        'duration': 180  # 3 minutes
    }
)
print(response.json())
```

### Decrypting Collected Data
```python
# Decrypt session data
response = requests.post(
    'http://localhost:8000/api/informacoes-suspeitas/surveillance/decrypt/',
    headers={'Authorization': 'Bearer your-token'},
    json={
        'session_id': 'your-session-uuid',
        'decryption_key': 'MujBTqtZ4QCQW_fmlMHVWBmTVRW8IGZSuxFctu_D3d0='
    }
)
print(response.json())
```

## ⚠️ Ethical Considerations

This system should only be used for:
- Educational purposes
- Authorized security research
- Legally permitted surveillance with proper consent
- Academic study of cybersecurity concepts

**Never use for:**
- Unauthorized surveillance
- Privacy invasion
- Illegal monitoring
- Commercial spyware deployment

## Troubleshooting

### Common Issues:
1. **Permission Errors** - Run as administrator
2. **Camera/Microphone Access** - Check device permissions
3. **Email Sending** - Verify SMTP settings
4. **File Access** - Ensure proper directory permissions

### Logs:
Check `C:/Users/Public/Logs/spyware_operations.log` for detailed operation logs.

## Disclaimer
This code is provided for educational purposes only. The authors are not responsible for any misuse or illegal activities conducted with this software.