from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, bot, t, is_admin_or_super_admin, get_group_id
from helper import get_message_argument, str_is_number


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('reply_forward_group'))
async def reply_forward_group(message: Message):
    await message.reply(t('common.command_only_for_private'))


@dp.message(ChatTypeFilter('private'), Command('reply_forward_group'))
async def reply_forward_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply(t('common.you_cant_send_message_to_group'))
        return
    group_id = get_group_id()
    if not group_id:
        await message.reply(t('common.no_group'))
        return
    try:
        message_id = get_message_argument(message)
        if not message.reply_to_message or not message_id or not str_is_number(message_id):
            await message.reply(t('commands.reply_forward_group.reply_to_message'))
            return
        if message.reply_to_message.media_group_id:
            await message.reply(t('commands.reply_forward_group.media_group_error'))
            return
        await bot.copy_message(
            group_id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id,
            reply_to_message_id=int(message_id)
        )
        await message.reply(t('commands.reply_forward_group.success'))
    except Exception as _:
        await message.reply(t('commands.reply_forward_group.failed'))
