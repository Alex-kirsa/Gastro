import gspread

from config.settings import (
    FOOD_SPREADSHEET_ID,
    GOOGLE_SHEETS_CREDENTIALS_PATH,
)
import asyncio

# import datetime
from icecream import ic


# резервація під ід 0, меню дати 1, база страв 2


class GoogleSheets:
    def __init__(self):
        self._gc = gspread.service_account(filename=GOOGLE_SHEETS_CREDENTIALS_PATH)
        self._sh = self._gc.open_by_key(FOOD_SPREADSHEET_ID)
        # self._wks: list[gspread.Worksheet] = [
        #    gspread.Worksheet,
        #    gspread.Worksheet,
        #    gspread.Worksheet,
        # ]  # кожен об'єкт стане аркушем
        self._sheets_data: list[list[list]] = [
            self._sh.get_worksheet(0),  # [],
            [],
            [],
        ]  # кожен об'єкт перетвориться на список всіх рядків аркушу

    async def update_workspace(self):
        ic("update_workspace")
        for i in range(1, 3):
            wks = self._sh.get_worksheet(i)
            # self._wks[i] = self._sh.get_worksheet(i)
            self._sheets_data[i] = wks.get_all_values()
        await asyncio.sleep(60 * 5)
        await self.update_workspace()

    async def time_of_day_are_two(self, date: str) -> bool:
        # ic(date)
        all_values = self._sheets_data[1]
        date_count = 0
        for row in all_values:
            # ic(row[0])
            if row[0] == date:
                date_count += 1
        # ic(date_count)
        return date_count == 2

    async def get_dishes(self, date: str, time_of_day: str = None):
        all_values = self._sheets_data[1]
        for row in all_values:
            if row[0] == date:
                if time_of_day:
                    if row[1] == time_of_day:
                        return await self._analise(row.copy())
                else:
                    return await self._analise(row.copy())
        # ic(all_values)
        return []

    async def _analise(self, date_row_values: list):
        while "" in date_row_values:
            date_row_values.remove("")

        all_values = self._sheets_data[2]
        return_list: list[dict] = []

        if len(date_row_values) == 1:
            return []

        for _ in range(2):
            date_row_values.pop(0)

        for row in all_values:
            if row[0] in date_row_values:
                return_list.append({"name": row[1]})
                if len(row) == 3:
                    url = row[2]
                else:
                    url = ""
                return_list[-1].update({"url": url})

        assert return_list is not None
        return return_list

    async def write_book_data(self, data: dict):
        wks: gspread.Worksheet = self._sheets_data[0]

        wks.insert_row(
            list(data.values()),
            index=2,
        )


gs = GoogleSheets()
