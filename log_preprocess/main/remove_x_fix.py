
import ahocorasick
from typing import List, Tuple


def create_trie(patterns: List[str]) -> ahocorasick.Automaton:
    """
    :param patterns: 트라이를 만들 패턴
    :return: 아호코라식 trie
    """
    # create trie
    a = ahocorasick.Automaton()
    for i, k in enumerate(patterns):
        a.add_word(k, (i, k))
    a.make_automaton()

    return a


def find_all(
        query: str,
        trie: ahocorasick.Automaton
) -> List[Tuple[int, int, str]]:
    """아호코라식 알고리즘으로 query에 포함된 패턴의 위치를 return
    :param query: 인덱스를 검색할 입력 쿼리
    :param trie: 아호코라식 trie
    :return: [
        int: 패턴의 시작 인덱스
        int: 패턴의 종료 인덱스
        str: 찾아낸 패턴
    ]
    """
    found = [
        (end_idx - len(key) + 1, end_idx, key)
        for end_idx, (_, key) in trie.iter(query)
    ]

    if len(found) != 0:
        return found
    else:
        return [(-1, -1, '')]


def remove_x_fix(
        query: str,
        trie: ahocorasick.Automaton,
        fix_type: str
) -> bool:
    """
    :param query: 인덱스를 검색할 입력 쿼리
    :param trie: aho-corasick trie 객체
    :param fix_type: 매칭 타입 (prefix, infix, suffix, exact 중 하나)
    :return: 매칭 여부
    """
    index_tuple = find_all(query=query, trie=trie)
    start_index = [t[0] for t in index_tuple]
    end_index = [t[1] for t in index_tuple]
    query_len = len(query) - 1  # 키워드의 길이는 마지막 인덱스 +1이므로 길이에서 -1

    # 헷갈리는 포인트!
    # prefix/suffix/infix가 포함된 경우는 제거를 하기 위함
    # .filter() 적용을 위해 포함된 경우 False를 return
    if fix_type == "prefix":
        is_exist = False if (0 in start_index) else True
    elif fix_type == "suffix":
        is_exist = False if query_len in end_index else True
    elif fix_type == "infix":
        is_exist = False if len(index_tuple) != 0 else True
    elif fix_type == "exact":
        is_exist = False if (0 in start_index) and (query_len in end_index) else True
    else:
        raise "fix_type should be one of 'prefix', 'suffix', 'infix'"

    return is_exist


def find_x_fix(
        query: str,
        trie: ahocorasick.Automaton,
        fix_type: str
) -> bool:
    """
    :param query: 인덱스를 검색할 입력 쿼리
    :param trie: aho-corasick trie 객체
    :param fix_type: 매칭 타입 (prefix, infix, suffix, exact 중 하나)
    :return: 매칭 여부
    """
    return not remove_x_fix(query=query, trie=trie, fix_type=fix_type)
