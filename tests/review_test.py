# -*- coding: utf-8 -*-
import os
import unittest
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote

from pages import MainPage, AddReviewPage, ReviewPage
from tests.asserts import CustomAssertions
from tests.components import RatingsBlock


class BaseTestCase(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']
    BROWSER = os.environ['TTHA4BROWSER']
    LOCAL = "LOCAL" in os.environ

    drivers = {
        'FIREFOX': webdriver.Firefox,
        'CHROME': webdriver.Chrome
    }

    @classmethod
    def setUpClass(cls):
        if cls.LOCAL:
            cls.driver = cls.drivers[cls.BROWSER]()
        else:
            cls.driver = Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=getattr(DesiredCapabilities, cls.BROWSER).copy()
            )


class LoginTest(BaseTestCase):
    def test(self):
        self.page = MainPage(self.driver)
        self.page.open()
        self.page.login(self.LOGIN, self.PASSWORD)

        menu_bar = self.page.menu_bar
        self.assertEqual(menu_bar.email_value, self.LOGIN)

    def tearDown(self):
        self.page.logout()
        self.driver.quit()


class LogoutTest(BaseTestCase, CustomAssertions):
    def setUp(self):
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

        average_rating = round(float(sum([x["rating"] for x in ratings])) / float(len(ratings)), 1)

        self.page.set_ratings(ratings)
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
        self.page = AddReviewPage(self.driver)
        self.page.open()

    def test(self):
        options = OrderedDict([("Марка", self.BRAND),
                               ("Модель", self.MODEL),
                               ("Год производства", self.YEAR),
                               ("Модификация", self.MODIFICATION)])

        self.page.select_car_options(options)
        self.page.set_run_current(self.RUN_CURRENT)

        select = self.page.car_select

        self.assertEqual(self.BRAND, select.get_current_value("Марка"))
        self.assertEqual(self.MODEL, select.get_current_value("Модель"))
        self.assertEqual(self.YEAR, select.get_current_value("Год производства"))
        self.assertEqual(self.MODIFICATION, select.get_current_value("Модификация"))
        self.assertEqual(self.RESULT_CURRENT, select.run_current)

    def tearDown(self):
        self.driver.quit()


class ReviewTextInputTest(BaseTestCase):
    ADVANTAGES_TEXT = "Advantages" * 40
    COMMON_TEXT = "Common" * 40
    PROBLEMS_TEXT = "Problems" * 40

    def setUp(self):
        self.page = AddReviewPage(self.driver)
        self.page.open()

    def test(self):
        reviews = self.page.review_inputs

        self.page.set_texts(self.COMMON_TEXT, self.ADVANTAGES_TEXT, self.PROBLEMS_TEXT)
        self.assertEqual(self.COMMON_TEXT, reviews.common_text)
        self.assertEqual(self.ADVANTAGES_TEXT, reviews.advantages_text)
        self.assertEqual(self.PROBLEMS_TEXT, reviews.problems_text)

    def tearDown(self):
        self.driver.quit()


class AddReviewTest(BaseTestCase):
    # Car text review
    ADVANTAGES_TEXT = "Advantages" * 40
    COMMON_TEXT = "Common" * 40
    PROBLEMS_TEXT = "Problems" * 40

    # Car ratings
    RATINGS = [
            {"name": RatingsBlock.DESIGN_RATING_NAME, "rating": 5},
            {"name": RatingsBlock.COMFORT_RATING_NAME, "rating": 4},
            {"name": RatingsBlock.CONTROL_RATING_NAME, "rating": 3},
            {"name": RatingsBlock.ERGONOMICS_RATING_NAME, "rating": 3},
            {"name": RatingsBlock.RELIABILITY_RATING_NAME, "rating": 2},
            {"name": RatingsBlock.SERVICE_RATING_NAME, "rating": 2}
    ]

    # Car options
    BRAND = "Audi"
    MODEL = "100"
    YEAR = "1996"
    MODIFICATION = "1.6 AT"
    RUN_CURRENT = "400"

    REVIEW_TITLE = BRAND + " " + MODEL + " " + MODIFICATION + " " + YEAR + u" г."

    def setUp(self):
        self.add_review_page = AddReviewPage(self.driver)
        self.add_review_page.open()
        self.add_review_page.login(self.LOGIN, self.PASSWORD)

    def test(self):
        self.add_review_page.set_ratings(self.RATINGS)

        options = OrderedDict([("Марка", self.BRAND),
                               ("Модель", self.MODEL),
                               ("Год производства", self.YEAR),
                               ("Модификация", self.MODIFICATION)])

        self.add_review_page.select_car_options(options)
        self.add_review_page.car_select.wait_option_enabled("Привод")
        self.add_review_page.set_run_current(self.RUN_CURRENT)
        self.add_review_page.set_texts(self.COMMON_TEXT, self.ADVANTAGES_TEXT, self.PROBLEMS_TEXT)

        self.add_review_page.add_review()
        self.add_review_page.wait_add_review()
        self.add_review_page.show_review()

        self.review_page = ReviewPage(self.driver)
        average_rating = round(float(sum([x["rating"] for x in self.RATINGS])) / float(len(self.RATINGS)), 1)
        self.assertEqual(average_rating, self.review_page.review_avg_rating)
        self.assertEqual(self.REVIEW_TITLE, self.review_page.review_title)
        self.assertEquals(self.COMMON_TEXT, self.review_page.review_text.common_text)
        self.assertEquals(self.ADVANTAGES_TEXT, self.review_page.review_text.advantages_text)
        self.assertEquals(self.PROBLEMS_TEXT, self.review_page.review_text.problems_text)

    def tearDown(self):
        self.review_page.remove_review()
        self.review_page.logout()
        self.driver.quit()
