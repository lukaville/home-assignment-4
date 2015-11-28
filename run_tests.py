# -*- coding: utf-8 -*-

import sys
import unittest

from tests.buy_tests import FilterBuyTestCase, CheckFilterTabs, CheckNumberOfResults
from tests.review_test import CarSelectionTest, LoginTest, LogoutTest, AverageRatingTest, ReviewTextInputTest, \
    AddReviewTest, AddReviewErrorsTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        # unittest.makeSuite(AddReviewErrorsTest),
        # unittest.makeSuite(LoginTest),
        # unittest.makeSuite(LogoutTest),
        # unittest.makeSuite(AverageRatingTest),
        # unittest.makeSuite(CarSelectionTest),
        # unittest.makeSuite(ReviewTextInputTest),
        # unittest.makeSuite(AddReviewTest),
        # unittest.makeSuite(CheckFilterTabs),
        # unittest.makeSuite(CheckNumberOfResults),
        unittest.makeSuite(FilterBuyTestCase)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
