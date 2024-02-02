import gspread
from config.settings import SPREADSHEET_ID
import datetime
from icecream import ic


class GoogleSheets:
    def __init__(self):
        self._gc = gspread.service_account(filename="google_sheets/credentials.json")
        self._sh = self._gc.open_by_key(SPREADSHEET_ID)
        self._wks = self._sh.get_worksheet(1)
        self._first_col_values = self._wks.col_values(1)
        # ic(self._wks.get_all_values())
        # self._wks = self._sh.get_worksheet(0)

    async def time_of_day_are_two(self, date: str) -> bool:
        return self._first_col_values.count(date) == 2

    async def get_dishes(self, date: str, time_of_day: str = None):
        self._wks = self._sh.get_worksheet(1)
        for i in range(len(self._first_col_values)):
            i, self._first_col_values[i]
            if date == self._first_col_values[i]:
                row_values = self._wks.row_values(i)
                # row_values
                if time_of_day:
                    if row_values[1] == time_of_day:
                        return await self._analise(row_values)
                else:
                    return await self._analise(row_values)

    async def _analise(self, row_values):
        self._wks = self._sh.get_worksheet(2)
        first_col = self._wks.col_values(1)
        return_list: list[dict] = []
        for el in row_values[2:]:
            for i in range(len(first_col)):
                if el == first_col[i]:
                    row_values = self._wks.row_values(i)
                    return_list.append({"name": row_values[1], "url": row_values[2]})
        return return_list
