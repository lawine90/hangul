import unittest

from main.HangulAutomata import HangulAutomata


class HangulAutomataTest(unittest.TestCase):
    # test1 english to hangul test
    def testEngToHan(self):
        h = HangulAutomata()
        result1 = h.engToHan("dkssudgktpdy")
        print("engToHan result: ", result1)

        self.assertEqual(
            result1,
            "안녕하세요"
        )

        result2 = h.engToHan("dkdidjdudhdydndbdmdl")
        self.assertEqual(
            result2,
            "아야어여오요우유으이"
        )

        result3 = h.engToHan("wmfuqkfqrhrktldhqthtj")
        self.assertEqual(
            result3,
            "즈려밟고가시옵소서"
        )

    # test2 hangul to jamo test
    def testHanToJamo(self):
        h = HangulAutomata()
        result1 = h.hanToJamo("안녕하세요")
        print("hanToJamo result: ", result1)

        self.assertEqual(
            result1,
            "ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ"
        )

    # test3 hangul to english test
    def testHanToEng(self):
        h = HangulAutomata()
        result1 = h.hanToEng("ㅗ메ㅔㅛ 채야ㅜㅎ!")
        print("hanToEng result: ", result1)

        self.assertEqual(
            result1,
            "happy coding!"
        )


if __name__ == '__main__':
    unittest.main()
