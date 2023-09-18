from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from aiogram.types.chat_permissions import ChatPermissions
from config import BOT_TOKEN
from sqlite3 import connect as sqlite3_connect
from re import sub as re_sub
from typing import Union
from lang import t_dictionary


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

    async def __call__(self, message_or_call: Message | CallbackQuery) -> bool:
        message = message_or_call if isinstance(message_or_call, Message) else message_or_call.message
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


def get_message_argument(message: Message):
    return re_sub(r'^/[A-z@\d]+', '', message.text).strip()  # Removes the command and returns argument


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


def str_is_number(data_str, check_negatives=False):
    result = str.isdigit(data_str)
    if check_negatives:
        result = result or data_str.startswith('-') and str.isdigit(data_str[1:])
    return bool(result)


def is_admin(chat_id):
    return bool(sql_exec('SELECT * FROM admins WHERE user_id=?', (chat_id,)))


def is_super_admin(chat_id):
    return bool(sql_exec('SELECT * FROM settings WHERE key=? and value=?', ('SUPER_ADMIN_ID', chat_id)))


def is_admin_or_super_admin(chat_id):
    return is_admin(chat_id) or is_super_admin(chat_id)


def get_group_id():
    v = sql_exec('SELECT value FROM settings WHERE key=?', ('GROUP_ID',)) or []
    return v[0].get('value') if len(v) else None


def t(key: str, replace: dict = None, locale: str = 'ru') -> str:
    replace = replace or {}
    lang = t_dictionary.get(locale)
    if not lang:
        return key
    c_depth = lang
    for k in key.split('.'):
        value = c_depth.get(k)
        if not value:  # None or empty
            return key
        if isinstance(value, str):  # Match found
            for rep_k, rep_v in replace.items():
                value = value.replace('{' + str(rep_k) + '}', str(rep_v))
            return value
        c_depth = value
    return key
