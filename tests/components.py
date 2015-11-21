# -*- coding: utf-8 -*-
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    PRELOADER = '//*[@class="x-ph__popup__content__preloader"]'
    LOGIN = '//*[@id="ph_login"]'
    PASSWORD = '//*[@id="ph_password"]'
    SUBMIT = '//*[@class="x-ph__button__input"]'

    def wait_until_form_is_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, self.PRELOADER))
        )

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN).send_keys(login)

    def set_password(self, password):
        self.driver.find_element_by_xpath(self.PASSWORD).send_keys(password)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT).click()


class MenuBar(Component):
    OPEN_LOGIN_FORM_BUTTON = '//*[@id="PH_authLink"]'
    EMAIL_FIELD = '//*[@id="PH_user-email"]'
    LOGOUT_BUTTON = '//*[@id="PH_logoutLink"]'

    def open_login_form(self):
        self.driver.find_element_by_xpath(self.OPEN_LOGIN_FORM_BUTTON).click()

    def logout(self):
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.LOGOUT_BUTTON))
        )
        self.driver.find_element_by_xpath(self.LOGOUT_BUTTON).click()

    @property
    def email_value(self):
        return self.driver.find_element_by_xpath(self.EMAIL_FIELD).text

    @property
    def login_form_button(self):
        return self.driver.find_element_by_xpath(self.OPEN_LOGIN_FORM_BUTTON)
