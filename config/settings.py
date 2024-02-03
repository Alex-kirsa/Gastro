import dotenv
import os

DEBUG = True

dotenv.load_dotenv()
if DEBUG:
    BOT_TOKEN = os.getenv("DEBUG_BOT_TOKEN")
    CHANNEL_ID = os.getenv("DEBUG_CHANNEL_ID")
    MANAGER_PHONE_NUMBER = os.getenv("DEBUG_MANAGER_PHONE_NUMBER")
    SPREADSHEET_ID = os.getenv("DEBUG_SPREADSHEET_ID")
else:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    MANAGER_PHONE_NUMBER = os.getenv("MANAGER_ID")
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


ADMINS_LIST = (706030949,)
