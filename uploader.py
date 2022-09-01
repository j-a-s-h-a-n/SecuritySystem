import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import  build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

class VideoUpload():

    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']

        self.creds = None

        if os.path.exists('token.json'):
            self.creds=Credentials.from_authorized_user_file('token.json',SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json',SCOPES
                )

                self.creds= flow.run_console(port=0)

            with open('token.json','w') as token:
                token.write(self.creds.to_json())
        try:
            self.service = build('drive', 'v3', credentials=self.creds)

            response = self.service.files().list(
                q="name = 'Footage' and mimeType='application/vnd.google-apps.folder'",
                spaces = 'drive'
            ).execute()

            if not response['files']:
                file_metadata={
                    'name':'Footage',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                file = self.service.files().create(body=file_metadata,fields='id').execute()
                self.folder_id = file.get('id')
            else:
                self.folder_id = response['files'][0]['id']

        except HttpError as e:
            print("Error: " + str(e))

    def uploadFile(self,file):
        file_metadata = {
            'name': file,
            'parents': [self.folder_id]
        }
        media = MediaFileUpload(f'videos/{file}')
        upload_file = self.service.files().create(body=file_metadata,
                                             media_body=media,
                                             fields='id').execute()
        print("uploaded to drive")
