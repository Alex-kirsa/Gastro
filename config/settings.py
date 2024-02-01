import importlib

dotenv = importlib.import_module('dotenv')

config: dict[str, str] = dotenv.dotenv_values("config/.env")

DEBUG = True

if DEBUG:
    BOT_TOKEN: str = config["DEBUG_BOT_TOKEN"]
else:
    BOT_TOKEN: str = config["BOT_TOKEN"]

ADMINS_LIST = config["ADMINS_LIST"]




