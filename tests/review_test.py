# -*- coding: utf-8 -*-

import unittest
from selenium import webdriver
from pages import MainPage


class AuthTest(unittest.TestCase):
    def setUp(self):
        # TODO: Driver env
        self.driver = webdriver.Firefox()

    def tearDown(self):
        pass
        self.driver.quit()

    def test(self):
        page = MainPage(self.driver)
        page.open()

        auth_form = page.auth_form
        auth_form.open_form
        auth_form.set_login("login")
        auth_form.set_password("password")
        auth_form.submit()
