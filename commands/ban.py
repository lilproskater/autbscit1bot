from aiogram.filters.command import Command
from aiogram.types import Message
from time import time
from helper import ChatTypeFilter, dp, bot, t, sql_exec, restricted_permissions


@dp.message(ChatTypeFilter('private'), Command('ban'))
async def ban_private(message: Message):
    await message.reply(t('common.command_only_for_group'))


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('ban'))
async def ban(message: Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != 'creator':
        await message.reply(t('commands.ban.only_creator_can_ban'))
        return
    else:
        if not message.reply_to_message:
            await message.reply(t('commands.ban.reply_to_message'))
            return
        elif message.reply_to_message.from_user.id in [user.user.id, bot.id]:
            await message.reply(t('commands.ban.cannot_ban_bot_or_yourself'))
            return
    user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    ban_hours, full_name = 2, f'{user.user.first_name} {user.user.last_name or ""}'.strip()
    unix_ban_timeout = int(time()) + ban_hours * 3600
    sql_exec('INSERT INTO banned_users(user_id, name, till_time) VALUES (?, ?, ?)', (
        message.reply_to_message.from_user.id,
        full_name,
        unix_ban_timeout,
    ))
    try:
        await bot.restrict_chat_member(
            message.chat.id,
            user.user.id,
            restricted_permissions,
            until_date=unix_ban_timeout
        )
        await message.reply(t('commands.ban.success', {
            'name': full_name,
            'hours': ban_hours,
        }))
    except Exception as _:
        await message.reply(t('commands.ban.failed'))
