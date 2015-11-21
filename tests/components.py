# -*- coding: utf-8 -*-

from selenium.webdriver.support.ui import WebDriverWait


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    OPEN_LOGIN_FORM_BUTTON = '//*[@id="PH_authLink"]'
    LOGIN = '//*[@id="ph_login"]'
    PASSWORD = '//*[@id="ph_password"]'
    SUBMIT = '//*[@class="x-ph__button__input"]'

    def open_form(self):
        self.driver.find_element_by_xpath(self.OPEN_LOGIN_FORM_BUTTON).click()

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, password):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(pwd)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()
