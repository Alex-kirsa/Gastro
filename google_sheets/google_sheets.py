import gspread
from config.settings import (
    FOOD_SPREADSHEET_ID,
    GOOGLE_SHEETS_CREDENTIALS_PATH,
)

# import datetime
# from icecream import ic


# резервація під ід 0, меню дати 1, база страв 2


class GoogleSheets:
    def __init__(self):
        self._gc = gspread.service_account(filename=GOOGLE_SHEETS_CREDENTIALS_PATH)
        # ic(self._wks.col_values(1))
        # ic(self._wks.get_all_values())
        # self._wks = self._sh.get_worksheet(0)

    async def time_of_day_are_two(self, date: str) -> bool:
        self._sh = self._gc.open_by_key(FOOD_SPREADSHEET_ID)
        self._wks = self._sh.get_worksheet(1)
        return len(self._wks.findall(date)) == 2

    async def get_dishes(self, date: str, time_of_day: str = None):
        self._sh = self._gc.open_by_key(FOOD_SPREADSHEET_ID)
        self._wks = self._sh.get_worksheet(1)
        # ic(self._first_col_values)
        # cell = self._wks.find(date)
        # ic(cell.col)

        # for i in range(len(self._first_col_values)):
        #    # i, self._first_col_values[i]
        #    # ic("DATE")
        #    if date == self._first_col_values[i]:
        # ic(date)
        cell = self._wks.find(date)
        if cell is None:
            return []
        # ic(date)
        row_values = self._wks.row_values(cell.row)
        # ic(row_values)
        if len(row_values) == 0:
            return []

        if time_of_day:
            if row_values[1] == time_of_day:
                return await self._analise(row_values)
        else:
            return await self._analise(row_values)

    async def _analise(self, date_row_values: list):
        # ic(row_values[2:])
        while "" in date_row_values:
            date_row_values.remove("")

        self._wks = self._sh.get_worksheet(2)
        # ic(first_col)
        return_list: list[dict] = []
        # ic(row_values)
        # ic(date_row_values)

        if len(date_row_values) == 1:
            return []

        for _ in range(2):
            date_row_values.pop(0)
        # ic(date_row_values)
        for el in date_row_values:
            # ic(el)
            row_values = self._wks.row_values(self._wks.find(el).row)
            # ic(row_values)
            return_list.append({"name": row_values[1]})
            if len(row_values) == 3:
                return_list[-1].update({"url": row_values[2]})
            else:
                return_list[-1].update({"url": ""})
                # ic(return_list)
        assert return_list is not None
        return return_list

    async def write_book_data(self, data: dict):
        self._sh = self._gc.open_by_key(FOOD_SPREADSHEET_ID)
        self._wks = self._sh.get_worksheet(0)

        self._wks.insert_row(
            [
                data.get("name"),
                data.get("phone"),
                data.get("action"),
                data.get("num_of_people"),
                data.get("desired_date"),
            ],
            index=2,
        )
