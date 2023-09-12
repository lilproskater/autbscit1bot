from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.chat_permissions import ChatPermissions
from config import AMIZONE_ID, AMIZONE_PASSWORD, BOT_TOKEN, ADMINS_ID, GROUP_ID
from aiogram import Bot, Dispatcher, executor, types
from re import sub as r_sub, search as r_search
from AmizoneAPI import amizone_api
from time import time
from lxml import html
from datetime import date
from base64 import decodebytes
from io import BytesIO
import requests
import json


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
restricted_permissions = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False
)


def xstr(x):
    return '' if x is None else x


async def get_google_weather(search='tashkent'):
    headers = {
        'Host': 'www.google.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    params = {
       'q': 'weather ' + search.strip().lower(),
       'hl': 'en',  # the language to use for the Google search
    }
    response = requests.get('https://www.google.com/search', headers=headers, params=params)
    pmc = json.loads(r_search(r'var pmc=\'{.*}\';', response.text)[0][9:-2].replace('\\\\', '\\').replace('\\x22', '"'))
    tree = html.fromstring(response.text)
    # try:
    location = tree.xpath("//div[@id='wob_loc']")[0].text
    today = tree.xpath("//div[@id='wob_dts']")[0].text[:-6].capitalize()
    forecast = tree.xpath("//span[@id='wob_dc']")[0].text.capitalize()
    img_base64 = tree.xpath("//div[contains(@class, 'DxhUm')]//img")[0].attrib['src']
    print(response.text)
    day_temp = tree.xpath("//div[contains(@class, 'gNCp2e')]//span")[0].text + '°'
    night_temp = tree.xpath("//div[contains(@class, 'ZXCv8e')]//span")[0].text + '°'
    precipitation = tree.xpath("//span[@id='wob_pp']")[0].text
    humidity = tree.xpath("//span[@id='wob_hm']")[0].text
    wind_speed = tree.xpath("//span[@id='wob_ws']")[0].text
    hourly_w = dict(zip(
        [pmc['wobnm']['wobhl'][x]['dts'].capitalize() for x in range(0, 15, 3)],
        [pmc['wobnm']['wobhl'][x]['tm'] + '°' for x in range(0, 15, 3)])
    )
    result = location + ' - ' + today + ', ' + forecast + '\n'
    result += 'Day: ' + day_temp + '\n'
    result += 'Night: ' + night_temp + '\n\n'
    result += 'Precipitation: ' + precipitation + '\n'
    result += 'Humidity: ' + humidity + '\n'
    result += 'Wind speed: ' + wind_speed + '\n\n'
    result += 'Hourly weather:\n'
    for w_time, temp in hourly_w.items():
        result += ', '.join(w_time.split(' ')) + ' - ' + temp + '\n'
    return img_base64, result
    # except Exception as _:
    #     return None, None


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    with open('static/welcome_sticker.webp', 'rb') as welcome_sticker:
        sticker_message = await bot.send_sticker(message.chat.id, welcome_sticker)
    me = await bot.get_me()
    await bot.send_message(
        message.chat.id,
        f"Hats off to you, I am slave of <i>Senior sudo</i> – <b>{me.first_name}</b>! What can I do for you?",
        parse_mode="html",
        reply_to_message_id=sticker_message.message_id
    )


@dp.message_handler(commands=['schedule'])
async def schedule(message: types.Message):
    await amizone_api.login(AMIZONE_ID, AMIZONE_PASSWORD)
    args = message.text.split()
    days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if len(args) == 1:
        try:
            await message.reply("Getting schedule from Amizone...")
            response_text = await amizone_api.get_time_table(days_of_the_week[date.today().weekday()])
        except Exception as _:
            response_text = "Couldn't get schedule from Amizone"
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
            await message.reply("Getting schedule from Amizone...")
            response_text = await amizone_api.get_time_table(day)
        except Exception as _:
            response_text = "Couldn't get schedule for " + args[1] + " from Amizone"
    else:
        response_text = "Error in given arguments"
    await message.reply(response_text)


@dp.message_handler(commands=['namaztoday'])
async def namaztoday(message: types.Message):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"
    }
    response = requests.get('https://namaz.today/city/tashkent', headers=headers)
    tree = html.fromstring(response.text)
    selector = "//div[contains(@class, 'subheader') and contains(@class, 'text-center')]"
    times = dict(zip(
        [name.text_content() for name in tree.xpath(selector)],
        [ptime.text for ptime in tree.xpath("//span[contains(@class, 'text-center') and contains(@class, 'rb')]")]
    ))
    selector = "//div[contains(@class, 'round') and contains(@class, 'active')]" \
               "//div[contains(@class, 'time-remaining-content')]"
    remaining_time_to_next = r_sub(' +', ' ', tree.xpath(selector)[0].text_content())
    response_text = "Времена Намаза сегодня в Ташкенте:\n"
    for namaz_name, ptime in times.items():
        response_text += namaz_name + ": " + ptime + "\n"
    response_text += remaining_time_to_next
    response_text += "\n\nИнформация взята с https://namaz.today/city/tashkent"
    await message.reply(response_text, disable_web_page_preview=True)


@dp.message_handler(commands=['googleweather'])
async def googleweather(message: types.Message):
    args = message.text.split()
    if len(args) > 2:
        await message.reply('Error in given arguments')
        return
    city = args[1].strip() + ' ' if len(args) == 2 else ''
    await message.reply('Getting ' + city + 'weather information from Google...')
    city = city.strip()
    img_base64, caption = await get_google_weather(city if city else 'tashkent')
    if not caption:
        await message.reply("Couldn't get weather info from Google")
        return
    if img_base64:
        image = types.InputFile(BytesIO(decodebytes(img_base64.split(',')[1].encode())))
        await bot.send_photo(message.chat.id, image, caption, reply_to_message_id=message.message_id)
        return
    await bot.send_message(message.chat.id, caption)


@dp.message_handler(commands=['ban'])
async def ban(message: types.Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != "creator":
        await message.reply('Only creator Senior can ban users!')
        return
    else:
        if not message.reply_to_message:
            await message.reply('Reply a message from user you want to ban Senior')
            return
        elif message.reply_to_message.from_user.id in [user.user.id, bot.id]:
            await message.reply('Admin cannot ban himself or bot')
            return
    ban_user = await bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    full_name = (ban_user.user.first_name + ' ' + xstr(ban_user.user.last_name)).strip()
    if ban_user.status == "restricted":
        await message.reply('User ' + full_name + ' is already banned')
        return
    ban_hours = 2
    unix_ban_timeout = int(time()) + ban_hours * 3600
    json_data['banned_users'][str(message.reply_to_message.from_user.id)] = {
        "name": full_name,
        "till_time": unix_ban_timeout
    }
    with open('data.json', 'w') as file:
        json.dump(json_data, file, indent=4)
    await bot.restrict_chat_member(message.chat.id,  ban_user.user.id, restricted_permissions, unix_ban_timeout)
    await message.reply('User ' + full_name + ' has been banned for ' + str(ban_hours) + ' hours!')


@dp.message_handler(commands=['unban'])
async def unban(message: types.Message):
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if user.status != "creator":
        await message.reply('Only creator Senior can unban users!')
        return
    inline_markup = InlineKeyboardMarkup(row_width=1)
    text = "Banned users:\n"
    for user_id, user_data in json_data['banned_users'].items():
        if user_data['till_time'] <= int(time()):
            del json_data['banned_users'][user_id]
            continue
        inline_markup.add(InlineKeyboardButton(user_data["name"], callback_data=str(user_id)))
        text += user_data["name"] + "\n"
    with open('data.json', 'w') as file:
        json.dump(json_data, file, indent=4)
    if not inline_markup['inline_keyboard']:
        await bot.send_message(message.chat.id, "No banned users found")
        return
    text += "\nChoose a user to unban Senior:"
    await bot.send_message(message.chat.id, text, reply_markup=inline_markup)


@dp.message_handler(commands=['send_to_group'], chat_type=[types.ChatType.PRIVATE])
async def message_handler(message: types.Message):
    if message.chat.id in ADMINS_ID:
        if GROUP_ID:
            try:
                await bot.send_message(GROUP_ID, message.text.split(' ', 1)[1])
            except Exception as _:
                await bot.send_message(
                    message.chat.id,
                    'Не удалось отправить сообщение в группу. Проверьте права и существование бота в группе'
                )
        else:
            await bot.send_message(message.chat.id, 'У бота нет привязанной группы в конфиге')


@dp.callback_query_handler(lambda call: True)
async def unban_callback_handler(call):
    caller = await bot.get_chat_member(call.message.chat.id, call.from_user.id)
    if caller.status != "creator":
        await bot.answer_callback_query(call.id, show_alert=True, text="Only Senior can choose whom to unban")
        return
    banned_user = await bot.get_chat_member(call.message.chat.id, int(call.data))
    full_name = (banned_user.user.first_name + ' ' + xstr(banned_user.user.last_name)).strip()
    if banned_user.status == "restricted":
        alert_text = "User " + full_name + " will be unbanned in 30 seconds."
        await bot.restrict_chat_member(call.message.chat.id, int(call.data), restricted_permissions, int(time()) + 31)
    else:
        alert_text = "User " + full_name + " is already unbanned"
    if json_data['banned_users'].get(call.data):
        del json_data['banned_users'][call.data]
        with open('data.json', 'w') as file:
            json.dump(json_data, file, indent=4)

    await bot.answer_callback_query(call.id, show_alert=True, text=alert_text)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=alert_text,
        reply_markup=None
    )


if __name__ == '__main__':
    try:
        with open('data.json') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = {"banned_users": {}}
        with open('data.json', 'w') as f:
            json.dump(json_data, f, indent=4)
    try:
        executor.start_polling(dp, skip_updates=True)
    except KeyboardInterrupt:
        print('Goodbye!')
        exit()
