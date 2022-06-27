#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.
import asyncio

from pyrogram import filters
from pyrogram.types import CallbackQuery, Message

from config import BANNED_USERS, MUSIC_BOT_NAME, adminlist, lyrical
from strings import get_command
from YukkiMusic import app
from YukkiMusic.core.call import Yukki
from YukkiMusic.misc import db
from YukkiMusic.utils.database import get_authuser_names, get_cmode
from YukkiMusic.utils.decorators import (ActualAdminCB, AdminActual,
                                         language)
from YukkiMusic.utils.formatters import alpha_to_int

### Multi-Lang Commands
RELOAD_COMMAND = get_command("RELOAD_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")


@app.on_message(
    filters.command(RELOAD_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@language
async def reload_admin_cache(client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = await app.get_chat_members(
            chat_id, filter="administrators"
        )
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.can_manage_voice_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except:
        await message.reply_text(
            "𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙧𝙚𝙡𝙤𝙖𝙙 𝙖𝙙𝙢𝙞𝙣𝙘𝙖𝙘𝙝𝙚. 𝙈𝙖𝙠𝙚 𝙨𝙪𝙧𝙚 𝘽𝙤𝙩 𝙞𝙨 𝙖𝙙𝙢𝙞𝙣 𝙞𝙣 𝙮𝙤𝙪𝙧 𝙘𝙝𝙖𝙩."
        )


@app.on_message(
    filters.command(RESTART_COMMAND)
    & filters.group
    & ~filters.edited
    & ~BANNED_USERS
)
@AdminActual
async def restartbot(client, message: Message, _):
    mystic = await message.reply_text(
        f"𝙋𝙡𝙚𝙖𝙨𝙚 𝙒𝙖𝙞𝙩.. 𝙍𝙚𝙨𝙩𝙖𝙧𝙩𝙞𝙣𝙜 {MUSIC_BOT_NAME} 𝙛𝙤𝙧 𝙮𝙤𝙪𝙧 𝙘𝙝𝙖𝙩.."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await Yukki.stop_stream(message.chat.id)
    except:
        pass
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await Yukki.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text(
        "𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡𝙡𝙮 𝙧𝙚𝙨𝙩𝙖𝙧𝙩𝙚𝙙. 𝙏𝙧𝙮 𝙥𝙡𝙖𝙮𝙞𝙣𝙜 𝙣𝙤𝙬.."
    )


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(
    filters.regex("𝙨𝙩𝙤𝙥_𝙙𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜") & ~BANNED_USERS
)
@ActualAdminCB
async def stop_download(client, CallbackQuery: CallbackQuery, _):
    message_id = CallbackQuery.message.message_id
    task = lyrical.get(message_id)
    if not task:
        return await CallbackQuery.answer(
            "𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙.", show_alert=True
        )
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜 𝙖𝙡𝙧𝙚𝙖𝙙𝙮 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚𝙙 𝙤𝙧 𝘾𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙.",  
          show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer(
                "𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜 𝘾𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙", show_alert=True
            )
            return await CallbackQuery.edit_message_text(
                f"𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙 𝘾𝙖𝙣𝙘𝙚𝙡𝙡𝙚𝙙 by {CallbackQuery.from_user.mention}"
            )
        except:
            return await CallbackQuery.answer(
                "𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙨𝙩𝙤𝙥 𝙩𝙝𝙚 𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙𝙞𝙣𝙜.", show_alert=True
            )
    await CallbackQuery.answer(
        "𝙁𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙧𝙚𝙘𝙤𝙜𝙣𝙞𝙯𝙚 𝙩𝙝𝙚 𝙧𝙪𝙣𝙣𝙞𝙣𝙜 𝙩𝙖𝙨𝙠", show_alert=True
    )
