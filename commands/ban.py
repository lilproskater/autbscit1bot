from aiogram.filters.command import Command
from aiogram.types import Message
from time import time
from helper import ChatTypeFilter, bot, dp, restricted_permissions, sql_exec


@dp.callback_query(ChatTypeFilter('private'), Command('ban'))
async def ban_private(message: Message):
    await message.reply('Данная команда работает только в группе')


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('ban'))
async def ban(message: Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != 'creator':
        await message.reply('Только Сеньор может забанить пользователей!')
        return
    else:
        if not message.reply_to_message:
            await message.reply('Ответьте на сообщение пользователя которого нужно забанить Сеньор')
            return
        elif message.reply_to_message.from_user.id in [user.user.id, bot.id]:
            await message.reply('Вы не можете забанить себя или бота Сеньор')
            return
    ban_user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    full_name = f'{ban_user.user.first_name} {ban_user.user.last_name or ""}'.strip()
    ban_hours = 2
    unix_ban_timeout = int(time()) + ban_hours * 3600
    sql_exec('INSERT INTO banned_users(user_id, name, till_time) VALUES (?, ?, ?)', (
        message.reply_to_message.from_user.id,
        full_name,
        unix_ban_timeout,
    ))
    try:
        await bot.restrict_chat_member(
            message.chat.id,
            ban_user.user.id,
            restricted_permissions,
            until_date=unix_ban_timeout
        )
        await message.reply(f'Пользователь "{full_name}" был забанен на {ban_hours} часа Сеньор!')
    except Exception as _:
        await message.reply('Не удалось забанить пользователя Сеньор')
