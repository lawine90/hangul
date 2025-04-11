
# from dill.source import getsource
# print(getsource(TypoCreator))
import math
from typing import List
from itertools import chain, combinations
from hangul.main.HangulAutomata import HangulAutomata


class TypoCreator:
    # keyboard characters distance
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

    def __init__(self, distance_criteria: float = 1.5):
        """
        :param distance_criteria: character distance criteria
            e.g. 'ㅁ' and 'ㄴ' distance is 1
        """
        # initialize
        self.distance_criteria = distance_criteria

        # hangul preprocessor
        self.hp = HangulAutomata()

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

    # replace character by index then compose jamo to hangul
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
            self.hp.engToHan(
                text=self.hp.hanToEng(text=keyword[:index] + rc + keyword[index + 1:]),
                ignore_kor=True
            )
            for rc in replace_chars
        ]

    # create typo
    def typo_strings(self, text: str) -> List[str]:
        """
        :param text: normal keyword to create typo
            e.g. 스타벅스
        :return: list of created typos
            e.g. ['쓰타벅스', '르타벅스', '흐타벅스', ...]
        """
        kor_decomposed = self.hp.hanToJamo(text)
        typo_candidates = []

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
