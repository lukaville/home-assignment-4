# -*- coding: utf-8 -*-


import unittest
import urlparse

from selenium import webdriver


class Page(object):
    BASE_URL = 'https://cars.mail.ru/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()


class AddReviewPage(Page):
    PATH = 'reviews/add_edit_review/'


class ReviewTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test(self):
        pass
