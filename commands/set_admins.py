from aiogram.filters.command import Command
from aiogram.types import Message
from helper import dp, sql_exec, is_super_admin, str_is_number, ChatTypeFilter


@dp.message(ChatTypeFilter(chat_type=['private']), Command('set_admins'))
async def set_admins(message: Message):
    if not is_super_admin(message.chat.id):
        await message.reply('Вы не являетесь супер-админом')
        return
    args = ' '.join(message.split(' ')[1:])
    user_ids = [x.strip() for x in args.split('\n') if x.strip()]
    non_numbers = [x for x in user_ids if not str_is_number(x, True)]  # Check only positive or 0 values
    if not user_ids or non_numbers:
        await message.reply(
            'Неверные параметры команды. Пожалуйста введите каждый ID пользователя на новой строке\n\n'
            'Пример: /set_admins\n1234567\n1234567\n\n'
            'Примечание: ID пользователей не может быть отрицательным'
        )
        return
    sql_exec('DELETE * FROM admins')
    for admin_id in [int(x) for x in user_ids]:
        sql_exec('INSERT INTO admins(user_id) VALUES(?)', (admin_id,))
    await message.reply('Список админов успешно обновлен!')
