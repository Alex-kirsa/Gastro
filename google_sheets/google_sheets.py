import gspread
from config.settings import SPREADSHEET_ID


class GoogleSheets:
    def __init__(self):
        self._gc = gspread.service_account(filename="cre")
        self._sh = self._gc.open_by_key(SPREADSHEET_ID)
        self.wks = self._sh.get_worksheet(0)

    def count_column_values(self):
        return self.wks.row_count - 1
