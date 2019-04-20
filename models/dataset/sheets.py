from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1XmLsX8CaI067RomchkxUOEm_2eZvZUISm3HG1Q6Z9y8'
SAMPLE_RANGE_NAME = 'A2:B'

class Sheets(object):
  def __init__(self, credentials_path):
    self.creds = self.login_verification(credentials_path)
    self.service = build('sheets', 'v4', credentials=self.creds)
    
  def login_verification(self, credentials_path):
      creds = None
      # The file token.pickle stores the user's access and refresh tokens, and is
      # created automatically when the authorization flow completes for the first
      # time.
      if os.path.exists('token.pickle'):
          with open('token.pickle', 'rb') as token:
              creds = pickle.load(token)
      # If there are no (valid) credentials available, let the user log in.
      if not creds or not creds.valid:
          if creds and creds.expired and creds.refresh_token:
              creds.refresh(Request())
          else:
              flow = InstalledAppFlow.from_client_secrets_file(
                  credentials_path, SCOPES)
              creds = flow.run_local_server()
          # Save the credentials for the next run
          with open('token.pickle', 'wb') as token:
              pickle.dump(creds, token)
      return creds


  def get_spreadsheet_data(self, spreadsheet_id, spreadsheet_range):
    sheet = self.service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=spreadsheet_range).execute()
    return result.get('values', [])


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    sheets = Sheets('./credentials.json')

    # Call the Sheets API
    values = sheets.get_spreadsheet_data(SAMPLE_SPREADSHEET_ID,
                                  SAMPLE_RANGE_NAME)

    if not values:
        print('No data found.')
    else:
        print('Word, Classification (0-2):')
        for row in values[:3]:
                # Print columns A and B, which correspond to indices 0 and 1.
            print('%s, %s' % (row[0], row[1]))


if __name__ == '__main__':
    main()
