#!/usr/bin/python3
from commands import *
from callback_queries import *
from helper import dp, bot, sql_exec
from sys import argv
from seeders import db_seed
from os import remove as os_remove
from os.path import isfile as file_exists
import asyncio


async def start_polling(skip_updates):
    if skip_updates:
        await bot.delete_webhook()
    await dp.start_polling(bot)


def create_db_schema():
    sql_exec('''CREATE TABLE IF NOT EXISTS settings (
        key VARCHAR(255) PRIMARY KEY,
        value VARCHAR(255)
    );''')
    sql_exec('''CREATE TABLE IF NOT EXISTS admins (
        user_id UNSIGNED BIG INT PRIMARY KEY
    );''')
    sql_exec('''CREATE TABLE IF NOT EXISTS banned_users (
        user_id UNSIGNED BIG INT PRIMARY KEY,
        name VARCHAR(255),
        till_time UNSIGNED BIG INT
     );''')
    sql_exec('''CREATE TABLE IF NOT EXISTS subjects (
        code VARCHAR(255) PRIMARY KEY,
        name VARCHAR(255)
    );''')


def ask_and_remove_db():
    ans = input('Do you want to wipe all existing data in DB and recreate schema with DB seeds? (Y/N) ')
    if ans.capitalize() != 'Y':
        return False
    db_fpath = 'data.sqlite'
    if file_exists(db_fpath):
        os_remove(db_fpath)
        return True
    return True


if __name__ == '__main__':
    create_db_schema()  # Create in case db does not exist
    args = argv[1:]
    if len(args):
        if len(args) > 1:
            print('Only one argument can be passed. See --help')
            exit(1)
        arg = args[0]
        if arg == '--help':
            print(f'Usage: {argv[0]} [argument]')
            print('Arguments:')
            print('  --db-seed: Keep existing data in DB and seed to DB (will inform what went wrong in case)')
            print('  --fresh-db: Remove all existing data in DB and recreate schema witout DB seed')
            print('  --fresh-db-seed: Remove all existing data in DB and recreate schema with DB seed')
            print('Note: if no argument has been provided bot will run in polling mode')
            exit()
        elif arg == '--fresh-db':
            if not ask_and_remove_db():
                print('Cancelled!')
                exit()
            create_db_schema()
            print('Recreated new DB file!')
            exit()
        elif arg == '--db-seed':
            db_seed()
            exit()
        elif arg == '--fresh-db-seed':
            if not ask_and_remove_db():
                print('Cancelled!')
                exit()
            create_db_schema()
            db_seed()
            print('Recreated new DB file with DB seeds!')
            exit()
        else:
            print(f'Unknown argument {arg} provided. See --help')
            exit(1)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_polling(skip_updates=False))
    except KeyboardInterrupt:
        print('Goodbye!')
        exit()
