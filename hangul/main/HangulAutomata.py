"""
한글 전처리
- 영한 변환
- 한영 변환
- 한글 자모 분리
- 한글 자모 결합

magic numbers:
- the number of Consonant: 28
- the number of Vowel: 21
"""

from typing import List, Optional


class HangulAutomata(object):
    def __init__(self):
        # initialize
        self.builder = []
        self.stack = []
        self.state = None

        # hangul start & end code
        self.start_code = ord('\uAC00')
        self.end_code = ord('\uD7A3')

        # chosung
        self.chosung_list = [
            'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ',
            'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ',
            'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ',
            'ㅎ'
        ]

        # chosung with index
        self.chosung_indices = {t[1]: t[0] for t in enumerate(self.chosung_list)}

        # jungsung
        self.jungsung_list = [
            'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ',
            'ㅕ', 'ㅖ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ',
            'ㅡ', 'ㅣ'
        ]
        self.double_jungsung_list = [
            "ㅗㅏ", "ㅗㅐ", "ㅗㅣ", "ㅜㅓ",
            "ㅜㅔ", "ㅜㅣ", "ㅡㅣ"
        ]
        # jungsung with index
        self.jungsung_indices = {t[1]: t[0] for t in enumerate([
            "ㅏ", "ㅐ", "ㅑ", "ㅒ", "ㅓ", "ㅔ", "ㅕ",
            "ㅖ", "ㅗ", "ㅗㅏ", "ㅗㅐ", "ㅗㅣ", "ㅛ", "ㅜ",
            "ㅜㅓ", "ㅜㅔ", "ㅜㅣ", "ㅠ", "ㅡ", "ㅡㅣ", "ㅣ"
        ])}

        # jongsung
        self.jongsung_list = [
            'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ',
            'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ',
            'ㅍ', 'ㅎ'
        ]
        self.double_jongsung_list = [
            "ㄱㅅ", "ㄴㅈ", "ㄴㅎ", "ㄹㄱ", "ㄹㅁ", "ㄹㅂ",
            "ㄹㅅ", "ㄹㅌ", "ㄹㅍ", "ㄹㅎ", "ㅂㅅ"
        ]

        # jongsung with index
        self.jongsung_indices = {t[1]: t[0] for t in enumerate([
            "", "ㄱ", "ㄲ", "ㄱㅅ", "ㄴ", "ㄴㅈ", "ㄴㅎ",
            "ㄷ", "ㄹ", "ㄹㄱ", "ㄹㅁ", "ㄹㅂ", "ㄹㅅ", "ㄹㅌ",
            "ㄹㅍ", "ㄹㅎ", "ㅁ", "ㅂ", "ㅂㅅ", "ㅅ", "ㅆ",
            "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"
        ])}

        # keyboard alphabet to korean character mapping
        self.alphabet_to_hangul = {
            'a': 'ㅁ', 'b': 'ㅠ', 'c': 'ㅊ', 'd': 'ㅇ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ',
            'g': 'ㅎ', 'h': 'ㅗ', 'i': 'ㅑ', 'j': 'ㅓ', 'k': 'ㅏ', 'l': 'ㅣ', 'm': 'ㅡ',
            'n': 'ㅜ', 'o': 'ㅐ', 'O': 'ㅒ', 'p': 'ㅔ', 'P': 'ㅖ', 'q': 'ㅂ', 'Q': 'ㅃ',
            'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 't': 'ㅅ', 'T': 'ㅆ', 'u': 'ㅕ', 'v': 'ㅍ',
            'w': 'ㅈ', 'W': 'ㅉ', 'x': 'ㅌ', 'y': 'ㅛ', 'z': 'ㅋ',
        }
        self.hangul_to_alphabet = {v: k for k, v in self.alphabet_to_hangul.items()}

    # about state
    def resetState(self):
        self.state = None

    def chosungState(self):
        self.state = "CHOSUNG"

    def jungsungState(self):
        self.state = "JUNGSUNG"

    def jongsungState(self):
        self.state = "JONGSUNG"

    # about stack
    def resetStack(self):
        self.stack = []

    def addStack(self, char):
        self.stack.append(char)

    # about builder
    def resetBuilder(self):
        self.builder = []

    def addBuilder(self, char):
        self.builder.append(char)

    # merge individual korean characters
    def mergeChar(self):
        chosung = self.chosung_indices[self.stack[0]]
        jungsung = self.jungsung_indices[self.stack[1]]
        if len(self.stack) == 3:
            jongsung = self.jongsung_indices[self.stack[2]]
        elif len(self.stack) == 4:
            jongsung = self.jongsung_indices[self.stack[2] + self.stack[3]]
        else:
            jongsung = 0

        self.resetStack()
        return chr(((chosung * 21) + jungsung) * 28 + jongsung + self.start_code)

    # normalize
    @staticmethod
    def normalizeString(text: str) -> str:
        return text.lower().strip()

    # english character to hangul
    # 2024-06-11 ignore_kor 옵션 추가
    #   기존 함수는 정상적인 한글이 입력될 경우 에러 발생
    #   정상 한글이 입력되더라도 무시하고 영문만 한글로 변환할 수 있는 ignore_kor 옵션 추가
    #   e.g. 아자개10kg특등급 -> 아자개10ㅏㅎ특등급
    # TODO 현재 로직에서 영문 대문자의 변환이 쌍자음이 있는 경우는 한글로 변환되지만 쌍자음이 없는 경우는 대문자 그대로 변환됨
    #   e.g. RkTkaldk -> 까싸미아
    #   e.g. CkXk -> CㅏXㅏ
    #   추후 쌍자음이 없는 케이스 어떻게 할지 수정 필요
    def engToHan(self, text: str, ignore_kor: bool = False) -> str:
        self.resetState()
        self.resetStack()
        self.resetBuilder()

        for c in text:
            # get korean character
            if ignore_kor:
                try:
                    han_char = self.alphabet_to_hangul[c]
                except:
                    han_char = c
            else:
                han_char = self.alphabet_to_hangul[c]

            # 초기 상태
            if self.state is None:
                if han_char in self.chosung_list:
                    self.addStack(han_char)
                    self.chosungState()
                else:
                    self.addBuilder(han_char)
            # 초성 상태
            elif self.state == "CHOSUNG":
                if han_char in self.jungsung_list:
                    self.addStack(han_char)
                    self.jungsungState()
                elif han_char in self.chosung_list:
                    self.addBuilder(self.stack.pop())
                    self.addStack(han_char)
                else:
                    self.addBuilder(self.stack.pop())
                    self.addBuilder(han_char)
                    self.resetState()
            # 중성 상태
            elif self.state == "JUNGSUNG":
                if han_char in self.jongsung_list:
                    self.addStack(han_char)
                    self.jongsungState()
                elif self.stack[-1] + han_char in self.double_jungsung_list:
                    self.addStack(self.stack.pop() + han_char)
                else:
                    self.addBuilder(self.mergeChar())
                    self.addBuilder(han_char)
                    self.resetState()
            # 종성 상태
            elif self.state == "JONGSUNG":
                if han_char in self.jungsung_list:
                    prev = self.stack.pop()
                    self.addBuilder(self.mergeChar())
                    self.addStack(prev)
                    self.addStack(han_char)
                    self.jungsungState()
                elif self.stack[-1] + han_char in self.double_jongsung_list:
                    self.addStack(han_char)
                elif han_char in self.chosung_list:
                    self.addBuilder(self.mergeChar())
                    self.addStack(han_char)
                    self.chosungState()
                else:
                    self.addBuilder(self.mergeChar())
                    self.addBuilder(han_char)
                    self.resetState()
            else:
                print("do nothing")

        if len(self.stack) == 1:
            self.addBuilder(self.stack.pop())
        elif len(self.stack) > 1:
            self.addBuilder(self.mergeChar())
        else:
            print("also do nothing")

        return "".join(self.builder)

    # hangul characters to jamo
    def hanToJamo(self, text: str) -> str:
        self.resetBuilder()

        for c in text:
            if (ord(c) >= self.start_code) & (ord(c) <= self.end_code):
                jong_code = ord(c) - self.start_code
                cho_code = jong_code // (21 * 28)
                jong_code = jong_code % (21 * 28)
                jung_code = jong_code // 28
                jong_code = jong_code % 28

                self.addBuilder(self.chosung_list[cho_code])
                self.addBuilder(list(self.jungsung_indices.keys())[jung_code])
                if jong_code != 0:
                    self.addBuilder(list(self.jongsung_indices.keys())[jong_code])
            else:
                self.addBuilder(c)

        return "".join(self.builder)

    # jamo characters to english
    def jamoToEng(self, text: str) -> str:
        self.resetBuilder()

        for c in text:
            if c in self.hangul_to_alphabet.keys():
                self.addBuilder(self.hangul_to_alphabet[c])
            else:
                self.addBuilder(c)

        return "".join(self.builder)

    # hangul characters to english
    def hanToEng(self, text: str) -> str:
        return self.jamoToEng(self.hanToJamo(text))

    # check list of str contains only chosung
    @staticmethod
    def isOnlyChosung(text: List[str]) -> bool:
        for c in text:
            if not (
                    (ord('\u0020') <= ord(c) <= ord('\u00A0')) or
                    (ord('\u3131') <= ord(c) <= ord('\u314e'))
            ):
                return False
        return True

    # get chosung only
    def getChosung(self, text: str) -> Optional[str]:
        chos = []

        for c in text:
            jamo = self.hanToJamo(text=c)[0]
            if (jamo in self.chosung_list or
                    c == ' ' or ('0' <= c <= '9')):
                chos.append(jamo)
            else:
                return None
        return "".join(chos)
