
import unittest
from log_preprocess.main.check_pattern import *


class RemoveXFixTest(unittest.TestCase):
    # test1: is_korean_domain
    def test_is_korean_domain(self):
        # test keywords
        keyword = "삼성전자.com"

        self.assertEqual(
            first=True,
            second=is_korean_domain(keyword)
        )

    # test2: is_tracking_number
    def test_is_tracking_number(self):
        # test keywords
        keyword = "택배 1234567"

        self.assertEqual(
            first=True,
            second=is_tracking_number(keyword)
        )


if __name__ == "__main__":
    unittest.main()
