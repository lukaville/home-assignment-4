# -*- coding: utf-8 -*-

import urlparse

from components import AuthForm, MenuBar, RatingsBlock, CarSelect, ReviewText


class Page(object):
    BASE_URL = 'https://cars.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)


class BasePage(Page):
    def __init__(self, driver):
        super(BasePage, self).__init__(driver)
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


class MainPage(BasePage):
    pass


class AddReviewPage(BasePage):
    PATH = 'reviews/add_edit_review/'

    def __init__(self, driver):
        super(AddReviewPage, self).__init__(driver)
        self.ratings = RatingsBlock(driver)
        self.car_select = CarSelect(driver)
        self.review_inputs = ReviewText(driver)
