from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, bot, dp, is_admin_or_super_admin
from config import GROUP_ID


@dp.message(ChatTypeFilter(chat_type=['private']), Command('reply_group'))
async def reply_group(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply('Вы не можете отвечать на сообщение в группе через бота')
        return
    if not GROUP_ID:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        args = [x.strip() for x in message.text.split(' ', 2)][1:]
        if len(args) < 2:
            await message.reply('Пожалуйста отправьте первым параметром message_id, а потом текст')
            return
        message_id, text = args
        await bot.send_message(GROUP_ID, text, reply_to_message_id=int(message_id))
        await message.reply('Ответ на сообщение успешно отправлен в группу')
    except Exception as _:
        await message.reply(
            'Не удалось ответить на сообщение в группе. Проверьте права, существование сообщения и бота в группе'
        )
