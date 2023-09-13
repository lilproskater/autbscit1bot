from commands import *
from callback_queries import *
from helper import dp, bot, sql_exec
import asyncio


async def start_polling(skip_updates):
    if skip_updates:
        await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == '__main__':
    sql_exec('''CREATE TABLE IF NOT EXISTS banned_users (
        user_id UNSIGNED BIG INT PRIMARY KEY,
        name VARCHAR(255),
        till_time UNSIGNED BIG INT
     );''')
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_polling(skip_updates=False))
    except KeyboardInterrupt:
        print('Goodbye!')
        exit()
