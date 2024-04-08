
import unittest
from log_preprocess.main.remove_x_fix import create_trie, find_pattern, remove_x_fix


class RemoveXFixTest(unittest.TestCase):
    # test1: find_pattern
    def test_sliding_log(self):
        # test keywords
        trie = create_trie(patterns=["아이폰", "갤럭시"])

        # search keywords
        keywords = ["아이폰 15", "갤럭시 24", "아이패드 프로", "아이폰 갤럭시 비교"]
        founds = [
            [(0, 2, '아이폰')],
            [(0, 2, '갤럭시')],
            [],
            [(0, 2, '아이폰'), (4, 6, '갤럭시')]
        ]

        for k, f in zip(keywords, founds):
            found = find_pattern(query=k, trie=trie)
            print(f"keyword: {k}")
            print(f"found: {found}\n")

            self.assertEqual(first=found, second=f)

    # test2: remove_x_fix
    def test_remove_prefix(self):
        # test keywords
        trie = create_trie(patterns=["아이폰", "갤럭시"])

        # search keywords
        keywords = ["아이폰 15", "갤럭시 24", "아이패드 프로", "아이폰 갤럭시 비교"]
        prefix_removed = ["아이패드 프로"]

        result = list(filter(lambda q: remove_x_fix(query=q, trie=trie, fix_type="prefix"), keywords))
        self.assertEqual(first=prefix_removed, second=result)


if __name__ == "__main__":
    unittest.main()
