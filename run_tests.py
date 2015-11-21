# -*- coding: utf-8 -*-

import unittest
import sys
from tests.review_test import LoginTest, LogoutTest, AverageRatingTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(LoginTest),
        unittest.makeSuite(LogoutTest),
        unittest.makeSuite(AverageRatingTest)
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())
