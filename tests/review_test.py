# -*- coding: utf-8 -*-
import os
import unittest

from selenium import webdriver

from pages import MainPage, AddReviewPage
from tests.asserts import CustomAssertions
from tests.components import RatingsBlock


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
        self.assertElementExists(self.driver, self.page.menu_bar.OPEN_LOGIN_FORM_BUTTON_XPATH)

    def tearDown(self):
        self.driver.quit()


class AverageRatingTest(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = AddReviewPage(self.driver)
        self.page.open()
        self.page.login(self.LOGIN, self.PASSWORD)

    def test(self):
        ratings = [
            {"name": RatingsBlock.DESIGN_RATING_NAME, "rating": 5},
            {"name": RatingsBlock.COMFORT_RATING_NAME, "rating": 4},
            {"name": RatingsBlock.CONTROL_RATING_NAME, "rating": 3},
            {"name": RatingsBlock.ERGONOMICS_RATING_NAME, "rating": 3},
            {"name": RatingsBlock.RELIABILITY_RATING_NAME, "rating": 2},
            {"name": RatingsBlock.SERVICE_RATING_NAME, "rating": 1}
        ]

        average_rating = sum([x["rating"] for x in ratings]) // len(ratings)

        for rating in ratings:
            self.page.ratings.set_rating(rating["name"], rating["rating"])

        self.assertAlmostEqual(average_rating, average_rating)

    def tearDown(self):
        self.driver.quit()
