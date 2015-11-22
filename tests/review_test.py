# -*- coding: utf-8 -*-
import os
import unittest
from collections import OrderedDict

from selenium import webdriver

from pages import MainPage, AddReviewPage
from tests.asserts import CustomAssertions
from tests.components import RatingsBlock, CarSelect


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
        self.page.logout()
        self.driver.quit()


class CarSelectionTest(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']
    BRAND = "Audi"
    MODEL = "100"
    YEAR = "1996"
    MODIFICATION = "1.6 AT"
    RUN_CURRENT = "123321"

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = AddReviewPage(self.driver)
        self.page.open()
        self.page.login(self.LOGIN, self.PASSWORD)

    def test(self):
        selects = OrderedDict([("Марка", self.BRAND),
                               ("Модель", self.MODEL),
                               ("Год производства", self.YEAR),
                               ("Модификация", self.MODIFICATION)])

        select = CarSelect(self.driver)
        for k, v in selects.iteritems():
            select.select_option(k, v)
        select.set_run_current(self.RUN_CURRENT)

    def tearDown(self):
        pass
        self.page.logout()
        self.driver.quit()
