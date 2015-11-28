from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def wait_invisibility_by_xpath(driver, xpath):
    WebDriverWait(driver, 30, 0.05).until(
        ec.invisibility_of_element_located((By.XPATH, xpath))
    )


def wait_clickable_by_xpath(driver, xpath):
    WebDriverWait(driver, 30, 0.05).until(
        ec.element_to_be_clickable((By.XPATH, xpath))
    )


def wait_visibility_by_xpath(driver, xpath):
    WebDriverWait(driver, 30, 0.05).until(
        ec.visibility_of_element_located((By.XPATH, xpath))
    )


def wait_presence_by_xpath(driver, xpath):
    WebDriverWait(driver, 30, 0.05).until(
        ec.presence_of_element_located((By.XPATH, xpath))
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


class url_ends_with(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, driver):
        url = driver.current_url
        if url.endswith(self.url):
            return url
        else:
            return False


def wait_url_ends_with(driver, url):
    WebDriverWait(driver, 30, 0.05).until(
        url_ends_with(url)
    )


class element_text_change(object):
    def __init__(self, init_value, xpath):
        self.init_value = init_value
        self.xpath = xpath

    def __call__(self, driver):
        current_value = driver.find_element(by=By.XPATH, value=self.xpath).text
        if self.init_value != current_value:
            return current_value
        else:
            return False


def wait_text_change(driver, xpath):
    init_value = driver.find_element(by=By.XPATH, value=xpath).text
    WebDriverWait(driver, 30, 0.05).until(
        element_text_change(init_value, xpath)
    )


def login(driver, username, password):
    from tests.pages import MainPage

    main_page = MainPage(driver)
    main_page.open()
    main_page.login(username, password)
    wait_url_ends_with(driver, "/?from=authpopup")