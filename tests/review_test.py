# -*- coding: utf-8 -*-
import os
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from pages import MainPage


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


class LogoutTest(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = MainPage(self.driver)
        self.page.open()
        self.page.login(self.LOGIN, self.PASSWORD)

    def test(self):
        self.page.logout()
        with self.assertRaises(NoSuchElementException):
            self.page.menu_bar.login_form_button()

    def tearDown(self):
        self.driver.quit()
