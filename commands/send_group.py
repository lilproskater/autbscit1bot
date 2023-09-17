from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, bot, dp, is_admin_or_super_admin, get_message_argument
from config import GROUP_ID


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('send_group'))
async def send_group(message: Message):
    await message.reply('Я не знаю такой команды. Ну или почти))')


@dp.message(ChatTypeFilter('private'), Command('send_group'))
async def send_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply('Вы не можете отправлять сообщение в группу через бота')
        return
    if not GROUP_ID:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        text = get_message_argument(message)
        if not text:
            await message.reply('Пожалуйста введите аргументом текст, который вы хотите отправить в группу')
            return
        await bot.send_message(GROUP_ID, text)
        await message.reply('Сообщение успешно отправлено в группу')
    except Exception as _:
        await message.reply('Не удалось отправить сообщение в группу. Проверьте права и существование бота в группе')
