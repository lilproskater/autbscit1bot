from lxml import html
from re import sub as r_sub
from requests import get as requests_get
from aiogram.filters.command import Command
from aiogram.types import Message
from helper import dp, t


@dp.message(Command('namaz_today'))
async def namaz_today(message: Message):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0'
    }
    url = 'https://namaz.today/city/tashkent'
    response = requests_get(url, headers=headers)
    tree = html.fromstring(response.text)
    selector = '//div[contains(@class, "subheader") and contains(@class, "text-center")]'
    times = dict(zip(
        [name.text_content() for name in tree.xpath(selector)],
        [ptime.text for ptime in tree.xpath('//span[contains(@class, "text-center") and contains(@class, "rb")]')]
    ))
    selector = '//div[contains(@class, "round") and contains(@class, "active")]' \
               '//div[contains(@class, "time-remaining-content")]'
    remaining_time_to_next = r_sub(' +', ' ', tree.xpath(selector)[0].text_content())
    response_text = t('commands.namaz_today.namaz_times') + ':\n'
    for namaz_name, ptime in times.items():
        response_text += f'{namaz_name}: {ptime}\n'
    response_text += remaining_time_to_next + '\n\n'
    response_text += t('commands.namaz_today.info_taken_from', {'source': url})
    await message.reply(response_text, disable_web_page_preview=True)
