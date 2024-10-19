from pyrogram import filters,Client
import csv
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.model.user_db import get_admin
from bot.utils.markup import admin_markup,list_markup
from bot import LOGGER,LOG_CHANNEL,SUDO_USERS
from bot.database.model.user_db import get_all_user_data,total_users
from  bot.database.model.channel_db import (total_banned_channel,
                                            total_channel,
                                            get_channel,
                                            get_banned_channel_list,
                                            
                                            get_user_channel_count)


@Bot.on_callback_query(filters.regex('^list$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def list_handler(bot:Client,message:Message):
    await bot.send_message(message.message.chat.id,"☑️ Choose Required List",reply_markup=list_markup())
    
@Bot.on_callback_query(filters.regex('^ban_list$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def ban_list_handler(bot:Client,message:Message):
    channel_count=total_banned_channel()
    text=""
    ban_channels=get_banned_channel_list()
    for channel in ban_channels:
            text+=str(channel)+'\n'
            data=f'Total Banned Channels : {channel_count}\n\n{text}'
            await bot.send_message(message.message.chat.id,data)
            
@Bot.on_callback_query(filters.regex('^user_list$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def user_list_handler(bot:Client,message:Message):        
    users=get_all_user_data()
    with open("users.txt","w",encoding='UTF-8') as f:
            for user in users:
                channel=get_user_channel_count(user.chat_id)
                data=f"""
🆔 ID : {user.chat_id}
📛 Name : {user.first_name}
👤 Username : {user.username}
🗓 Joined at : {user.date}
📢 No. of Registed Channels : {channel}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
                """
                f.write(data)
    await bot.send_document(message.from_user.id,'users.txt',caption=f'Total Users : {total_users()}',file_name='user_list.txt')
                
@Bot.on_callback_query(filters.regex('^channel_list$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def channel_list_handler(bot:Client,message:Message):   
    channels=get_channel()
    with open("channels.txt","w",encoding='UTF-8') as f:
            for channel in channels:
                data=f"""
🆔 ID : {channel.channel_id}
📛 Name : {channel.channel_name}
👤 Subscribers : {channel.subscribers}
📄 Description : {channel.description}
👨‍ Admin : {channel.admin_username} [{channel.chat_id}]
🔗 Invite Link : {channel.invite_link}
➖➖➖➖➖➖➖➖➖➖➖➖➖➖  
"""
                f.write(data)
    await bot.send_document(message.from_user.id,'channels.txt',caption=f'Total channels : {total_channel()}',file_name='channel_list.txt')