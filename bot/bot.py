#-*-coding : utf-8 -*-

from platform import python_version
from time import gmtime, strftime, time
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
import os
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.database import session,base
from pyromod import listen
from bot import (
    STRING_SESSION,
    API_HASH,
    APP_ID,
    LOG_CHANNEL,
    LOG_DATETIME,
    LOGGER,
    STRING_SESSION,
    WORKERS,
    UPTIME,
    BOT_TOKEN)

class Bot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            STRING_SESSION,
            plugins=dict(root=f"{name}.plugins"),
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=WORKERS,
            parse_mode='html'
        )
        
        
    
    async def start(self):
        await super().start() 
        LOGGER.info("Starting bot...")
        
        me=await self.get_me()  
        LOGGER.info(
            f"Pyrogram v{__version__} (Layer - {layer}) started on {me.username} [{me.id}]",
        )
        LOGGER.info(f"Python Version: {python_version()}\n")
        LOGGER.info("Bot Started Successfully!\n")
        await self.send_message(LOG_CHANNEL, "<i>Starting Bot...</i>")
    async def stop(self):
        #LOGGER.info("Closing Database Connection")
        runtime = strftime("%Hh %Mm %Ss", gmtime(time() - UPTIME))
        LOGGER.info("Uploading logs before stopping...!\n")
        await self.send_message(
            LOG_CHANNEL,
                ("Bot Stopped!\n\n"
                f"Uptime: {runtime}\n"
                f"<code>{LOG_DATETIME}</code>")
            ),
        
        await super().stop()
        LOGGER.info(
            f"""Bot Stopped [Runtime: {runtime}s]\n
        """,
        )   
    