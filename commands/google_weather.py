from aiogram.filters.command import Command
from aiogram.types import Message
from lxml import html
from re import search as r_search
from requests import get as requests_get
from json import loads as json_loads
from helper import dp, bot, t, get_message_argument


async def get_google_weather(search='tashkent', lang='ru'):
    headers = {
        'Host': 'www.google.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
    }
    params = {
       'q': f'weather {search.strip().lower()}',
       'hl': lang,  # the language to use for the Google search
    }
    response = requests_get('https://www.google.com/search', headers=headers, params=params)
    pmc = json_loads(r_search(r'var pmc=\'{.*}\';', response.text)[0][9:-2].replace('\\\\', '\\').replace('\\x22', '"'))
    tree = html.fromstring(response.text)
    try:
        location = tree.xpath('//div[@id="wob_loc"]')[0].text
        today = tree.xpath('//div[@id="wob_dts"]')[0].text[:-6].capitalize()
        forecast = tree.xpath('//span[@id="wob_dc"]')[0].text.capitalize()
        img_url = tree.xpath('//img[@id="wob_tci"]')[0].attrib['src'].lstrip('/')
        day_temp = tree.xpath('//div[contains(@class, "gNCp2e")]//span')[0].text + '°'
        night_temp = tree.xpath('//div[contains(@class, "ZXCv8e")]//span')[0].text + '°'
        precipitation = tree.xpath('//span[@id="wob_pp"]')[0].text
        humidity = tree.xpath('//span[@id="wob_hm"]')[0].text
        wind_speed = tree.xpath('//span[@id="wob_ws"]')[0].text
        hourly_w = dict(zip(
            [pmc['wobnm']['wobhl'][x]['dts'].capitalize() for x in range(0, 15, 3)],
            [pmc['wobnm']['wobhl'][x]['tm'] + '°' for x in range(0, 15, 3)])
        )
        result = f'{location} - {today}, {forecast}\n'
        result += t('commands.google_weather.day_temp', {'day_temp': day_temp}) + '\n'
        result += t('commands.google_weather.night_temp', {'night_temp': night_temp}) + '\n\n'
        result += t('commands.google_weather.precipitation', {'precipitation': precipitation}) + '\n'
        result += t('commands.google_weather.humidity', {'humidity': humidity}) + '\n'
        result += t('commands.google_weather.wind_speed', {'wind_speed': wind_speed}) + '\n\n'
        result += t('commands.google_weather.hourly_weather') + ':\n'
        for w_time, temp in hourly_w.items():
            result += ', '.join(w_time.split()) + f' - {temp}\n'
        return img_url, result
    except Exception as _:
        return None, None


@dp.message(Command('google_weather'))
async def google_weather(message: Message):
    city = get_message_argument(message) or 'Tashkent'
    await message.reply(t('commands.google_weather.getting_info', {'city': city}))
    img_url, caption = await get_google_weather(city)
    if not caption:
        await message.reply(t('commands.google_weather.failed'))
        return
    if img_url:
        await bot.send_photo(message.chat.id, img_url, caption=caption, reply_to_message_id=message.message_id)
        return
    await bot.send_message(message.chat.id, caption)
