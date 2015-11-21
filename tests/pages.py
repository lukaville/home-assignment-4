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

    def __init__(self, driver):
        super(MainPage, self).__init__(driver)
        self.auth_form = AuthForm(driver)
        self.menu_bar = MenuBar(driver)

    def login(self, login, password):
        self.menu_bar.open_login_form()
        self.auth_form.wait_until_form_is_loaded()
        self.auth_form.set_login(login)
        self.auth_form.set_password(password)
        self.auth_form.submit()

    def logout(self):
        self.menu_bar.logout()
