from aiogram.filters.command import Command
from aiogram.types import Message
from helper import dp, sql_exec, is_super_admin, str_is_number, ChatTypeFilter


@dp.message(ChatTypeFilter(chat_type=['private']), Command('set_group'))
async def set_group(message: Message):
    if not is_super_admin(message.chat.id):
        await message.reply('Вы не являетесь супер-админом')
        return
    args = message.split(' ')[1:]
    if not args or not str_is_number(args[0]):
        await message.reply(
            'Неверный параметр команды. Пожалуйста введите ID группы параметром сообщения')
        return
    group_id = args[0]
    response = f'ID группы успешно изменен на {group_id}'
    if not group_id.startsWith('-100'):
        response = f'Запись обновлена на {group_id}, '\
                   'но данное ID группы не начинается на -100. Функции бота для группы могут работать не правильно'
    sql_exec('REPLACE INTO settings(key, value) VALUES(?, ?)', ('GROUP_ID', group_id))  # Works as INSERT OR REPLACE
    await message.reply(response)
