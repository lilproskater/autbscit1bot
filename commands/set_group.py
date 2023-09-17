from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, sql_exec, str_is_number, is_super_admin, get_message_argument


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('set_group'))
async def set_group(message: Message):
    await message.reply('Я не знаю такой команды. Ну или почти))')


@dp.message(ChatTypeFilter('private'), Command('set_group'))
async def set_group_private(message: Message):
    if not is_super_admin(message.chat.id):
        await message.reply('Вы не являетесь супер-админом')
        return
    group_id = get_message_argument(message)
    if not group_id or not str_is_number(group_id, True):
        await message.reply(
            'Неверный параметр команды. Пожалуйста введите ID группы параметром сообщения'
        )
        return
    response = f'ID группы успешно изменен на {group_id}'
    if not group_id.startswith('-100'):
        response = f'Запись обновлена на {group_id}, '\
                   'но данное ID группы не начинается на -100. Функции бота для группы могут работать не правильно'
    sql_exec('REPLACE INTO settings(key, value) VALUES(?, ?)', ('GROUP_ID', group_id))  # Works as INSERT OR REPLACE
    await message.reply(response)
