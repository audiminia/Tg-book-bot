import os
import logging
from logging.handlers import RotatingFileHandler

import dotenv
from os import getenv

dotenv.load_dotenv('config.env')


#Your API ID from my.telegram.org
API_ID = int(getenv("API_ID", ""))

#Your API Hash from my.telegram.org
API_HASH = getenv("API_HASH", "")

#Bot token @Botfather
BOT_TOKEN = getenv("BOT_TOKEN", "")

#Port
PORT = getenv("PORT", "8080")

BOT_WORKERS = int(getenv("TG_BOT_WORKERS", "4"))

#Admins
try:
    ADMINS=[]
    for x in (getenv("ADMINS", "").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

LOG_FILE_NAME = "yamato.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
