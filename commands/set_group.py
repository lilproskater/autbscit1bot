from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, t, is_super_admin, sql_exec, get_message_argument, str_is_number


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('set_group'))
async def set_group(message: Message):
    await message.reply(t('common.command_only_for_private'))


@dp.message(ChatTypeFilter('private'), Command('set_group'))
async def set_group_private(message: Message):
    if not is_super_admin(message.chat.id):
        await message.reply(t('common.you_are_not_super_admin'))
        return
    group_id = get_message_argument(message)
    if not group_id or not str_is_number(group_id, True):
        await message.reply(t('commands.set_group.arg_error'))
        return
    t_key = 'commands.set_group.success'
    t_key += '_with_warning' if not group_id.startswith('-100') else ''
    try:
        sql_exec('REPLACE INTO settings(key, value) VALUES(?, ?)', ('GROUP_ID', group_id))  # Works as INSERT OR REPLACE
        await message.reply(t(t_key, {'group_id': group_id}))
    except Exception as _:
        await message.reply(t('commands.set_group.failed'))
