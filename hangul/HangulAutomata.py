class HangulAutomata():
    def __init__(self):
        # chosung
        self.chosung_list = [
            'ㄱ',  'ㄲ',  'ㄴ',  'ㄷ',  'ㄸ',  'ㄹ',
            'ㅁ',  'ㅂ',  'ㅃ',  'ㅅ',  'ㅆ',  'ㅇ',
            'ㅈ',  'ㅉ',  'ㅊ',  'ㅋ',  'ㅌ',  'ㅍ',
            'ㅎ'
        ]

        # chosung with index
        self.chosung_indices = {t[1]: t[0] for t in enumerate(chosung_list)}

        #jungsung
        self.jungsung_list = [
            'ㅏ',  'ㅐ',  'ㅑ',  'ㅒ',  'ㅓ',  'ㅔ',
            'ㅕ',  'ㅖ',  'ㅗ',  'ㅛ',  'ㅜ',  'ㅠ',
            'ㅡ',  'ㅣ'
        ]
        self.double_jungsung_list = [
            "ㅗㅏ", "ㅗㅐ", "ㅗㅣ", "ㅜㅓ",
            "ㅜㅔ", "ㅜㅣ","ㅡㅣ"
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
            "ㄷ", "ㄹ", "ㄹㄱ", "ㄹㅁ", "ㄹㅂ","ㄹㅅ", "ㄹㅌ",
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
        self.hangul_to_alphabet = {v: k for k, v in alphabet_to_hangul.items()}


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
        if (len(self.stack) == 3):
            jongsung = self.jongsung_indices[self.stack[2]]
        elif (len(self.stack) == 4):
            jongsung = self.jongsung_indices[self.stack[2]+self.stack[3]]
        else:
            jongsung = 0

        self.resetStack()
        return chr(((chosung * 21) + jungsung) * 28 + jongsung + ord('\uAC00'))

    # normalize
    def normalizeString(self, text):
        return text.lower().strip()

    # english character to hangul
    def engToHan(self, text):
        self.resetState()
        self.resetStack()
        self.resetBuilder()

        for c in text:
            # get korean character
            hanChar = self.alphabet_to_hangul[c]

            # 초기 상태
            if (self.state is None):
                if (hanChar in self.chosung_list):
                    self.addStack(hanChar)
                    self.chosungState()
                else:
                    self.addBuilder(hanChar)
            # 초성 상태
            elif (self.state == "CHOSUNG"):
                if (hanChar in self.jungsung_list):
                    self.addStack(hanChar)
                    self.jungsungState()
                elif (hanChar in self.chosung_list):
                    self.addBuilder(self.stack.pop())
                    self.addStack(hanChar)
                else:
                    self.addBuilder(self.stack.pop())
                    self.addBuilder(hanChar)
                    self.resetState()
            # 중성 상태
            elif (self.state == "JUNGSUNG"):
                if (hanChar in self.jongsung_list):
                    self.addStack(hanChar)
                    self.jongsungState()
                elif (self.stack[-1]+hanChar in self.double_jungsung_list):
                    self.addStack(self.stack.pop()+hanChar)
                else:
                    self.addBuilder(self.mergeChar())
                    self.addBuilder(hanChar)
                    self.resetState()
            # 종성 상태
            elif (self.state == "JONGSUNG"):
                if (hanChar in self.jungsung_list):
                    prev = self.stack.pop()
                    self.addBuilder(self.mergeChar())
                    self.addStack(prev)
                    self.addStack(hanChar)
                    self.jungsungState()
                elif (self.stack[-1]+hanChar in self.double_jongsung_list):
                    self.addStack(hanChar)
                elif (hanChar in self.chosung_list):
                    self.addBuilder(self.mergeChar())
                    self.addStack(hanChar)
                    self.chosungState()
                else:
                    self.addBuilder(self.mergeChar())
                    self.addBuilder(hanChar)
                    self.resetState()
            else:
                print("do nothing")

        if (len(self.stack) == 1):
            self.addBuilder(self.stack.pop())
        elif (len(self.stack) > 1):
            self.addBuilder(self.mergeChar())
        else:
            print("also do nothing")

        return "".join(self.builder)




def engToHan(text):
    # initialize
    stack_list = []
    builder_list = []
    state = State()
    state.resetState()

    for c in text:
        # get korean character
        hanChar = alphabet_to_hangul[c]

        # 초기 상태
        if (state.state is None):
            if (hanChar in chosung_list):
                stack_list.append(hanChar)
                state.chosungState()
            else:
                builder_list.append(hanChar)
        # 초성 상태
        elif (state.state == "CHOSUNG"):
            if (hanChar in jungsung_list):
                stack_list.append(hanChar)
                state.jungsungState()
            elif (hanChar in chosung_list):
                builder_list.append(stack_list.pop())
                stack_list.append(hanChar)
            else:
                builder_list.append(stack_list.pop())
                builder_list.append(hanChar)
                state.resetState()
        # 중성 상태
        elif (state.state == "JUNGSUNG"):
            if (hanChar in jongsung_list):
                stack_list.append(hanChar)
                state.jongsungState()
            elif (stack_list[-1]+hanChar in double_jungsung_list):
                stack_list.append(stack_list.pop()+hanChar)
            else:
                builder_list.append(mergeChar(stack_list))
                builder_list.append(hanChar)
                state.resetState()
        # 종성 상태
        elif (state.state == "JONGSUNG"):
            if (hanChar in jungsung_list):
                prev = stack_list.pop()
                builder_list.append(mergeChar(stack_list))
                stack_list.append(prev)
                stack_list.append(hanChar)
                state.jungsungState()
            elif (stack_list[-1]+hanChar in double_jongsung_list):
                stack_list.append(hanChar)
            elif (hanChar in chosung_list):
                builder_list.append(mergeChar(stack_list))
                stack_list.append(hanChar)
                state.chosungState()
            else:
                builder_list.append(mergeChar(stack_list))
                builder_list.append(hanChar)
                state.resetState()
        else:
            print("do nothing")

    if (len(stack_list) == 1):
        builder_list.append(stack_list.pop())
    elif (len(stack_list) > 1):
        builder_list.append(mergeChar(stack_list))
    else:
        print("also do nothing")

    return "".join(builder_list)











