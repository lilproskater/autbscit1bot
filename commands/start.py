from aiogram.filters.command import Command
from aiogram.types import Message, FSInputFile
from helper import bot, dp


@dp.message(Command('start'))
async def start(message: Message):
    sticker_message = await bot.send_sticker(message.chat.id, FSInputFile('static/welcome_sticker.webp'))
    me = await bot.get_me()
    await bot.send_message(
        message.chat.id,
        f'Hats off to you, I am slave of <i>Senior sudo</i> – <b>{me.first_name}</b>! What can I do for you?',
        parse_mode='html',
        reply_to_message_id=sticker_message.message_id
    )
