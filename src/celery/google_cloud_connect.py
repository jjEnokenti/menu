import apiclient
import httplib2
from oauth2client.service_account import ServiceAccountCredentials

from src.config import settings


def get_data_from_cloud():
    """"""

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        settings.CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
    )

    http_auth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=http_auth)

    res = service.spreadsheets().values().batchGet(spreadsheetId=settings.SPREADSHEET_ID,
                                                   ranges=['Sheet1!A:F']).execute()

    return res['valueRanges'][0]['values']
