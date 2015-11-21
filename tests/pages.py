# -*- coding: utf-8 -*-

import urlparse

from components import AuthForm, MenuBar


class Page(object):
    BASE_URL = 'https://cars.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class MainPage(Page):
    @property
    def auth_form(self):
        return AuthForm(self.driver)

    @property
    def menu_bar(self):
        return MenuBar(self.driver)
