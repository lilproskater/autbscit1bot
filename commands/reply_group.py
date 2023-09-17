from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, bot, dp, is_admin_or_super_admin, get_message_argument, str_is_number, get_group_id


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('reply_group'))
async def reply_group(message: Message):
    await message.reply('Я не знаю такой команды. Ну или почти))')


@dp.message(ChatTypeFilter('private'), Command('reply_group'))
async def reply_group_private(message: Message):
    if not is_admin_or_super_admin(message.chat.id):
        await message.reply('Вы не можете отвечать на сообщение в группе через бота')
        return
    group_id = get_group_id()
    if not group_id:
        await message.reply('У бота нет привязанной группы в конфиге')
        return
    try:
        args = get_message_argument(message).split(maxsplit=1)
        if len(args) < 2:
            await message.reply('Пожалуйста отправьте первым параметром число (message_id из группы), а потом текст')
            return
        message_id, text = args
        if not str_is_number(message_id):
            await message.reply('Первый параметр message_id должен быть задан числом')
            return
        await bot.send_message(group_id, text, reply_to_message_id=int(message_id))
        await message.reply('Ответ на сообщение успешно отправлен в группу')
    except Exception as _:
        await message.reply(
            'Не удалось ответить на сообщение в группе. Проверьте права, существование сообщения и бота в группе'
        )
