#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import sys

from pyrogram import Client

import config

from ..logging import LOGGER


class YukkiBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"𝙎𝙩𝙖𝙧𝙩𝙞𝙣𝙜 𝘽𝙤𝙩")
        super().__init__(
            "YukkiMusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        try:
            await self.send_message(
                config.LOG_GROUP_ID, "𝘽𝙤𝙩 𝙎𝙩𝙖𝙧𝙩𝙚𝙙"
            )
        except:
            LOGGER(__name__).error(
                "𝘽𝙤𝙩 𝙝𝙖𝙨 𝙛𝙖𝙞𝙡𝙚𝙙 𝙩𝙤 𝙖𝙘𝙘𝙚𝙨𝙨 𝙩𝙝𝙚 𝙡𝙤𝙜 𝙂𝙧𝙤𝙪𝙥. 𝙈𝙖𝙠𝙚 𝙨𝙪𝙧𝙚 𝙩𝙝𝙖𝙩 𝙮𝙤𝙪 𝙝𝙖𝙫𝙚 𝙖𝙙𝙙𝙚𝙙 𝙮𝙤𝙪𝙧 𝙗𝙤𝙩 𝙩𝙤 𝙮𝙤𝙪𝙧 𝙡𝙤𝙜 𝙘𝙝𝙖𝙣𝙣𝙚𝙡 𝙖𝙣𝙙 𝙥𝙧𝙤𝙢𝙤𝙩𝙚𝙙 𝙖𝙨 𝙖𝙙𝙢𝙞𝙣!"
            )
            sys.exit()
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != "administrator":
            LOGGER(__name__).error(
                "𝙋𝙡𝙚𝙖𝙨𝙚 𝙥𝙧𝙤𝙢𝙤𝙩𝙚 𝘽𝙤𝙩 𝙖𝙨 𝘼𝙙𝙢𝙞𝙣 𝙞𝙣 𝙇𝙤𝙜𝙜𝙚𝙧 𝙂𝙧𝙤𝙪𝙥"
            )
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"𝙈𝙪𝙨𝙞𝙘𝘽𝙤𝙩 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝙖𝙨 {self.name}")
