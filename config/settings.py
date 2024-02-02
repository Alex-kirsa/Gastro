import dotenv
import os

DEBUG = True

dotenv.load_dotenv()
if DEBUG:
    BOT_TOKEN = os.getenv("DEBUG_BOT_TOKEN")
    # DATABASE_CONNECT = os.getenv("DEBUG_DATABASE")
else:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    # DATABASE_CONNECT = os.getenv("DATABASE_CONNECT")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
ADMINS_LIST = os.getenv("ADMINS_LIST")
