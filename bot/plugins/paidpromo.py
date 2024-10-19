from pyrogram import filters,Client
from bot.bot import Bot
from pyrogram.types import Message
import traceback,time
from bot.database.model.user_db import get_admin
from bot.utils.markup import admin_markup,back_markup,empty_markup,promo_button_markup
from bot import LOGGER,LOG_CHANNEL,SUDO_USERS,SUPPORT_CHANNEL
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired,ChannelPrivate
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden,ChatForbidden
from bot.database.model.promo_db import add_paidpromo,delete_paid_promo,get_paidpromo
from bot.database.model.channel_db  import get_channel,get_channel_by_id

@Bot.on_callback_query(filters.regex('^send_paid_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def paid_promo_handler(bot:Client,message:Message):
    error_list=""
    msg=await bot.ask(message.message.chat.id,"**✅ Send Text With Parse mode(if required)**",parse_mode='markdown',reply_markup=back_markup())
    if msg.text=='🚫 Cancel':
        await bot.send_message(message.message.chat.id,"Terminated",reply_markup=empty_markup())
    else:
        if msg.media is True:
            m=await bot.send_photo(SUPPORT_CHANNEL,msg.photo.file_id,caption=msg.caption,parse_mode='HTML',reply_markup=promo_button_markup())
        else:
            m=await bot.send_message(SUPPORT_CHANNEL,msg.text,reply_markup=promo_button_markup(),parse_mode='HTML')
        chname=get_channel()
        for x in chname:                    
            try:
                id_channel=await bot.forward_messages(chat_id=x.channel_id,from_chat_id=SUPPORT_CHANNEL,message_ids=m.message_id)
                add_paidpromo(x.channel_id,id_channel.message_id)
            except (ChatAdminRequired,ChannelPrivate,ChatWriteForbidden,ChatForbidden):
                await bot.send_message(x.chat_id,f"Failed to send message for {x.channel_name}\nRepost the promo to avoid ban")
                error_list+=f"🆔 ID : {x.channel_id}\n📛 Name : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Link : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
            except Exception as e:
                await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode='html')
                LOGGER.error(e)
        
        await bot.send_message(message.message.chat.id,f"DONE",reply_markup=empty_markup())
        await bot.send_message(message.from_user.id,f"Failed to Send Message \n\n {error_list}")
        #await bot.send_message(SUPPORT_CHANNEL,f"Error List \n\n {error_list}")
        
@Bot.on_callback_query(filters.regex('^delete_paid_promo$')& (filters.user(get_admin()) | filters.user(SUDO_USERS)))
async def delete_paid_promo_handler(bot:Client,message:Message):
    error_list=""
    promo=get_paidpromo()
    for i in promo:
            print(i.message_id)
            try:
                messages=await bot.delete_messages(i.channel,i.message_id)
                if messages is False:
                    x=get_channel_by_id(i.channel)
                    error_list+=f"🆔 ID : {x.channel_id}\n📛 Name : {x.channel_name}\n👨‍ Admin : @{x.admin_username} \n🔗Link : {x.invite_link}\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
            except Exception as e:
                await bot.send_message(LOG_CHANNEL,f'\n<code>{traceback.format_exc()}</code>\n\nTime : {time.ctime()} UTC',parse_mode='html')
                LOGGER.error(e)
    delete_paid_promo()
    await bot.send_message(message.message.chat.id,"✅ DONE")
    await bot.send_message(message.from_user.id,f"Failed to delete message\n\n {error_list}",disable_web_page_preview=True)