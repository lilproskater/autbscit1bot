from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile
from helper import dp, bot, t


@dp.message(Command('start'))
async def start(message: Message):
    sticker_message = await bot.send_sticker(message.chat.id, FSInputFile('static/welcome_sticker.webp'))
    me = await bot.get_me()
    await bot.send_message(
        message.chat.id,
        t('commands.start.welcome_message_html', {'bot_name': me.first_name}),
        parse_mode='html',
        reply_to_message_id=sticker_message.message_id
    )
