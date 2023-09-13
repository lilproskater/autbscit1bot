from aiogram.filters.command import Command
from aiogram.types import Message
from helper import bot, dp, ChatTypeFilter
from config import ADMINS_ID, GROUP_ID


@dp.message(ChatTypeFilter(chat_type=['private']), Command('reply_forward_group'))
async def reply_forward_group(message: Message):
    if message.chat.id not in ADMINS_ID:
        await message.reply('Вы не можете пересылать сообщение в группу через бота')
        return
    if not GROUP_ID:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        args = [x.strip() for x in message.text.split(' ', 2)][1:]
        if not message.reply_to_message or len(args) < 1:
            await message.reply(
                'Пожалуйста ответьте на сообщение которое хотите переслать и параметром напишите message_id из группы'
            )
            return
        if message.reply_to_message.media_group_id:
            await message.reply('Нельзя переслать медиа-группу. Пожалуйста ответьте на сообщение с одним вложением')
            return
        await bot.copy_message(
            GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id,
            reply_to_message_id=int(args[0])
        )
        await message.reply('Ответ на сообщение успешно переслан в группу')
    except Exception as _:
        await message.reply(
            'Не удалось ответить на сообщение в группе. '
            'Проверьте права, существование сообщения и бота в группе'
        )
