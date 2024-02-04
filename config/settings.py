import dotenv
import os

DEBUG = False

dotenv.load_dotenv()
if DEBUG:
    BOT_TOKEN = os.getenv("DEBUG_BOT_TOKEN")
    CHANNEL_ID = os.getenv("DEBUG_CHANNEL_ID")
    MANAGER_PHONE_NUMBER = os.getenv("DEBUG_MANAGER_PHONE_NUMBER")
    FOOD_SPREADSHEET_ID = os.getenv("DEBUG_FOOD_SPREADSHEET_ID")
    BOOK_SPREADSHEET_ID = os.getenv("DEBUG_BOOK_SPREADSHEET_ID")
    GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("DEBUG_GOOGLE_SHEETS_CREDENTIALS_PATH")
else:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    MANAGER_PHONE_NUMBER = os.getenv("MANAGER_PHONE_NUMBER")
    FOOD_SPREADSHEET_ID = os.getenv("FOOD_SPREADSHEET_ID")
    BOOK_SPREADSHEET_ID = os.getenv("BOOK_SPREADSHEET_ID")
    GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH")

REMINDER_SECS = 60 * 60 * 24
ADMINS_LIST = (706030949, 1072064812, 626252754)
