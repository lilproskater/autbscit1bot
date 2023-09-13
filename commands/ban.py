from aiogram.filters.command import Command
from aiogram.types import Message
from time import time
from helper import bot, dp, restricted_permissions, sql_exec


@dp.message(Command('ban'))
async def ban(message: Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != 'creator':
        await message.reply('Only creator Senior can ban users!')
        return
    else:
        if not message.reply_to_message:
            await message.reply('Reply a message from user you want to ban Senior')
            return
        elif message.reply_to_message.from_user.id in [user.user.id, bot.id]:
            await message.reply('Admin cannot ban himself or bot')
            return
    ban_user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    full_name = (ban_user.user.first_name + ' ' + (ban_user.user.last_name or '')).strip()
    if ban_user.status == 'restricted':
        await message.reply('User ' + full_name + ' is already banned')
        return
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
        await message.reply('User ' + full_name + ' has been banned for ' + str(ban_hours) + ' hours!')
    except Exception as _:
        await message.reply('Couldn\'t ban user')
