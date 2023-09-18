from aiogram.filters.command import Command
from aiogram.types import Message
from helper import ChatTypeFilter, dp, t, is_super_admin, sql_exec, get_message_argument


@dp.message(ChatTypeFilter(chat_type=['group', 'supergroup']), Command('set_subjects'))
async def set_subjects(message: Message):
    await message.reply(t('common.command_only_for_private'))


@dp.message(ChatTypeFilter('private'), Command('set_subjects'))
async def set_subjects_private(message: Message):
    if not is_super_admin(message.chat.id):
        await message.reply(t('common.you_are_not_super_admin'))
        return
    args = get_message_argument(message)
    subjects = [x.strip() for x in args.split('\n') if x.strip()]
    if not len(subjects):
        await message.reply(t('commands.set_subjects.arg_error'))
        return
    subjects_data = {}
    for subject in subjects:
        split = [x.strip() for x in subject.split('-', 1) if x.strip()]
        if len(split) == 1:
            await message.reply(t('commands.set_subjects.arg_error'))
            return
        course_code, course_name = split
        ccu = course_code.upper()
        if ccu in subjects_data:
            await message.reply(t('commands.set_subjects.course_code_duplicate', {'course_code': ccu}))
            return
        subjects_data[ccu] = course_name
    try:
        sql_exec('DELETE FROM subjects')
        for code, name in subjects_data.items():
            sql_exec('INSERT INTO subjects(code, name) VALUES(?, ?)', (code, name))
        await message.reply(t('commands.set_subjects.success'))
    except Exception as _:
        await message.reply(t('commands.set_subjects.failed'))
