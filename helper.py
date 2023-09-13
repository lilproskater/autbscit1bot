from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import BaseFilter
from aiogram.types.chat_permissions import ChatPermissions
from config import BOT_TOKEN
from sqlite3 import connect as sqlite3_connect
from typing import Union


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
restricted_permissions = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False
)


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: Union[str, list]):
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


def sql_exec(sql, args=()):
    db_connection = sqlite3_connect('data.sqlite')
    db_cursor = db_connection.cursor()
    data = db_cursor.execute(sql, args)
    db_connection.commit()
    rows = db_cursor.fetchall()
    columns = [x[0] for x in data.description or []]
    db_cursor.close()
    db_connection.close()
    return [dict(zip(columns, row)) for row in rows] or None
