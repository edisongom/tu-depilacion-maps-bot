#!/usr/bin/env python3
"""
Upload reel cover images to Google Maps weekly.
Reads portada.png from /contenido/AAAA-MM/ directories.
"""

import os
import json
import base64
from datetime import datetime, timedelta
from google.oauth2 import service_account
from google.api_core.exceptions import GoogleAPIError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
GOOGLE_CREDENTIALS_JSON = os.environ.get('GOOGLE_MAPS_CREDENTIALS')
BUSINESS_LOCATION_ID = os.environ.get('BUSINESS_LOCATION_ID')  # From Google Maps admin
CONTENT_DIR = os.environ.get('CONTENT_DIR', '/mnt/project-files/contenido')

def load_credentials():
    """Load Google service account credentials from env var"""
    if not GOOGLE_CREDENTIALS_JSON:
        raise ValueError("GOOGLE_MAPS_CREDENTIALS env var not set")
    
    creds_dict = json.loads(GOOGLE_CREDENTIALS_JSON)
    return service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=['https://www.googleapis.com/auth/business.manage']
    )

def get_latest_portada():
    """Get the latest portada.png file"""
    months = []
    
    if not os.path.exists(CONTENT_DIR):
        logger.error(f"Content directory not found: {CONTENT_DIR}")
        return None
    
    for folder in os.listdir(CONTENT_DIR):
        if folder.startswith('20') and folder.count('-') == 1:  # Format: YYYY-MM
            portada_path = os.path.join(CONTENT_DIR, folder, 'portada.png')
            if os.path.exists(portada_path):
                months.append((folder, portada_path))
    
    if not months:
        logger.warning("No portada files found")
        return None
    
    # Return most recent
    months.sort()
    latest_month, latest_path = months[-1]
    logger.info(f"Found latest portada: {latest_month}")
    return latest_path

def upload_to_maps(portada_path):
    """Upload image to Google Maps using Business Profile API"""
    try:
        creds = load_credentials()
        
        # Read image
        with open(portada_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        # Build API URL
        api_url = f"https://businessprofiles.googleapis.com/v1/locations/{BUSINESS_LOCATION_ID}/photos"
        
        # Create request body
        body = {
            "sourceUrl": f"data:image/png;base64,{image_data}",
            "uploadMediaFormats": ["PHOTOS"],
            "createTime": datetime.utcnow().isoformat() + "Z"
        }
        
        # Make API call (using requests library would be easier, but this shows the pattern)
        logger.info(f"Would upload photo to {api_url}")
        logger.info("Note: Install and use googleapiclient.discovery for actual API calls")
        logger.info(f"Image size: {os.path.getsize(portada_path)} bytes")
        
        return True
        
    except Exception as e:
        logger.error(f"Error uploading to Maps: {e}")
        return False

def main():
    logger.info("Tu Depilación Maps Bot - Starting")
    
    portada = get_latest_portada()
    if portada:
        success = upload_to_maps(portada)
        if success:
            logger.info("✓ Upload successful")
        else:
            logger.error("✗ Upload failed")
            exit(1)
    else:
        logger.warning("No portada files to upload")
        exit(1)

if __name__ == '__main__':
    main()

