from aiogram.filters.command import Command
from aiogram.types import Message
from helper import dp
from datetime import date
from amizone_api import AmizoneApiSession, week_day_names
from helper import get_message_argument
from config import AMIZONE_ID, AMIZONE_PASSWORD


def normalize_day(day):  # Returns 'Week' or 'Monday' - 'Sunday'
    day = day.capitalize()
    if day == 'Week':
        return day
    if day in ['Tom', 'Tomorrow']:
        return week_day_names[(date.today().weekday() + 1) % 7]
    # Check for weekdays (Monday-Sunday or Mon-Sun)
    short_day_names = (x[:3] for x in week_day_names)  # ('Mon', ..., 'Sun')
    if day in (*week_day_names, *short_day_names):
        return [x for x in week_day_names if x[:3] == day[:3]][0]
    return None


def get_course_name_by_code(code):
    if not code:
        return 'Unknown Course'
    # TODO: Remake below into DB sql_exec
    return {
        'CSIT136': '🌐 Internet of Things',
        'IT305': '📱 Mobile App Development',
        'CSIT322': '🖼 Image Processing',
        'CSIT311': '🐧 UNIX OS & Shell',
        'CSIT342': '🛠 Software Testing',
        'PFE301': '🗣 Professional Ethics',
    }.get(code) or 'Unknown Course'


def tt2text(time_table):
    result, one_day = '', len(time_table.keys()) == 1
    delim = '_' * 20
    for day, lectures in time_table.items():
        result += f'{day.upper()} Time-Table\n\n'
        if not lectures:
            result += f'Time-Table Not Set\n'
        for lecture in lectures:
            result += f'{lecture.get("time") or "Unknown Time"}\n'
            code = lecture.get('code') or ''
            result += f'{get_course_name_by_code(code)} - {code or "Unknown Code"}\n'
            result += f'{lecture.get("teacher") or "Unknown Teacher"}\n'
            result += f'Room: {lecture.get("room") or "Unknown Room"}\n'
            result += delim + '\n' * (2 if one_day else 1)
        result += '\n' if one_day else delim + '\n' * 2
    return result


@dp.message(Command('schedule'))
async def schedule(message: Message):
    day = get_message_argument(message).capitalize()
    day = normalize_day(day or week_day_names[date.today().weekday()])
    if not day:
        await message.reply('Ошибка: Параметр должен быть задан как [Week, Tom (Tomorrow) или Mon-Sun (Monday-Sunday)]')
        return
    try:
        await message.reply('Получаю расписание из Amizone...')
        session = AmizoneApiSession(AMIZONE_ID, AMIZONE_PASSWORD)
        await session.login()
        time_table = await session.get_tt(day)
        if not time_table:
            await message.reply('Расписание не вышло')
            return
        await message.reply(tt2text(time_table))
    except Exception as _:
        await message.reply(f'Не удалось получить расписание из Amizone')
