from aiogram.types import CallbackQuery
from time import time
from helper import ChatTypeFilter, dp, bot, t, sql_exec, restricted_permissions


@dp.callback_query(ChatTypeFilter('private'), lambda call: True)
async def unban_callback_query_private(call):
    await bot.answer_callback_query(call.id, show_alert=True, text=t('common.command_only_for_group'))


@dp.callback_query(ChatTypeFilter(chat_type=['group', 'supergroup']), lambda call: True)
async def unban_callback_query(call: CallbackQuery):
    caller = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
    if caller.status != 'creator':
        await bot.answer_callback_query(
            call.id,
            show_alert=True,
            text=t('callback_queries.unban.only_creator_can_unban')
        )
        return
    banned_user = await bot.get_chat_member(call.message.chat.id, int(call.data))
    full_name = f'{banned_user.user.first_name} {banned_user.user.last_name or ""}'.strip()
    if banned_user.status == 'restricted':
        response = t('callback_queries.unban.success', {'name': full_name})
        await bot.restrict_chat_member(
            call.message.chat.id,
            int(call.data),
            restricted_permissions,
            until_date=int(time()) + 31
        )
    else:
        response = t('callback_queries.unban.already_not_banned', {'name': full_name})
    sql_exec('DELETE FROM banned_users WHERE user_id=?', (call.data,))
    await bot.answer_callback_query(call.id, show_alert=True, text=response)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=response,
        reply_markup=None
    )
