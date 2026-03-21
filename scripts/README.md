# Suspicious Information Photo Sync Scripts

This directory contains scripts for automatically syncing photos from suspicious information records from the external API to the local media folder.

## Available Scripts

### `sync_suspicious_info_cron.py`
This script fetches suspicious information from the external API (`http://10.110.2.220:3333/api/v1/inteligency/actions-suspectius`) and downloads associated photos to the local media folder at `media/suspicious_info_photos/`.

The script:
- Fetches all suspicious information records from the external API
- Checks if photos already exist locally (skips if they do)
- Downloads new photos using the correct URL pattern
- Updates the local database with photo paths

## Automatic Execution Setup

For detailed instructions on setting up automatic execution, see [SYNC_SUSPICIOUS_INFO_SETUP.md](SYNC_SUSPICIOUS_INFO_SETUP.md).

## URL Pattern Handling
The script properly handles the external API's URL pattern:
- External API returns relative paths like `/410/1764538518979.jpg`
- These are accessed through the proxy endpoint: `http://10.110.2.220:3333/api/v1/files?url=%2F410%2F1764538518979.jpg`

## Media Storage Location
All suspicious information photos are stored in:
`C:\Users\Alvaro\Music\PNA\SACIP\backend-v2\media\suspicious_info_photos\`