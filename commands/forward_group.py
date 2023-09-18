from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, bot, t, is_admin_or_super_admin, get_group_id


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('forward_group'))
async def forward_group(message: Message):
    await message.reply(t('common.command_only_for_private'))


@dp.message(ChatTypeFilter('private'), Command('forward_group'))
async def forward_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply(t('common.you_cant_send_message_to_group'))
        return
    group_id = get_group_id()
    if not group_id:
        await message.reply(t('common.no_group'))
        return
    try:
        if not message.reply_to_message:
            await message.reply(t('commands.forward_group.reply_to_message'))
            return
        if message.reply_to_message.media_group_id:
            await message.reply(t('commands.forward_group.media_group_error'))
            return
        await bot.copy_message(group_id, from_chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
        await message.reply(t('commands.forward_group.success'))
    except Exception as _:
        await message.reply(t('commands.forward_group.failed'))
