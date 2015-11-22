# -*- coding: utf-8 -*-

from tests.utils import wait_invisibility_by_xpath, wait_visibility_by_xpath, wait_enabled_by_xpath


class Component(object):
    def __init__(self, driver):
        self.driver = driver


class AuthForm(Component):
    PRELOADER_XPATH = '//*[@class="x-ph__popup__content__preloader"]'
    LOGIN_XPATH = '//*[@id="ph_login"]'
    PASSWORD_XPATH = '//*[@id="ph_password"]'
    SUBMIT_XPATH = '//*[@class="x-ph__button__input"]'

    def wait_until_form_is_loaded(self):
        wait_invisibility_by_xpath(self.driver, self.PRELOADER_XPATH)
        wait_visibility_by_xpath(self.driver, self.LOGIN_XPATH)
        wait_visibility_by_xpath(self.driver, self.PASSWORD_XPATH)
        wait_enabled_by_xpath(self.driver, self.SUBMIT_XPATH)

    def set_login(self, login):
        self.driver.find_element_by_xpath(self.LOGIN_XPATH).send_keys(login)

    def set_password(self, password):
        self.driver.find_element_by_xpath(self.PASSWORD_XPATH).send_keys(password)

    def submit(self):
        self.driver.find_element_by_xpath(self.SUBMIT_XPATH).submit()


class MenuBar(Component):
    OPEN_LOGIN_FORM_BUTTON_XPATH = '//*[@id="PH_authLink"]'
    EMAIL_FIELD_XPATH = '//*[@id="PH_user-email"]'
    LOGOUT_BUTTON_XPATH = '//*[@id="PH_logoutLink"]'

    def open_login_form(self):
        self.driver.find_element_by_xpath(self.OPEN_LOGIN_FORM_BUTTON_XPATH).click()

    def logout(self):
        wait_visibility_by_xpath(self.driver, self.LOGOUT_BUTTON_XPATH)
        self.driver.find_element_by_xpath(self.LOGOUT_BUTTON_XPATH).click()

    @property
    def email_value(self):
        wait_visibility_by_xpath(self.driver, self.EMAIL_FIELD_XPATH)
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


class ReviewText(Component):
    COMMON_TEXT_INPUT_XPATH = '//*[@name="common_text"]'
    ADVANTAGES_TEXT_INPUT_XPATH = '//*[@name="advantages_text"]'
    PROBLEMS_TEXT_INPUT_XPATH = '//*[@name="problems_text"]'

    def set_common_text(self, text):
        self.driver.find_element_by_xpath(self.COMMON_TEXT_INPUT_XPATH).send_keys(text)

    def set_advantages_text(self, text):
        self.driver.find_element_by_xpath(self.ADVANTAGES_TEXT_INPUT_XPATH).send_keys(text)

    def set_problems_text(self, text):
        self.driver.find_element_by_xpath(self.PROBLEMS_TEXT_INPUT_XPATH).send_keys(text)

    @property
    def common_text(self):
        return self.driver.find_element_by_xpath(self.COMMON_TEXT_INPUT_XPATH).get_attribute('value')

    @property
    def advantages_text(self):
        return self.driver.find_element_by_xpath(self.ADVANTAGES_TEXT_INPUT_XPATH).get_attribute('value')

    @property
    def problems_text(self):
        return self.driver.find_element_by_xpath(self.PROBLEMS_TEXT_INPUT_XPATH).get_attribute('value')


class CarSelect(Component):
    SELECT_BY_TITLE_XPATH = '//*[@data-title="{title}"]'
    CURRENT_SELECT_VALUE_XPATH = '//*[@data-title="{title}"]/div/div/div'
    SELECT_DISABLED_BY_TITLE_XPATH = '//*[@data-title="{title}"]/div[1][contains(@class, "input__box_disabled")]'
    VALUE_BY_TITLE_XPATH = '//*[contains(@class, "input__data__value") and text()="{value}"]'
    RUN_CURRENT_INPUT_XPATH = '//*[@class="input__data__value selt-run_current" and not(@data-type="masked")]'

    def select_option(self, title, value):
        wait_invisibility_by_xpath(self.driver, self.SELECT_DISABLED_BY_TITLE_XPATH.format(title=title))
        self.driver.find_element_by_xpath(self.SELECT_BY_TITLE_XPATH.format(title=title)).click()
        self.driver.find_element_by_xpath(self.VALUE_BY_TITLE_XPATH.format(value=value)).click()

    def set_run_current(self, value):
        self.driver.find_element_by_xpath(self.RUN_CURRENT_INPUT_XPATH).send_keys(value)

    @property
    def run_current(self):
        return self.driver.find_element_by_xpath(self.RUN_CURRENT_INPUT_XPATH).get_attribute('value')

    def get_current_value(self, title):
        return self.driver.find_element_by_xpath(self.CURRENT_SELECT_VALUE_XPATH.format(title=title)).text


class AddReviewButton(Component):
    ADD_REVIEW_BUTTON_XPATH = '//button[@class="button js-check_auth"]'

    def add_review(self):
        self.driver.find_element_by_xpath(self.ADD_REVIEW_BUTTON_XPATH).click()

