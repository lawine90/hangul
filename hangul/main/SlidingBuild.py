
import itertools
from typing import List, Tuple
from hangul.main.HangulAutomata import HangulAutomata


class Slidingbuild(object):
    """
    자소분리된 한글을 슬라이딩하여 분해, 키를 생성하는 클래스
    """

    def __init__(self):
        self.super_weight = 10.0
        self.minor_weight = 5.0

    # @staticmethod
    # def get_terms(term: str, analyzed_terms: List[dict]) -> List[str]:
    #     """형태소 분석 결과를 참조하여 원본 키워드에 띄어쓰기를 추가하는 함수
    #
    #     :param term: 원본 키워드
    #         e.g. "계란후라이 담요"
    #     :param analyzed_terms: 형태소 분석된 term 및 term이 시작되는 위치
    #         e.g.[
    #             {"str": "계란", "pos": "0"},
    #             {"str": "후라이", "pos": "2"},
    #             {"str": "담요", "pos": "6"},
    #         ]
    #
    #     :return: dha 분석 결과에 따라 split 된 list of terms
    #         e.g. ['계란', '후라이 ', '담요']
    #     """
    #     if len(analyzed_terms) == 0:
    #         return [term]
    #     else:
    #         position_list = [int(d["cpos"]) for d in analyzed_terms]
    #         real_position_list = ([0] + position_list if position_list[0] != 0 else position_list) + [len(term)]
    #
    #         return [term[p1:p2] for p1, p2 in zip(real_position_list[:-1], real_position_list[1:])]

    @staticmethod
    def get_sliding_terms(terms: List[str]) -> List[str]:
        """
        term의 개수가 2개 이상인 경우 중간일치 페어빌드를 위한 infix 텀 생성
        맨 앞의 첫번째 텀은 제거하고 생성한다
        term의 개수가 1개인 경우 후방일치 페어빌드를 위한 suffix 텀 생성
        맨 앞 첫번째 character는 제거하고 생성한다
        :param terms: 입력되는 list of terms
            e.g. ['갤럭시', '워치', '6 ', '클래식 ', '43mm ', '스트랩']
        :return: 앞에서부터 슬라이딩하여 생성된 term list
            e.g. ['워치6 클래식 43mm 스트랩', '6 클래식 43mm 스트랩', '클래식 43mm 스트랩', '43mm 스트랩', '스트랩']
        """
        return [''.join(terms[1:][i:]).lower() for i in range(len(terms[1:]))]

    def create_mainkey_lists(
            self,
            key: str,
            score: float,
            weight_list: List[int]
    ) -> List[Tuple[str, float]]:
        """
        서제스트 페어빌드 로직
        """

        ### 0. 한글 유틸 선언 및 base 자소분해
        func_hp = HangulAutomata()
        #base_terms = self.get_terms(term=key, analyzed_terms=analyzed_terms)
        base_terms = key.split(' ')
        jamo_terms = [func_hp.hanToJamo(t) for t in base_terms]

        ### 1. 초성일치
        base_chosung = func_hp.getChosung(text=key)

        if base_chosung is not None:
            chosung = base_chosung.lower()
            chosung_default_score = weight_list[3] * score * self.super_weight
            chosung_default_result = [(chosung, chosung_default_score)]

            _chosung = chosung.replace(" ", "")
            _chosung_default_result = [(_chosung, chosung_default_score)]
        else:
            chosung_default_result = []
            _chosung_default_result = []

        ### 2. 전방일치 prefix matching
        front_key = ''.join(jamo_terms).lower()
        front_default_score = weight_list[0] * score * self.super_weight
        front_default_result = [(front_key, front_default_score)]

        _front_key = front_key.replace(" ", "")
        _front_default_result = [(_front_key, front_default_score)]

        # 중간 저장
        temp_result = front_default_result + _front_default_result + chosung_default_result + _chosung_default_result

        ### 3. 중간일치 infix matching
        infix_keys = self.get_sliding_terms(terms=jamo_terms)
        infix_default_score = weight_list[1] * score * self.super_weight
        infix_default_result = [(infix_key, infix_default_score) for infix_key in infix_keys]

        _infix_keys = [infix_key.replace(" ", "") for infix_key in infix_keys]
        _infix_default_result = [(_infix_key, infix_default_score) for _infix_key in _infix_keys]

        ### 4. 후방일치 term의 개수가 1개일때만 생성
        if len(jamo_terms) == 1:
            suffix_keys = [func_hp.hanToJamo(t) for t in self.get_sliding_terms(terms=list(key))]
            suffix_default_score = weight_list[2] * score * self.super_weight
            suffix_default_result = [(suffix_key, suffix_default_score) for suffix_key in suffix_keys]

            _suffix_keys = [suffix_key.replace(" ", "") for suffix_key in suffix_keys]
            _suffix_default_result = [(_suffix_key, suffix_default_score) for _suffix_key in _suffix_keys]

            # return
            return temp_result + infix_default_result + _infix_default_result + \
                suffix_default_result + _suffix_default_result
        else:
            return temp_result + infix_default_result + _infix_default_result

    @staticmethod
    def create_key_sliding(input_pair: Tuple[str, float]) -> List[Tuple[str, float]]:
        """
        create_suggest_list에서 생성된 (key, score) 페어에서 key를 character 단위로 sliding하여 여러개의 key, score 페어를 생성
        :param input_pair: create_suggest_list에서 생성된 초성, 전방, 중간, 후방일치의 key, score 페어
            e.g. ("ㄱㅐㄹㄹㅓㄱㅅㅣ", 20)
        :return: key를 맨 처음 character부터 sliding한 key, score의 list
            e.g. [
                ('ㄱ', 20),
                ('ㄱㅐ', 20),
                ('ㄱㅐㄹ', 20),
                ('ㄱㅐㄹㄹ', 20),
                ('ㄱㅐㄹㄹㅓ', 20),
                ('ㄱㅐㄹㄹㅓㄱ', 20),
                ('ㄱㅐㄹㄹㅓㄱㅅ', 20),
                ('ㄱㅐㄹㄹㅓㄱㅅㅣ', 20)
            ]
        """
        temp_key, temp_score = input_pair
        return [(temp_key[:i+1], temp_score) for i in range(len(temp_key))]

    def create_mainkey(
            self,
            key: str,
            # analyzed_terms: List[dict],
            score: float,
            weight_list: List[int]
    ) -> List[Tuple[str, float]]:
        """
        create_suggest_list에서 생성된 mainkey, score 페어에 create_key_sliding를 적용,
        여러개의 mainkey, score 페어를 생성하고 중복이 제거된 최종 mainkey, score 페어를 return
        :param key: 입력 키워드
        # :param analyzed_terms: dha 분석 결과
        :param score: 스코어
        :param weight_list: 전방/중간/후방/초성 가중치
        :return:
        """
        if len(key.replace(" ", "")) == 0:
            return []
        else:
            temp_list = self.create_mainkey_lists(
                key=key,
                # analyzed_terms=analyzed_terms,
                score=score,
                weight_list=weight_list
            )

            return list(set(
                itertools.chain(*[self.create_key_sliding(input_pair=t) for t in temp_list])
            ))
