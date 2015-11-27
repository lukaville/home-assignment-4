# -*- coding: utf-8 -*-

from tests.base import BaseTestCase
from tests.pages import BuyPage


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