from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, sql_exec, str_is_number, is_super_admin, get_message_argument


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('set_admins'))
async def set_admins(message: Message):
    await message.reply('Я не знаю такой команды. Ну или почти))')


@dp.message(ChatTypeFilter('private'), Command('set_admins'))
async def set_admins_private(message: Message):
    if not is_super_admin(message.chat.id):
        await message.reply('Вы не являетесь супер-админом')
        return
    args = get_message_argument(message)
    user_ids = [x.strip() for x in args.split('\n') if x.strip()]
    non_numbers = [x for x in user_ids if not str_is_number(x)]
    user_ids = tuple(set(user_ids))
    if not user_ids or non_numbers:
        await message.reply(
            'Неверные параметры команды. Пожалуйста введите каждый ID пользователя на новой строке\n\n'
            'Пример: /set_admins\n1234567\n1234567\n\n'
            'Примечание: ID пользователей не может быть отрицательным'
        )
        return
    try:
        sql_exec('DELETE FROM admins')
        for admin_id in [int(x) for x in user_ids]:
            sql_exec('INSERT INTO admins(user_id) VALUES(?)', (admin_id,))
        await message.reply('Список админов успешно обновлен!')
    except Exception as _:
        await message.reply('Во время обновления списка админов что-то пошло не так')
