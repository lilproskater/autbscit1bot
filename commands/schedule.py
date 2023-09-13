from aiogram.filters.command import Command
from aiogram.types import Message
from helper import dp
from datetime import date
from AmizoneAPI import amizone_api
from config import AMIZONE_ID, AMIZONE_PASSWORD


@dp.message(Command('schedule'))
async def schedule(message: Message):
    await amizone_api.login(AMIZONE_ID, AMIZONE_PASSWORD)
    args = message.text.split()
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if len(args) == 1:
        try:
            await message.reply('Getting schedule from Amizone...')
            response_text = await amizone_api.get_time_table(days_of_the_week[date.today().weekday()])
        except Exception as _:
            response_text = 'Couldn\'t get schedule from Amizone'
    elif len(args) == 2:
        day = args[1].capitalize()
        try:
            if day == 'Week':
                day = ''
            elif day in ['Tom', 'Tomorrow']:
                day = days_of_the_week[(date.today().weekday() + 1) % 7]
            else:
                day = [x for x in days_of_the_week if x[:3] == args[1] or x == args[1]]
                if not day:
                    await message.reply('Error: Argument 1 should be [Week, Tom (Tomorrow) or Mon-Sun (Monday-Sunday)]')
                    return
                day = args[1][0]
            await message.reply('Getting schedule from Amizone...')
            response_text = await amizone_api.get_time_table(day)
        except Exception as _:
            response_text = 'Couldn\'t get schedule for ' + args[1] + ' from Amizone'
    else:
        response_text = 'Error in given arguments'
    await message.reply(response_text)
