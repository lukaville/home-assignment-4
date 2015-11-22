from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def wait_invisibility_by_xpath(driver, xpath):
    WebDriverWait(driver, 30, 0.05).until(
        ec.invisibility_of_element_located((By.XPATH, xpath))
    )


def wait_visibility_by_xpath(driver, xpath):
    WebDriverWait(driver, 30, 0.05).until(
        ec.visibility_of_element_located((By.XPATH, xpath))
    )


class element_to_be_enabled(object):
    def __init__(self, xpath):
        self.xpath = xpath

    def __call__(self, driver):
        element = driver.find_element(by=By.XPATH, value=self.xpath)
        if element and element.is_enabled():
            return element
        else:
            return False


def wait_enabled_by_xpath(driver, xpath):
    WebDriverWait(driver, 30, 0.05).until(
        element_to_be_enabled(xpath)
    )
