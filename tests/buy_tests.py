# coding=utf-8
from selenium.webdriver import ActionChains

from tests.base import BaseTestCase
from tests.pages import BuyPage


class FilterBuyTestCase(BaseTestCase):
    WITHOUT_PHOTO_SRC = 'https://cars.mail.ru/img/default/nofoto__car_sedan_small.jpg'

    def setUp(self):
        self.create_driver()
        self.page = BuyPage(self.driver)
        self.page.open()

    def test_brand(self):
        self.page.filters.select_filter('Все марки', 'BMW')
        self.page.filters.submit_filters()
        self.assertFalse(self.page.car_buy_block.if_car_without_mark_exists('BMW'))

    def test_model(self):
        self.page.filters.select_filter('Все марки', 'Audi')
        self.page.filters.select_filter('Все модели', '100')
        self.page.filters.submit_filters()
        self.assertFalse(self.page.car_buy_block.if_car_without_mark_exists('Audi 100'))

    def test_only_with_photo(self):
        self.page.filters.select_only_with_photo()
        self.page.filters.submit_filters()
        self.assertFalse(self.page.car_buy_block.if_car_with_photo_src_exists(self.WITHOUT_PHOTO_SRC))

    def tearDown(self):
        self.driver.quit()


class CheckFilterTabs(BaseTestCase):
    def setUp(self):
        self.create_driver()
        self.page = BuyPage(self.driver)
        self.page.open()

    def testFilterNew(self):
        self.page.filter_tabs.set_filter_new()
        is_all_cars_with_label = self.page.buy_results.is_car_without_label_exists(u"новый")
        self.assertTrue(is_all_cars_with_label)

    def testFilterGuarantee(self):
        self.page.filter_tabs.set_filter_guarantee()
        is_all_cars_with_label = self.page.buy_results.is_car_without_label_exists(u"на гарантии")
        self.assertTrue(is_all_cars_with_label)

    def tearDown(self):
        self.driver.quit()


class CheckNumberOfResults(BaseTestCase):
    def setUp(self):
        self.create_driver()
        self.page = BuyPage(self.driver)
        self.page.open()

    def test(self):
        self.page.buy_result_count.set_max_results_20()
        self.assertGreaterEqual(20, self.page.buy_results.get_result_count())

        self.page.buy_result_count.set_max_results_40()
        self.assertGreaterEqual(40, self.page.buy_results.get_result_count())

        self.page.buy_result_count.set_max_results_100()
        self.assertGreaterEqual(100, self.page.buy_results.get_result_count())

    def tearDown(self):
        self.driver.quit()


class CheckGuaranteeToolTip(BaseTestCase):
    def setUp(self):
        self.create_driver()
        self.page = BuyPage(self.driver)
        self.page.open()

    def test(self):
        action = ActionChains(self.driver)
        action.move_to_element(self.page.filter_tabs.get_guarantee_tooltip_button())
        action.perform()

        is_tooltip_visible = self.page.filter_tabs.get_guarantee_tooltip().is_displayed()
        self.assertTrue(is_tooltip_visible)

    def tearDown(self):
        self.driver.quit()


class CheckRegionFilter(BaseTestCase):
    def setUp(self):
        self.create_driver()
        self.page = BuyPage(self.driver)
        self.page.open()

    def test(self):
        self.page.filters.set_region(u"Санкт-Петербург")
        result_count_all = self.page.buy_results.get_result_count()
        result_count_city = self.page.buy_results.get_result_count_by_city(u"Санкт-Петербург")
        self.assertEqual(result_count_all, result_count_city)

    def tearDown(self):
        self.driver.quit()
