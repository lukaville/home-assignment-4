# coding=utf-8

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