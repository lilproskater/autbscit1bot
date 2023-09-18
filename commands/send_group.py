from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, bot, t, is_admin_or_super_admin, get_group_id, get_message_argument


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('send_group'))
async def send_group(message: Message):
    await message.reply(t('common.command_only_for_private'))


@dp.message(ChatTypeFilter('private'), Command('send_group'))
async def send_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply(t('common.you_cant_send_message_to_group'))
        return
    group_id = get_group_id()
    if not group_id:
        await message.reply(t('common.no_group'))
        return
    try:
        text = get_message_argument(message)
        if not text:
            await message.reply(t('commands.send_group.arg_error'))
            return
        await bot.send_message(group_id, text)
        await message.reply(t('commands.send_group.success'))
    except Exception as _:
        await message.reply(t('commands.send_group.failed'))
