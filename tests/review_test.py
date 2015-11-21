# -*- coding: utf-8 -*-
import os
import unittest
from selenium import webdriver
from pages import MainPage


class LoginTest(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']

    def setUp(self):
        # TODO: Driver env
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test(self):
        page = MainPage(self.driver)
        page.open()

        auth_form = page.auth_form
        auth_form.open_form()
        auth_form.set_login(self.LOGIN)
        auth_form.set_password(self.PASSWORD)
        auth_form.submit()

        menu_bar = page.menu_bar
        self.assertEqual(menu_bar.email_value, self.LOGIN)
