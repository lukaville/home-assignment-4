# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    PRELOADER_XPATH = '//*[@class="x-ph__popup__content__preloader"]'
    LOGIN_XPATH = '//*[@id="ph_login"]'
    PASSWORD_XPATH = '//*[@id="ph_password"]'
    SUBMIT_XPATH = '//*[@class="x-ph__button__input"]'

    def wait_until_form_is_loaded(self):
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, self.PRELOADER_XPATH))
        )

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN_XPATH).send_keys(login)

    def set_password(self, password):
        self.driver.find_element_by_xpath(self.PASSWORD_XPATH).send_keys(password)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_XPATH).click()


class MenuBar(Component):
    OPEN_LOGIN_FORM_BUTTON_XPATH = '//*[@id="PH_authLink"]'
    EMAIL_FIELD_XPATH = '//*[@id="PH_user-email"]'
    LOGOUT_BUTTON_XPATH = '//*[@id="PH_logoutLink"]'

    def open_login_form(self):
        self.driver.find_element_by_xpath(self.OPEN_LOGIN_FORM_BUTTON_XPATH).click()

    def logout(self):
        WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, self.LOGOUT_BUTTON_XPATH))
        )
        self.driver.find_element_by_xpath(self.LOGOUT_BUTTON_XPATH).click()

    @property
    def email_value(self):
        return self.driver.find_element_by_xpath(self.EMAIL_FIELD_XPATH).text

    @property
    def login_form_button(self):
        return self.driver.find_element_by_xpath(self.OPEN_LOGIN_FORM_BUTTON_XPATH)


class RatingsBlock(Component):
    DESIGN_RATING_NAME = 'design_grade'
    COMFORT_RATING_NAME = 'comfortability_grade'
    CONTROL_RATING_NAME = 'running_characteristics_grade'
    ERGONOMICS_RATING_NAME = 'ergonomics_grade'
    RELIABILITY_RATING_NAME = 'reliability_grade'
    SERVICE_RATING_NAME = 'service_availability_grade'

    RATING_RADIO_XPATH = '//*[@name="{name}" and @value="{value}"]'
    AVERAGE_RATING_XPATH = '//*[@class="js-average_score_val"]'

    def set_rating(self, rating_name, value):
        radio_xpath = self.RATING_RADIO_XPATH.format(name=rating_name, value=value)
        self.driver.find_element_by_xpath(radio_xpath).click()

    @property
    def average_rating(self):
        return float(self.driver.find_element_by_xpath(self.AVERAGE_RATING_XPATH).text)
