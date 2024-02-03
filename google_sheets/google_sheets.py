import gspread
from config.settings import SPREADSHEET_ID

# import datetime
from icecream import ic


class GoogleSheets:
    def __init__(self):
        self._gc = gspread.service_account(filename="google_sheets/credentials.json")
        self._sh = self._gc.open_by_key(SPREADSHEET_ID)
        self._wks = self._sh.get_worksheet(1)
        # ic(self._wks.col_values(1))
        self._first_col_values = self._wks.col_values(1)
        # ic(self._wks.get_all_values())
        # self._wks = self._sh.get_worksheet(0)

    async def time_of_day_are_two(self, date: str) -> bool:
        return self._first_col_values.count(date) == 2

    async def get_dishes(self, date: str, time_of_day: str = None):
        self._wks = self._sh.get_worksheet(1)
        # ic(self._first_col_values)
        for i in range(len(self._first_col_values)):
            # i, self._first_col_values[i]
            # ic("DATE")
            if date == self._first_col_values[i]:
                row_values = self._wks.row_values(i)
                # row_values
                if time_of_day:
                    if row_values[1] == time_of_day:
                        return await self._analise(row_values)
                else:
                    return await self._analise(row_values)

    async def _analise(self, row_values):
        # ic(row_values[2:])
        while "" in row_values:
            row_values.remove("")

        self._wks = self._sh.get_worksheet(2)
        first_col = self._wks.col_values(1)
        # ic(first_col)
        return_list: list[dict] = []
        # ic(row_values)
        for el in row_values[2:]:
            # ic(el)
            # ic(first_col)
            for i in range(len(first_col)):
                # ic(i)
                if el == first_col[i]:
                    # ic(el, first_col[i])
                    row_values = self._wks.row_values(i + 1)
                    # ic(row_values)
                    return_list.append({"name": row_values[1]})
                    if len(row_values) == 3:
                        return_list[-1].update({"url": row_values[2]})
                    else:
                        return_list[-1].update({"url": ""})
                    # ic(return_list)
        assert return_list is not None
        return return_list
