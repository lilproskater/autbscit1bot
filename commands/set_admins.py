from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, t, is_super_admin, sql_exec, get_message_argument, str_is_number


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('set_admins'))
async def set_admins(message: Message):
    await message.reply(t('common.command_only_for_private'))


@dp.message(ChatTypeFilter('private'), Command('set_admins'))
async def set_admins_private(message: Message):
    if not is_super_admin(message.chat.id):
        await message.reply(t('common.you_are_not_super_admin'))
        return
    args = get_message_argument(message)
    user_ids = [x.strip() for x in args.split('\n') if x.strip()]
    non_numbers = [x for x in user_ids if not str_is_number(x)]
    user_ids = tuple(set(user_ids))
    if not user_ids or non_numbers:
        await message.reply(t('commands.set_admins.arg_error'))
        return
    try:
        sql_exec('DELETE FROM admins')
        for admin_id in [int(x) for x in user_ids]:
            sql_exec('INSERT INTO admins(user_id) VALUES(?)', (admin_id,))
        await message.reply(t('commands.set_admins.success'))
    except Exception as _:
        await message.reply(t('commands.set_admins.failed'))
