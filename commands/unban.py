from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.command import Command
from aiogram.types import Message
from time import time
from helper import ChatTypeFilter, bot, dp, sql_exec


@dp.callback_query(ChatTypeFilter('private'), Command('unban'))
async def unban_private(message: Message):
    await message.reply('Данная команда работает только в группе')


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('unban'))
async def unban(message: Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != 'creator':
        await message.reply('Только Сеньор может разбанить пользователей!')
        return
    inline_markup_rows = []
    sql_exec('DELETE FROM banned_users WHERE till_time <= ?', (int(time()),))
    banned_users = sql_exec('SELECT * FROM banned_users')
    if not banned_users:
        await message.reply('Нет забаненных пользователей Сеньор')
        return
    text = 'Забаненные пользователи:\n'
    for banned_user in banned_users:
        inline_markup_rows.append([
            InlineKeyboardButton(text=banned_user.get('name'), callback_data=str(banned_user.get('user_id')))
        ])
        text += f'{banned_user.get("name")}\n'
    inline_markup = InlineKeyboardMarkup(inline_keyboard=inline_markup_rows)
    if not inline_markup.inline_keyboard:
        await bot.send_message(message.chat.id, 'Нет забаненных пользователей Сеньор')
        return
    text += '\nВыберите кого нужно разбанить Сеньор:'
    await bot.send_message(message.chat.id, text, reply_markup=inline_markup)
