# -*- coding: utf-8 -*-
import os
import unittest

from selenium import webdriver

from pages import MainPage
from tests.asserts import CustomAssertions


class LoginTest(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.page.logout()
        self.driver.quit()

    def test(self):
        self.page = MainPage(self.driver)
        self.page.open()
        self.page.login(self.LOGIN, self.PASSWORD)

        menu_bar = self.page.menu_bar
        self.assertEqual(menu_bar.email_value, self.LOGIN)


class LogoutTest(unittest.TestCase, CustomAssertions):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = MainPage(self.driver)
        self.page.open()
        self.page.login(self.LOGIN, self.PASSWORD)

    def test(self):
        self.page.logout()
        self.assertElementExists(self.driver, self.page.menu_bar.OPEN_LOGIN_FORM_BUTTON)

    def tearDown(self):
        self.driver.quit()
