
import unittest
from hangul.main.HangulAutomata import HangulAutomata


class HangulAutomataTest(unittest.TestCase):
    # test1 english to hangul test
    def testEngToHan(self):
        # class
        h = HangulAutomata()

        # test keywords
        eng_to_han_tuple = [
            ("dkssudgktpdy", "안녕하세요"),
            ("dkdidjdudhdydndbdmdl", "아야어여오요우유으이"),
            ("wmfuqkfqrhrktldhqthtj", "즈려밟고가시옵소서"),
        ]

        for input, output in eng_to_han_tuple:
            result = h.engToHan(text=input)

            print("engToHan input: ", input)
            print("engToHan output: ", result, "\n")

            self.assertEqual(first=result, second=output)

    # test2 hangul to jamo test
    def testHanToJamo(self):
        h = HangulAutomata()
        result1 = h.hanToJamo("안녕하세요")
        print("hanToJamo input: ", "안녕하세요")
        print("hanToJamo output: ", result1, "\n")

        self.assertEqual(
            first=result1,
            second="ㅇㅏㄴㄴㅕㅇㅎㅏㅅㅔㅇㅛ"
        )

    # test3 hangul to english test
    def testHanToEng(self):
        h = HangulAutomata()
        result1 = h.hanToEng("ㅗ메ㅔㅛ 채야ㅜㅎ!")
        print("hanToEng input: ", "ㅗ메ㅔㅛ 채야ㅜㅎ!")
        print("hanToEng output: ", result1, "\n")

        self.assertEqual(
            first=result1,
            second="happy coding!"
        )


if __name__ == "__main__":
    unittest.main()
