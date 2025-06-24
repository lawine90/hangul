
# from dill.source import getsource
# print(getsource(TypoCreator))
import math
from typing import List
from itertools import chain, combinations, product
from hangul.main.HangulAutomata import HangulAutomata


class KorTypoCreator(HangulAutomata):
    def __init__(self, distance_criteria: float = 1.5, joiner: str = "___"):
        """
        :param distance_criteria: character distance criteria
            e.g. 'ㅁ' and 'ㄴ' distance is 1
        """
        super().__init__()

        ### about keyboard distance
        # keyboard distance criteria
        self.distance_criteria = distance_criteria

        # ja/mo coordinates
        # (horizontal, vertical, shift)
        self.ja_coordinates = {
            'ㅂ': (0, 0, 0),
            'ㅃ': (0, 0, 1),
            'ㅈ': (0, 1, 0),
            'ㅉ': (0, 1, 1),
            'ㄷ': (0, 2, 0),
            'ㄸ': (0, 2, 1),
            'ㄱ': (0, 3, 0),
            'ㄲ': (0, 3, 1),
            'ㅅ': (0, 4, 0),
            'ㅆ': (0, 4, 1),

            'ㅁ': (1, 0, 0),
            'ㄴ': (1, 1, 0),
            'ㅇ': (1, 2, 0),
            'ㄹ': (1, 3, 0),
            'ㅎ': (1, 4, 0),

            'ㅋ': (2, 0, 0),
            'ㅌ': (2, 1, 0),
            'ㅊ': (2, 2, 0),
            'ㅍ': (2, 3, 0),
        }
        self.mo_coordinates = {
            'ㅛ': (0, 5, 0),
            'ㅕ': (0, 6, 0),
            'ㅑ': (0, 7, 0),
            'ㅐ': (0, 8, 0),
            'ㅒ': (0, 8, 1),
            'ㅔ': (0, 9, 0),
            'ㅖ': (0, 9, 1),

            'ㅗ': (1, 5, 0),
            'ㅓ': (1, 6, 0),
            'ㅏ': (1, 7, 0),
            'ㅣ': (1, 8, 0),

            'ㅠ': (2, 4, 0),
            'ㅜ': (2, 5, 0),
            'ㅡ': (2, 6, 0),
        }

        # ja/mo distance
        self.ja_distances = [
            (char1, char2, self.keyboard_distance(char1, char2))
            for char1, char2 in combinations(self.ja_coordinates.keys(), 2)
            if self.keyboard_distance(char1, char2) <= self.distance_criteria
        ]
        self.mo_distances = [
            (char1, char2, self.keyboard_distance(char1, char2))
            for char1, char2 in combinations(self.mo_coordinates.keys(), 2)
            if self.keyboard_distance(char1, char2) <= self.distance_criteria
        ]

        ### about phonetic distance
        ### IPA 초성/중성/종성 리스트
        # self.ipa_chosung_map = {
        #     'ㄱ': 'k', 'ㄲ': 'kʼ', 'ㄴ': 'n', 'ㄷ': 't', 'ㄸ': 'tʼ', 'ㄹ': 'ɾ', 'ㅁ': 'm',
        #     'ㅂ': 'p', 'ㅃ': 'pʼ', 'ㅅ': 's', 'ㅆ': 'sʼ', 'ㅇ': 'ŋ', 'ㅈ': 'tɕ',
        #     'ㅉ': 'tɕʼ', 'ㅊ': 'tɕʰ', 'ㅋ': 'kʰ', 'ㅌ': 'tʰ', 'ㅍ': 'pʰ', 'ㅎ': 'h'
        # }
        self.ipa_chosung_map = {
            'ㄱ': 'k', 'ㄲ': 'kʰ', 'ㄴ': 'n', 'ㄷ': 't', 'ㄸ': 'tʰ', 'ㄹ': 'ɾ', 'ㅁ': 'm',
            'ㅂ': 'p', 'ㅃ': 'pʰ', 'ㅅ': 's', 'ㅆ': 'sʼ', 'ㅇ': 'ŋ', 'ㅈ': 'tɕ',
            'ㅉ': 'tɕʼ', 'ㅊ': 'tɕʰ', 'ㅋ': 'kʰ', 'ㅌ': 'tʰ', 'ㅍ': 'pʰ', 'ㅎ': 'h'
        }
        # self.ipa_jungsung_map = {
        #     'ㅏ': 'a', 'ㅐ': 'ɛ', 'ㅑ': 'ja', 'ㅒ': 'jɛ', 'ㅓ': 'ʌ',
        #     'ㅔ': 'e', 'ㅕ': 'jʌ', 'ㅖ': 'je', 'ㅗ': 'o', 'ㅗㅏ': 'wa',
        #     'ㅗㅐ': 'wɛ', 'ㅗㅣ': 'we', 'ㅛ': 'jo', 'ㅜ': 'u', 'ㅜㅓ': 'wʌ',
        #     'ㅜㅔ': 'we', 'ㅜㅣ': 'wi', 'ㅠ': 'ju', 'ㅡ': 'ɯ', 'ㅡㅣ': 'ɰi', 'ㅣ': 'i'
        # }
        self.ipa_jungsung_map = {
            'ㅏ': 'a', 'ㅐ': 'e', 'ㅑ': 'ja', 'ㅒ': 'je', 'ㅓ': 'ʌ',
            'ㅔ': 'e', 'ㅕ': 'jʌ', 'ㅖ': 'je', 'ㅗ': 'o', 'ㅗㅏ': 'wa',
            'ㅗㅐ': 'we', 'ㅗㅣ': 'we', 'ㅛ': 'jo', 'ㅜ': 'u', 'ㅜㅓ': 'wʌ',
            'ㅜㅔ': 'we', 'ㅜㅣ': 'wi', 'ㅠ': 'ju', 'ㅡ': 'ɯ', 'ㅡㅣ': 'ɰi', 'ㅣ': 'i'
        }
        # self.ipa_jongsung_map = {
        #     '': '', 'ㄱ': 'k̚', 'ㄲ': 'k̚', 'ㄱㅅ': 'k̚', 'ㄴ': 'n', 'ㄴㅈ': 'n',
        #     'ㄴㅎ': 'n', 'ㄷ': 't̚', 'ㄹ': 'l', 'ㄹㄱ': 'lk̚', 'ㄹㅁ': 'lm', 'ㄹㅂ': 'lp',
        #     'ㄹㅅ': 'ls', 'ㄹㅌ': 'lt̚', 'ㄹㅍ': 'lp̚', 'ㄹㅎ': 'lh', 'ㅁ': 'm', 'ㅂ': 'p̚',
        #     'ㅂㅅ': 'p̚s', 'ㅅ': 't̚', 'ㅆ': 't̚', 'ㅇ': 'ŋ', 'ㅈ': 't̚', 'ㅊ': 't̚',
        #     'ㅋ': 'k̚', 'ㅌ': 't̚', 'ㅍ': 'p̚', 'ㅎ': 't̚'
        # }
        self.ipa_jongsung_map = {
            '': '', 'ㄱ': 'k̚', 'ㄲ': 'k̚', 'ㄱㅅ': 'k̚', 'ㄴ': 'n', 'ㄴㅈ': 'n',
            'ㄴㅎ': 'n', 'ㄷ': 't̚', 'ㄹ': 'l', 'ㄹㄱ': 'k̚', 'ㄹㅁ': 'm', 'ㄹㅂ': 'p̚',
            'ㄹㅅ': 'ls', 'ㄹㅌ': 'lt̚', 'ㄹㅍ': 'p̚', 'ㄹㅎ': 'l', 'ㅁ': 'm', 'ㅂ': 'p̚',
            'ㅂㅅ': 'p̚', 'ㅅ': 't̚', 'ㅆ': 't̚', 'ㅇ': 'ŋ', 'ㅈ': 't̚', 'ㅊ': 't̚',
            'ㅋ': 'k̚', 'ㅌ': 't̚', 'ㅍ': 'p̚', 'ㅎ': 't̚'
        }

        # IPA 역매핑 테이블 (1:N 맵핑)
        self.rev_ipa_chosung_map = {
            v: [k_ for k_, v_ in self.ipa_chosung_map.items() if v_ == v]
            for k, v in self.ipa_chosung_map.items()
        }
        self.rev_ipa_jungsung_map = {
            v: [k_ for k_, v_ in self.ipa_jungsung_map.items() if v_ == v]
            for k, v in self.ipa_jungsung_map.items()
        }
        self.rev_ipa_jongsung_map = {
            v: [k_ for k_, v_ in self.ipa_jongsung_map.items() if v_ == v]
            for k, v in self.ipa_jongsung_map.items()
        }

        # ipa 변환시 사용할 join/spliter
        self.joiner = joiner

    # keyboard distance: characters distance
    def keyboard_distance(self, char1: str, char2: str) -> float:
        """
        :param char1: first character (ja or mo not digit or eng)
        :param char2: second character (ja or mo not digit or eng)
        :return: distance between two characters
        """
        # first character's coordinates
        if char1 in self.ja_coordinates.keys():
            coord1 = self.ja_coordinates[char1]
        elif char1 in self.mo_coordinates.keys():
            coord1 = self.mo_coordinates[char1]
        else:
            raise ValueError(f"first character {char1} is invalid")

        # second character's coordinates
        if char2 in self.ja_coordinates.keys():
            coord2 = self.ja_coordinates[char2]
        elif char2 in self.mo_coordinates.keys():
            coord2 = self.mo_coordinates[char2]
        else:
            raise ValueError(f"second character {char2} is invalid")

        return round(math.sqrt(sum([abs(c1 - c2) for c1, c2 in zip(coord1, coord2)])), 2)

    # keyboard distance: replace character by index then compose jamo to hangul
    def replace_by_index_and_compose(
            self,
            keyword: str,
            index: int,
            replace_chars: List[str]
    ) -> List[str]:
        """
        :param keyword: decomposed korean
            e.g. "ㅅㅡㅌㅏㅂㅓㄱㅅㅡ"
        :param index: from decomposed korean, select index to replace
            e.g. 0
        :param replace_chars: character to replace
            e.g. ['ㅁ', 'ㄴ']
        :return: list of and miss typed and composed hangul
            e.g. ['므타벅스', '느타벅스']
        """
        return [
            self.jamoToHan(text=keyword[:index] + rc + keyword[index + 1:])
            for rc in replace_chars
        ]

    # keyboard distance: create keyboard typo
    def typo_strings(self, text: str) -> List[str]:
        """
        :param text: normal keyword to create typo
            e.g. 스타벅스
        :return: list of created typos
            e.g. ['쓰타벅스', '르타벅스', '흐타벅스', ...]
        """
        # decompose korean keywords to jamo
        kor_decomposed = self.hanToJamo(text)

        # add last character ommited typo
        if kor_decomposed[-1] in self.jongsung_list:
            typo_candidates = []
        else:
            typo_candidates = [self.jamoToHan(text=kor_decomposed[:-1])]

        for i, char in enumerate(kor_decomposed):
            if char in self.ja_coordinates.keys():
                # select 'ja' near typo candidates
                ja_typo_characters = list(chain(*[
                    [d[1] for d in self.ja_distances if d[0] == char],
                    [d[0] for d in self.ja_distances if d[1] == char]
                ]))

                typo_candidates.extend(self.replace_by_index_and_compose(
                    keyword=kor_decomposed,
                    index=i,
                    replace_chars=ja_typo_characters
                ))
            elif char in self.mo_coordinates.keys():
                # select 'mo' near typo candidates
                mo_typo_characters = list(chain(*[
                    [d[1] for d in self.mo_distances if d[0] == char],
                    [d[0] for d in self.mo_distances if d[1] == char]
                ]))

                typo_candidates.extend(self.replace_by_index_and_compose(
                    keyword=kor_decomposed,
                    index=i,
                    replace_chars=mo_typo_characters
                ))

            else:
                print(f"character: {char}")

        return typo_candidates

    # phonetic distance: convert hangul to IPA
    #   IPA?: International Phonetic Alphabet
    def han_to_ipa(self, text: str) -> str:
        result = []
        for char in text:
            if '가' <= char <= '힣':
                decomposed = self.hanToJamo(text=char)

                # chosung
                ipa_cho = self.ipa_chosung_map.get(decomposed[0])

                # jungsung
                decomposed = decomposed[1:] # 초성을 뺀 나머지 문자열
                ipa_jung, jung = [
                    (self.ipa_jungsung_map.get(decomposed[:i+1]), decomposed[:i+1])
                    for i, c in enumerate(decomposed)
                    if decomposed[:i+1] in self.ipa_jungsung_map.keys()
                ][-1]

                # jongsung
                decomposed = decomposed.replace(jung, '')
                ipa_jong = self.ipa_jongsung_map.get(decomposed) if decomposed != '' else ''

                result.append(f"{ipa_cho}{ipa_jung}{ipa_jong}".strip())
            else:
                result.append(char)
        return self.joiner.join(result)

    # phonetic distance: split ipa characters as cho/jung/jong
    def split_ipa_token(self, tokens: str):
        ipa_tokens = tokens

        # select ipa chosung token
        ipa_cho = [
            ipa_tokens[:i+1]
            for i, c in enumerate(ipa_tokens)
            if ipa_tokens[:i+1] in self.rev_ipa_chosung_map.keys()
        ][-1]

        # select ipa jungsung token (replace only first occurrence)
        ipa_tokens = ipa_tokens.replace(ipa_cho, '', 1)

        ipa_jung = [
            ipa_tokens[:i+1]
            for i, c in enumerate(ipa_tokens)
            if ipa_tokens[:i+1] in self.rev_ipa_jungsung_map.keys()
        ][-1]

        # select ipa jongsung token (replace only first occurrence)
        ipa_jong = ipa_tokens.replace(ipa_jung, '', 1)

        return ipa_cho, ipa_jung, ipa_jong

    # phonetic distance: convert ipa characters to jamo then hangul
    def ipa_to_han(self, ipa_string: str) -> List[str]:
        self.resetState()
        self.resetStack()
        self.resetBuilder()

        tokens = ipa_string.strip().split(self.joiner)
        result = []

        for token in tokens:
            if not token.isdigit() and len(token) >= 2:
                # split ipa tokens
                ipa_cho, ipa_jung, ipa_jong = self.split_ipa_token(token)

                # add chosung & jungsung to builder
                chosung_codes = [self.chosung_indices[c] for c in self.rev_ipa_chosung_map[ipa_cho]]
                jungsung_codes = [self.jungsung_indices[c] for c in self.rev_ipa_jungsung_map[ipa_jung]]
                jongsung_codes = [self.jongsung_indices[c] for c in self.rev_ipa_jongsung_map[ipa_jong]]

                # rev_ipa mapping이 1:N 맵핑이므로 변환한 결과를 flatten
                result.append([
                    chr(((cho * 21) + jung) * 28 + jong + self.start_code)
                    for cho, jung, jong in product(*[chosung_codes, jungsung_codes, jongsung_codes])
                ])
            else:
                result.append([token])

        return [''.join(t) for t in product(*result)]


