import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


class GoogleDocs:
    def __init__(self, keyfile=None):
        """
        Initializes the GoogleDocs class with credentials for Google API.
        :param keyfile: Path to the JSON file containing Google service account credentials.
        Defaults to "./credentials.json" if not provided.
        """
        if keyfile is None:
            keyfile = "./credentials.json"

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile, scope)
        self.spreadsheet = None
        self.gc = gspread.authorize(credentials)

    def get_dataframe(self, spreadsheet_key, worksheet_index=0, worksheet_title=None) -> pd.DataFrame:
        """
        Returns a worksheet from a Google Spreadsheet as a pandas DataFrame.
        :param spreadsheet_key: ID of the Google Spreadsheet.
        :param worksheet_index: Index of the worksheet (default: 0).
        :param worksheet_title: Title of the worksheet (overrides index if set).
        :return: pandas DataFrame with the worksheet data.
        """
        spreadsheet = self.gc.open_by_key(spreadsheet_key)
        if worksheet_title:
            worksheet = spreadsheet.worksheet(worksheet_title)
        else:
            worksheet = spreadsheet.get_worksheet(worksheet_index)
        data = worksheet.get_all_values()
        return pd.DataFrame(data[1:], columns=data[0])

    # def write_dataframe(self, ):

