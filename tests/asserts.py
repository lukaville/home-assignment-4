# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException


class CustomAssertions:
    def __init__(self):
        pass

    def assertElementExists(self, webdriver, xpath):
        try:
            webdriver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            raise AssertionError('Element not exists by xpath "' + xpath + '".')
