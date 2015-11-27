# -*- coding: utf-8 -*-
import os
import unittest
from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote

from pages import MainPage, AddReviewPage, ReviewPage
from tests.asserts import CustomAssertions
from tests.components import RatingsBlock
from tests.utils import wait_url_ends_with, wait_text_change, login


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
        try:
            self.page.logout()
        finally:
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

        average_rating = float(sum([x["rating"] for x in ratings])) / float(len(ratings))

        self.page.set_ratings(ratings)
        wait_text_change(self.driver, self.page.ratings.AVERAGE_RATING_XPATH)
        self.assertAlmostEqual(average_rating, self.page.ratings.average_rating, places=1)

    def tearDown(self):
        self.driver.quit()


class AddReviewErrorsTest(BaseTestCase):

    # Not full Car ratings
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

    def setUp(self):
        login(self.driver, self.LOGIN, self.PASSWORD)
        wait_url_ends_with(self.driver, "/?from=authpopup")
        self.page = AddReviewPage(self.driver)
        self.page.open()

    def testRatings(self):
        self.page.set_ratings(self.RATINGS[:-1])
        self.page.add_review()
        self.assertFalse(self.page.ratings.is_rating_valid("Обслуживание и ремонт"))
        self.page.set_ratings([self.RATINGS[-1]])
        self.assertTrue(self.page.ratings.is_all_ratings_valid())

    def tearDown(self):
        try:
            self.page.logout()
        finally:
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
        login(self.driver, self.LOGIN, self.PASSWORD)
        wait_url_ends_with(self.driver, "/?from=authpopup")
        self.add_review_page = AddReviewPage(self.driver)
        self.add_review_page.open()

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
        self.assertEqual(self.RUN_CURRENT, self.review_page.run_current)
        self.assertEqual(self.REVIEW_TITLE, self.review_page.review_title)
        self.assertEquals(self.COMMON_TEXT, self.review_page.review_text.common_text)
        self.assertEquals(self.ADVANTAGES_TEXT, self.review_page.review_text.advantages_text)
        self.assertEquals(self.PROBLEMS_TEXT, self.review_page.review_text.problems_text)

    def tearDown(self):
        try:
            self.review_page.remove_review()
            self.review_page.logout()
        finally:
            self.driver.quit()
