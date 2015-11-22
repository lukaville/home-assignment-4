# -*- coding: utf-8 -*-

import sys
import unittest

from tests.review_test import CarSelectionTest, LoginTest, LogoutTest, AverageRatingTest, ReviewTextTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(LoginTest),
        unittest.makeSuite(LogoutTest),
        unittest.makeSuite(AverageRatingTest),
        unittest.makeSuite(CarSelectionTest),
        unittest.makeSuite(ReviewTextTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
