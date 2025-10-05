#!/usr/bin/env python3

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import pickle
import os
import io
import pandas as pd

class GoogleDriveHandler:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.service = self.authenticate()
        
    def authenticate(self):
        """Authenticate with Google Drive API"""
        creds = None
        
        # Check if token.pickle exists
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
                
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Use environment variables for credentials in production
                if os.environ.get('GOOGLE_CREDENTIALS'):
                    # Production: use service account
                    from google.oauth2 import service_account
                    import json
                    
                    credentials_info = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
                    creds = service_account.Credentials.from_service_account_info(
                        credentials_info, scopes=self.SCOPES)
                else:
                    # Development: use OAuth flow
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                    
            # Save credentials for next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
                
        return build('drive', 'v3', credentials=creds)
    
    def upload_excel_file(self, file_path, file_name="Chartink_Workflow.xlsx"):
        """Upload Excel file to Google Drive"""
        try:
            # Check if file already exists
            existing_file = self.find_file(file_name)
            
            media = MediaIoBaseUpload(
                io.BytesIO(open(file_path, 'rb').read()),
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            if existing_file:
                # Update existing file
                file = self.service.files().update(
                    fileId=existing_file['id'],
                    media_body=media
                ).execute()
                print(f"Updated file: {file.get('name')} (ID: {file.get('id')})")
            else:
                # Create new file
                file_metadata = {'name': file_name}
                file = self.service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
                print(f"Created file: {file_name} (ID: {file.get('id')})")
                
            return file.get('id')
            
        except Exception as e:
            print(f"Error uploading file: {str(e)}")
            return None
    
    def download_excel_file(self, file_name="Chartink_Workflow.xlsx", local_path="Chartink_Workflow.xlsx"):
        """Download Excel file from Google Drive"""
        try:
            file_info = self.find_file(file_name)
            if not file_info:
                print(f"File {file_name} not found in Google Drive")
                return False
                
            request = self.service.files().get_media(fileId=file_info['id'])
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                
            # Save to local file
            with open(local_path, 'wb') as f:
                f.write(file_content.getvalue())
                
            print(f"Downloaded {file_name} to {local_path}")
            return True
            
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
            return False
    
    def find_file(self, file_name):
        """Find file by name in Google Drive"""
        try:
            results = self.service.files().list(
                q=f"name='{file_name}'",
                fields="files(id, name)"
            ).execute()
            
            files = results.get('files', [])
            return files[0] if files else None
            
        except Exception as e:
            print(f"Error finding file: {str(e)}")
            return None
