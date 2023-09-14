from aiogram.filters.command import Command
from aiogram.types import Message
from helper import bot, dp, ChatTypeFilter, is_admin_or_super_admin
from config import GROUP_ID


@dp.message(ChatTypeFilter(chat_type=['private']), Command('send_group'))
async def send_group(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply('Вы не можете отправлять сообщение в группу через бота')
        return
    if not GROUP_ID:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        await bot.send_message(GROUP_ID, message.text.split(' ', 1)[1])
        await message.reply('Сообщение успешно отправлено в группу')
    except Exception as _:
        await message.reply('Не удалось отправить сообщение в группу. Проверьте права и существование бота в группе')
