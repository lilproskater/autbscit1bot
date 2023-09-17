from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, bot, dp, is_admin_or_super_admin, get_message_argument, str_is_number, get_group_id


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('reply_forward_group'))
async def reply_forward_group(message: Message):
    await message.reply('Я не знаю такой команды. Ну или почти))')


@dp.message(ChatTypeFilter('private'), Command('reply_forward_group'))
async def reply_forward_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply('Вы не можете пересылать сообщение в группу через бота')
        return
    group_id = get_group_id()
    if not group_id:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        message_id = get_message_argument(message)
        if not message.reply_to_message or not message_id or not str_is_number(message_id):
            await message.reply(
                'Пожалуйста ответьте на сообщение, которое хотите переслать '
                'и параметром напишите число (message_id из группы)'
            )
            return
        if message.reply_to_message.media_group_id:
            await message.reply('Нельзя переслать медиа-группу. Пожалуйста ответьте на сообщение с одним вложением')
            return
        await bot.copy_message(
            group_id,
            from_chat_id=message.chat.id,
            message_id=message.reply_to_message.message_id,
            reply_to_message_id=int(message_id)
        )
        await message.reply('Ответ на сообщение успешно переслан в группу')
    except Exception as _:
        await message.reply(
            'Не удалось ответить на сообщение в группе. '
            'Проверьте права, существование сообщения и бота в группе'
        )
