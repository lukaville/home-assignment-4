# -*- coding: utf-8 -*-

import unittest
import sys
from tests.review_test import ReviewTest

if __name__ == '__main__':
    suite = unittest.TestSuite((
        unittest.makeSuite(ReviewTest),
    ))
    result = unittest.TextTestRunner().run(suite)
    sys.exit(not result.wasSuccessful())