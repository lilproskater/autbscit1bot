from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, bot, t, is_admin_or_super_admin, get_group_id
from helper import get_message_argument, str_is_number


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('reply_group'))
async def reply_group(message: Message):
    await message.reply(t('common.command_only_for_private'))


@dp.message(ChatTypeFilter('private'), Command('reply_group'))
async def reply_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply(t('common.you_cant_send_message_to_group'))
        return
    group_id = get_group_id()
    if not group_id:
        await message.reply(t('common.no_group'))
        return
    try:
        args = get_message_argument(message).split(maxsplit=1)
        if len(args) < 2:
            await message.reply(t('commands.reply_group.arg_error'))
            return
        message_id, text = args
        if not str_is_number(message_id):
            await message.reply(t('commands.reply_group.first_arg_as_int'))
            return
        await bot.send_message(group_id, text, reply_to_message_id=int(message_id))
        await message.reply(t('commands.reply_group.success'))
    except Exception as _:
        await message.reply(t('commands.reply_group.failed'))
