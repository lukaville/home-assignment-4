# -*- coding: utf-8 -*-

import urlparse

from components import AuthForm, MenuBar, RatingsBlock, CarSelect, AddReviewText, AddReviewButton, AddResultButtons, \
    ReviewText, ReviewManagement, ReviewRemovePopup, ReviewInfo
from tests.utils import wait_visibility_by_xpath


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
        self.review_inputs = AddReviewText(driver)
        self.add_button = AddReviewButton(driver)
        self.add_result_buttons = AddResultButtons(driver)

    def set_ratings(self, ratings):
        for rating in ratings:
            self.ratings.set_rating(rating["name"], rating["rating"])

    def select_car_options(self, options):
        for k, v in options.iteritems():
            self.car_select.select_option(k, v)

    def set_run_current(self, current):
        self.car_select.set_run_current(current)

    def set_texts(self, common, advantages, problems):
        self.review_inputs.set_common_text(common)
        self.review_inputs.set_advantages_text(advantages)
        self.review_inputs.set_problems_text(problems)

    def add_review(self):
        self.add_button.add_review()

    def wait_add_review(self):
        wait_visibility_by_xpath(self.driver, self.add_result_buttons.SHOW_REVIEW_BUTTON_XPATH)

    def show_review(self):
        self.add_result_buttons.show_review()


class ReviewPage(BasePage):
    def __init__(self, driver):
        super(ReviewPage, self).__init__(driver)
        self.review_info = ReviewInfo(driver)
        self.review_text = ReviewText(driver)
        self.review_management = ReviewManagement(driver)
        self.remove_popup = ReviewRemovePopup(driver)

    def remove_review(self):
        self.review_management.remove_review()
        self.remove_popup.wait_popup()
        self.remove_popup.confirm_remove()

    @property
    def review_title(self):
        return self.review_info.title

    @property
    def run_current(self):
        return self.review_info.run_current

    @property
    def review_avg_rating(self):
        return self.review_info.avg_rating
