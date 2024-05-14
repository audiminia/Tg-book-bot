from pyrogram import Client, enums
from pyrogram.enums import ParseMode
import sys
from datetime import datetime
import os

from config import API_HASH, API_ID, LOGGER, BOT_TOKEN, BOT_WORKERS, PORT
import logging

class Bot(Client):
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        logging.getLogger("pyrogram").setLevel(logging.INFO)
            
        super().__init__(
            name="Book-Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins"},
            workers=BOT_WORKERS,
            bot_token=BOT_TOKEN,
        )
        self.LOGGER = LOGGER
        
    async def start(self):
        try:
            await super().start()
            usr_bot_me = await self.get_me()
            self.username = usr_bot_me.username
            self.namebot = usr_bot_me.first_name
            self.LOGGER(__name__).info(f"Bot info!\n┌ First Name: {self.namebot}\n└ Username: @{self.username}\n——")
        except Exception as a:
            self.LOGGER(__name__).warning(a)
            self.LOGGER(__name__).info("Bot failed to start")
            sys.exit()
        
    async def stop(self, *args):
        await super().stop()
        LOGGER(__name__).info("Bot stopped.")
        
if __name__ == "__main__":
    Bot().run()
