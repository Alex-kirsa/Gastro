import gspread
from config.settings import SPREADSHEET_ID
import datetime


class GoogleSheets:
    def __init__(self):
        self._gc = gspread.service_account(filename="credentials.json")
        self._sh = self._gc.open_by_key(SPREADSHEET_ID)
        # self._wks = self._sh.get_worksheet(0)

    async def time_of_day_are_two(self, date: str) -> bool:
        wks = self._sh.get_worksheet(0)
        return bool(wks.col_values(1).count(date) - 1)

    async def get_dishes(self, date: datetime.date, time_of_day: str = None):
        pass
