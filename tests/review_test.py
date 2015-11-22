# -*- coding: utf-8 -*-
import os
import unittest
from collections import OrderedDict

from selenium import webdriver

from pages import MainPage, AddReviewPage
from tests.asserts import CustomAssertions
from tests.components import RatingsBlock


class BaseTestCase(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']


class LoginTest(BaseTestCase):
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


class LogoutTest(BaseTestCase, CustomAssertions):
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


class AverageRatingTest(BaseTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = AddReviewPage(self.driver)
        self.page.open()

    def test(self):
        ratings = [
            {"name": RatingsBlock.DESIGN_RATING_NAME, "rating": 5},
            {"name": RatingsBlock.COMFORT_RATING_NAME, "rating": 4},
            {"name": RatingsBlock.CONTROL_RATING_NAME, "rating": 3},
            {"name": RatingsBlock.ERGONOMICS_RATING_NAME, "rating": 3},
            {"name": RatingsBlock.RELIABILITY_RATING_NAME, "rating": 2},
            {"name": RatingsBlock.SERVICE_RATING_NAME, "rating": 1}
        ]

        average_rating = float(sum([x["rating"] for x in ratings])) / float(len(ratings))

        for rating in ratings:
            self.page.ratings.set_rating(rating["name"], rating["rating"])

        self.assertAlmostEqual(average_rating, average_rating, places=1)

    def tearDown(self):
        self.driver.quit()


class CarSelectionTest(BaseTestCase):
    BRAND = "Audi"
    MODEL = "100"
    YEAR = "1996"
    MODIFICATION = "1.6 AT"
    RUN_CURRENT = "123321"
    RESULT_CURRENT = "123 321"

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = AddReviewPage(self.driver)
        self.page.open()

    def test(self):
        selects = OrderedDict([("Марка", self.BRAND),
                               ("Модель", self.MODEL),
                               ("Год производства", self.YEAR),
                               ("Модификация", self.MODIFICATION)])

        select = self.page.car_select
        for k, v in selects.iteritems():
            select.select_option(k, v)
        select.set_run_current(self.RUN_CURRENT)

        self.assertEqual(self.BRAND, select.get_current_value("Марка"))
        self.assertEqual(self.MODEL, select.get_current_value("Модель"))
        self.assertEqual(self.YEAR, select.get_current_value("Год производства"))
        self.assertEqual(self.MODIFICATION, select.get_current_value("Модификация"))
        self.assertEqual(self.RESULT_CURRENT, select.run_current)

    def tearDown(self):
        self.driver.quit()


class ReviewTextTest(BaseTestCase):
    ADVANTAGES_TEXT = "Advantages test Advantages test Advantages test Advantages test " \
                      "Advantages test Advantages test Advantages test Advantages test " \
                      "Advantages test Advantages test Advantages test Advantages test "
    COMMON_TEXT = "Common text Common text Common text Common text Common text Common text " \
                  "Common text Common text Common text Common text Common text Common text " \
                  "Common text Common text Common text Common text Common text Common text "
    PROBLEMS_TEXT = "Problems text Problems text Problems text Problems text Problems text " \
                    "Problems text Problems text Problems text Problems text Problems text " \
                    "Problems text Problems text Problems text Problems text Problems text "

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.page = AddReviewPage(self.driver)
        self.page.open()

    def test(self):
        reviews = self.page.review_inputs
        reviews.set_common_text(self.COMMON_TEXT)
        reviews.set_advantages_text(self.ADVANTAGES_TEXT)
        reviews.set_problems_text(self.PROBLEMS_TEXT)

        self.assertEqual(self.COMMON_TEXT, reviews.common_text)
        self.assertEqual(self.ADVANTAGES_TEXT, reviews.advantages_text)
        self.assertEqual(self.PROBLEMS_TEXT, reviews.problems_text)

    def tearDown(self):
        self.driver.quit()
