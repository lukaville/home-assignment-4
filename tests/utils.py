from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def wait_invisibility_by_xpath(driver, xpath):
    WebDriverWait(driver, 30).until(
        ec.invisibility_of_element_located((By.XPATH, xpath))
    )


def wait_visibility_by_xpath(driver, xpath):
    WebDriverWait(driver, 30).until(
        ec.visibility_of_element_located((By.XPATH, xpath))
    )
