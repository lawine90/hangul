
import unittest
import pandas as pd
from hangul.main.SlidingBuild import Slidingbuild


class SlidingBuildTest(unittest.TestCase):
    # test1 create decomposed key
    def test_create_mainkey(self):
        # class
        sb = Slidingbuild()

        # args
        weight_list = [10, 1, 1, 1]

        # test keywords
        keywords = [
            ("파이썬", 10),
            ("파이썬 테스트", 5)
        ]

        # outcomes
        outcomes = [
            [('ㅆ', 100.0),
             ('ㅆㅓ', 100.0),
             ('ㅆㅓㄴ', 100.0),
             ('ㅇ', 100.0),
             ('ㅇㅣ', 100.0),
             ('ㅇㅣㅆ', 100.0),
             ('ㅇㅣㅆㅓ', 100.0),
             ('ㅇㅣㅆㅓㄴ', 100.0),
             ('ㅍ', 100.0),
             ('ㅍ', 1000.0),
             ('ㅍㅇ', 100.0),
             ('ㅍㅇㅆ', 100.0),
             ('ㅍㅏ', 1000.0),
             ('ㅍㅏㅇ', 1000.0),
             ('ㅍㅏㅇㅣ', 1000.0),
             ('ㅍㅏㅇㅣㅆ', 1000.0),
             ('ㅍㅏㅇㅣㅆㅓ', 1000.0),
             ('ㅍㅏㅇㅣㅆㅓㄴ', 1000.0)],
            [('ㅌ', 50.0),
             ('ㅌㅔ', 50.0),
             ('ㅌㅔㅅ', 50.0),
             ('ㅌㅔㅅㅡ', 50.0),
             ('ㅌㅔㅅㅡㅌ', 50.0),
             ('ㅌㅔㅅㅡㅌㅡ', 50.0),
             ('ㅍ', 50.0),
             ('ㅍ', 500.0),
             ('ㅍㅇ', 50.0),
             ('ㅍㅇㅆ', 50.0),
             ('ㅍㅇㅆ ', 50.0),
             ('ㅍㅇㅆ ㅌ', 50.0),
             ('ㅍㅇㅆ ㅌㅅ', 50.0),
             ('ㅍㅇㅆ ㅌㅅㅌ', 50.0),
             ('ㅍㅇㅆㅌ', 50.0),
             ('ㅍㅇㅆㅌㅅ', 50.0),
             ('ㅍㅇㅆㅌㅅㅌ', 50.0),
             ('ㅍㅏ', 500.0),
             ('ㅍㅏㅇ', 500.0),
             ('ㅍㅏㅇㅣ', 500.0),
             ('ㅍㅏㅇㅣㅆ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓㄴ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓㄴㅌ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓㄴㅌㅔ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓㄴㅌㅔㅅ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓㄴㅌㅔㅅㅡ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓㄴㅌㅔㅅㅡㅌ', 500.0),
             ('ㅍㅏㅇㅣㅆㅓㄴㅌㅔㅅㅡㅌㅡ', 500.0)]
        ]

        for (k, s), outcome in zip(keywords, outcomes):
            result = sorted(sb.create_mainkey(key=k, score=s, weight_list=weight_list))
            print("engToHan output: ", pd.DataFrame(result), "\n")

            self.assertEqual(
                first=result,
                second=outcome
            )


if __name__ == "__main__":
    unittest.main()

    # # class
    # sb = Slidingbuild()
    #
    # # args
    # weight_list = [10, 1, 1, 1]
    #
    # # test keywords
    # keywords = [
    #     ("파이썬", 10),
    #     ("파이썬 테스트", 5)
    # ]
    #
    # for k, s in keywords:
    #     result = sb.create_mainkey(key=k, score=s, weight_list=weight_list)
    #     print("engToHan output: ", result, "\n")
    #
