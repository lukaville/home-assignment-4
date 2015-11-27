import os
import unittest

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities, Remote


class BaseTestCase(unittest.TestCase):
    LOGIN = os.environ['TTHA4LOGIN']
    PASSWORD = os.environ['TTHA4PASSWORD']
    BROWSER = os.environ['TTHA4BROWSER']
    LOCAL = "LOCAL" in os.environ

    drivers = {
        'FIREFOX': webdriver.Firefox,
        'CHROME': webdriver.Chrome
    }

    def create_driver(self):
        if self.LOCAL:
            self.driver = self.drivers[self.BROWSER]()
        else:
            self.driver = Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=getattr(DesiredCapabilities, self.BROWSER).copy()
            )