from aiogram.filters.command import Command
from aiogram.types import Message
from helper import bot, dp, ChatTypeFilter
from config import ADMINS_ID, GROUP_ID


@dp.message(ChatTypeFilter(chat_type=['private']), Command('forward_group'))
async def forward_group(message: Message):
    if message.chat.id not in ADMINS_ID:
        await message.reply('Вы не можете пересылать сообщение в группу через бота')
        return
    if not GROUP_ID:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        if not message.reply_to_message:
            await message.reply('Пожалуйста ответьте на сообщение которое хотите переслать')
            return
        if message.reply_to_message.media_group_id:
            await message.reply('Нельзя переслать медиа-группу. Пожалуйста ответьте на сообщение с одним вложением')
            return
        await bot.copy_message(GROUP_ID, from_chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
        await message.reply('Сообщение успешно переслано в группу')
    except Exception as _:
        await message.reply(
            'Не удалось ответить на сообщение в группе. Проверьте права, существование бота в группе'
        )
