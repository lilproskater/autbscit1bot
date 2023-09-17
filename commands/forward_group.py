from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, bot, dp, is_admin_or_super_admin, get_group_id


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('forward_group'))
async def forward_group(message: Message):
    await message.reply('Я не знаю такой команды. Ну или почти))')


@dp.message(ChatTypeFilter('private'), Command('forward_group'))
async def forward_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply('Вы не можете пересылать сообщение в группу через бота')
        return
    group_id = get_group_id()
    if not group_id:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        if not message.reply_to_message:
            await message.reply('Пожалуйста ответьте на сообщение которое хотите переслать')
            return
        if message.reply_to_message.media_group_id:
            await message.reply('Нельзя переслать медиа-группу. Пожалуйста ответьте на сообщение с одним вложением')
            return
        await bot.copy_message(group_id, from_chat_id=message.chat.id, message_id=message.reply_to_message.message_id)
        await message.reply('Сообщение успешно переслано в группу')
    except Exception as _:
        await message.reply(
            'Не удалось ответить на сообщение в группе. Проверьте права, существование бота в группе'
        )
