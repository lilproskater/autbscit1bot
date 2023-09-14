from aiogram.filters.command import Command
from aiogram.types import Message
from helper import dp
from datetime import date
from amizone_api import AmizoneApiSession
from calendar import day_name as calendar_day_name  # ['Monday', ..., 'Sunday']
from config import AMIZONE_ID, AMIZONE_PASSWORD


def normalize_day(day):  # Returns 'Week' or string Monday-Sunday
    day = day.capitalize()
    if day == 'Week':
        return day
    if day in ['Tom', 'Tomorrow']:
        return calendar_day_name[(date.today().weekday() + 1) % 7]
    # Check for weekdays (Mon-Sun or Monday-Sunday)
    short_day_names = [x[:3] for x in calendar_day_name]  # ['Mon', ..., 'Sun']
    if day in (*calendar_day_name, *short_day_names):
        return [x for x in calendar_day_name if x[:3] == day[:3]][0]
    return None


@dp.message(Command('schedule'))
async def schedule(message: Message):
    day = f'{message.text} '.split(' ', 1)[1].capitalize()
    day = normalize_day(calendar_day_name[date.today().weekday()] if not day else day.strip())
    if not day:
        await message.reply('Ошибка: Параметр должен быть задан как [Week, Tom (Tomorrow) или Mon-Sun (Monday-Sunday)]')
        return
    try:
        await message.reply('Получаю расписание из Amizone...')
        session = AmizoneApiSession(AMIZONE_ID, AMIZONE_PASSWORD)
        await session.login()
        # TODO: Redo parsing for AmizoneApiSession.get_tt. See TODO.txt
        await message.reply(await session.get_tt(day))
    except Exception as _:
        await message.reply(f'Не удалось получить расписание из Amizone')
