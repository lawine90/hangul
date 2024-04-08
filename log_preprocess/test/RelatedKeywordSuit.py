
import unittest
from log_preprocess.main.related_keyword import sliding_log, keyword_type


class RelatedKeywordTest(unittest.TestCase):
    # test1: sliding_log
    def test_sliding_log(self):
        # test keywords
        logs = [
            (1712188522, "아이폰 15"),
            (1712188528, "아이폰 15 케이스"),
            (1712188548, "아이폰 15 프로 맥스"),
            (1712188558, "아이폰 15 프로 케이스"),
        ]
        output = [
            ('아이폰 15', '아이폰 15 케이스'),
            ('아이폰 15 케이스', '아이폰 15 프로 맥스'),
            ('아이폰 15 프로 맥스', '아이폰 15 프로 케이스')
        ]

        result = list(sliding_log(iterable=logs))
        self.assertEqual(first=result, second=output)

    # test2: keyword_type
    def test_keyword_type(self):
        pairs = [
            ('아이폰 15', '아이폰 15 케이스', 'add'),
            ('아이폰 15 케이스', '아이폰 15', 'del'),
            ('아이폰 15 프로 맥스', '아이폰 15 프로 케이스', 'mod')
        ]

        for left, right, ktype in pairs:
            self.assertEqual(first=ktype, second=keyword_type(mkey=left, skey=right))


if __name__ == "__main__":
    unittest.main()
