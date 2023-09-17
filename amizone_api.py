#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from re import sub as re_sub, search as re_search
from calendar import day_name as week_day_names  # ['Monday', ..., 'Sunday']
from lxml import html


class AmizoneApiSession:
    def __init__(self, amizone_id, password):
        self.amizone_id = amizone_id
        self.password = password
        self.session = requests.Session()
        self.requestVerificationToken = self.session.get('https://s.amizone.net').cookies['__RequestVerificationToken']
        self.aspx_auth = ''

    async def login(self):
        login_token = re_search(
            r'<form action="/" class=" validate-form" id="loginform" method="post" name="loginform">'
            r'<input name="__RequestVerificationToken".{0,20}value=".{0,110}/>',
            self.session.get('https://s.amizone.net').text
        )[0][148:-4]
        self.session.post(
            'https://s.amizone.net',
            headers={
                'Cookie': f'__RequestVerificationToken={self.requestVerificationToken}',
                'Host': 's.amizone.net',
                'Origin': 'https://s.amizone.net',
                'Referer': 'https://s.amizone.net/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
            },
            data={
                '__RequestVerificationToken': login_token,
                '_UserName': self.amizone_id,
                '_QString': '',
                '_Password': self.password,
            }
        )
        try:
            self.aspx_auth = self.session.cookies['.ASPXAUTH']
        except KeyError:
            exit('Could not login to Amizone with provided login and password')

    @staticmethod
    def __parse_time_table__(html_text, day):
        day = day.capitalize()
        if day != 'Week' and day not in week_day_names:
            raise Exception('Given day should be Week or Monday-Sunday')
        days = week_day_names if day == 'Week' else [day]
        tree = html.fromstring(html_text)
        in_ids = ' or '.join([f'contains(@id, "{x}")' for x in days])
        if not tree.xpath(f'//div[{in_ids}]'):
            return None
        parsed = {}
        for day in days:
            parsed[day] = []
            lectures = tree.xpath(f'//div[@id="{day}"]//div[contains(@class, "timetable-box")]')
            if not lectures:
                continue
            lectures_buffer = []
            for lecture in lectures:
                room_no = re_search(r'\d{3}', lecture.find_class('class-loc')[0].text_content())
                lecture_buf = {
                    'code': lecture.find_class('course-code')[0].text_content().replace(' ', ''),
                    'time': lecture.find_class('class-time')[0].text_content().replace(' ', '').replace('to', ' - '),
                    'teacher': re_sub(r'\[[^[]*]', '', lecture.find_class('course-teacher')[0].text_content()),
                    'room': room_no[0] if room_no else 'Unknown Room'
                }
                lectures_buffer.append(lecture_buf)
            parsed[day] = lectures_buffer
        return parsed

    async def get_tt(self, day='Week'):
        if not self.aspx_auth:
            raise Exception('Login to Amizone first')
        response = self.session.get(
            'https://s.amizone.net/TimeTable/Home?X-Requested-With=XMLHttpRequest',
            headers={
                'Cookie': f'__RequestVerificationToken={self.requestVerificationToken};.ASPXAUTH={self.aspx_auth}',
                'Host': 'student.amizone.net',
                'Origin': 'https://student.amizone.net',
                'Referer': 'https://student.amizone.net/Home',
                'X-Requested-With': 'XMLHttpRequest',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
            }
        )
        return AmizoneApiSession.__parse_time_table__(response.text, day)


if __name__ == '__main__':
    print('Unofficial Amizone.net Application Programming Interface')
