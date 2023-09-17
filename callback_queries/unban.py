from aiogram.types import CallbackQuery
from time import time
from helper import ChatTypeFilter, bot, dp, restricted_permissions, sql_exec


@dp.callback_query(ChatTypeFilter('private'), lambda call: True)
async def unban_callback_query_private(call):
    await bot.answer_callback_query(call.id, show_alert=True, text='Данная команда работает только в группе')


@dp.callback_query(ChatTypeFilter(chat_type=['group', 'supergroup']), lambda call: True)
async def unban_callback_query(call: CallbackQuery):
    caller = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
    if caller.status != 'creator':
        await bot.answer_callback_query(call.id, show_alert=True, text='Только Сеньор может выбирать кого разбанить!')
        return
    banned_user = await bot.get_chat_member(call.message.chat.id, int(call.data))
    full_name = f'{banned_user.user.first_name} {banned_user.user.last_name or ""}'.strip()
    if banned_user.status == 'restricted':
        alert_text = f'Пользователь "{full_name}" будет разбанен через 30 секунд Сеньор'
        await bot.restrict_chat_member(
            call.message.chat.id,
            int(call.data),
            restricted_permissions,
            until_date=int(time()) + 31
        )
    else:
        alert_text = f'У пользователя "{full_name}" и так нет бана Сеньор'
    sql_exec('DELETE FROM banned_users WHERE user_id=?', (call.data,))
    await bot.answer_callback_query(call.id, show_alert=True, text=alert_text)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=alert_text,
        reply_markup=None
    )
