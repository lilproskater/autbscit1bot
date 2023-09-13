#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from re import sub as re_sub, search as re_search
from lxml import html


Session = requests.Session()
COOKIE_requestVerificationToken = Session.get('https://s.amizone.net').cookies['__RequestVerificationToken']
ASPXAUTH = ''
__version__ = '0.1 beta'


async def login(amizone_id, password):
    global ASPXAUTH
    login_token = re_search(r'<form action="/" class=" validate-form" id="loginform" method="post" name="loginform">'
                            r'<input name="__RequestVerificationToken".{0,20}value=".{0,110}/>',
                            Session.get('https://s.amizone.net').text)[0][148:-4]
    headers = {
        'Cookie': '__RequestVerificationToken=' + COOKIE_requestVerificationToken,
        'Host': 's.amizone.net',
        'Origin': 'https://s.amizone.net',
        'Referer': 'https://s.amizone.net/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    }
    form_data = {
        '__RequestVerificationToken': login_token,
        '_UserName': amizone_id,
        '_QString': '',
        '_Password': password,
    }
    Session.post('https://s.amizone.net', headers=headers, data=form_data)
    try:
        ASPXAUTH = Session.cookies['.ASPXAUTH']
    except KeyError:
        exit('Could not login to Amizone with provided login and password')


async def get_time_table(day=''):
    if not ASPXAUTH:
        raise Exception('Login to Amizone first')

    def parse_time_table(html_text):
        nonlocal day
        day = day.capitalize()
        days_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if day and day not in days_of_the_week:
            return 'Given day should be in range of Monday-Sunday (Mon-Sun)'
        days_to_parse = days_of_the_week if not day else [day]
        tree = html.fromstring(html_text)
        if not tree.xpath('//div[' + ' or '.join(['contains(@id, "' + x + '")' for x in days_to_parse]) + ']'):
            return 'Time-table not set'.title()
        res = ''
        one_day_parse = len(days_to_parse) == 1
        for day in days_to_parse:
            res += (day.upper() + ' time-table'.title()).strip() + '\n\n'
            lectures = tree.xpath('//div[@id="' + day + '"]//div[contains(@class, "timetable-box")]')
            if not lectures:
                res += 'Time-table not set'.title() + '\n'
            course_names = {
                'CSIT136': '🌐 Internet of Things',
                'IT305': '📱 Mobile App Development',
                'CSIT322': '🖼 Image Processing',
                'CSIT311': '🐧 UNIX OS & Shell',
                'CSIT342': '🛠 Software Testing',
                'PFE301': '🗣 Professional Ethics',
            }
            for lecture in lectures:
                res += lecture.find_class('class-time')[0].text_content().replace(' ', '').replace('to', ' - ') + '\n'
                course_code = lecture.find_class('course-code')[0].text_content().replace(' ', '')
                course_name = course_names.get(course_code)
                res += (course_name if course_name else 'Unknown Course') + ' - ' + course_code + '\n'
                res += re_sub(r'\[[^[]*]', '', lecture.find_class('course-teacher')[0].text_content()) + '\n'
                room_number = re_search(r'\d{3}', lecture.find_class('class-loc')[0].text_content())
                room_number = room_number[0] if room_number else 'Unknown Room'
                res += 'Room: ' + room_number + '\n'
                res += '_' * 20 + '\n' * 2 if one_day_parse else "\n"
            res += '\n' if one_day_parse else '_' * 20 + '\n' * 2
        return res

    headers = {
        'Cookie': '__RequestVerificationToken=' + COOKIE_requestVerificationToken + ';.ASPXAUTH=' + ASPXAUTH,
        'Host': 'student.amizone.net',
        'Origin': 'https://student.amizone.net',
        'Referer': 'https://student.amizone.net/Home',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
    }
    response = Session.get('https://s.amizone.net/TimeTable/Home?X-Requested-With=XMLHttpRequest', headers=headers)
    return parse_time_table(response.text)


if __name__ == '__main__':
    print('Unofficial Amizone.net Application Programming Interface')
    print('Version:', __version__)
