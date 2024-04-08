
import ahocorasick


def create_trie(
        spark: SparkSession,
        paths: List[str],
        col_name: str = "keyword"
) -> ahocorasick.Automaton:
    """hdfs에서 data read 후 col_name의 키워드로 trie return
    :param spark: spark
    :param paths: hdfs path
    :param col_name: 패턴으로 사용할 column name
    :return: 아호코라식 trie
    """
    # read df
    dfs = []
    for p in paths:
        dfs.append(read(spark=spark, path=p, file_format="json").select(col_name))

    # collect as pattern list
    patterns = reduce(DataFrame.union, dfs).distinct() \
        .rdd.map(lambda r: r[0]).collect()

    # create trie
    a = ahocorasick.Automaton()
    for i, k in enumerate(patterns):
        a.add_word(k, (i, k))
    a.make_automaton()

    return a


def aho_idx(
        query: str,
        trie: ahocorasick.Automaton
) -> Tuple[List[int], List[int]]:
    """아호코라식 알고리즘으로 query에 포함된 패턴의 위치를 return
    :param query: 인덱스를 검색할 입력 쿼리
    :param trie: 아호코라식 trie
    :return: (
        List[int]: 포함된 패턴들이 등장하는 start index
        List[ind]: 포함된 패턴들이 등장하는 end index
    )
    """
    index_tuple = [
        (end_idx - len(key) + 1, end_idx)
        for end_idx, (_, key) in trie.iter(query)
    ]

    if len(index_tuple) != 0:
        return (
            [i[0] for i in index_tuple],
            [i[1] for i in index_tuple],
        )
    else:
        return [], []


def exclude_xfix(
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
    index_tuple = aho_idx(query=query, trie=trie)
    query_len = len(query) - 1  # 키워드의 길이는 마지막 인덱스 +1이므로 길이에서 -1

    # 헷갈리는 포인트!
    # prefix/suffix/infix가 포함된 경우는 제거를 하기 위함
    # .filter() 적용을 위해 포함된 경우 False를 return
    if fix_type == "prefix":
        is_exist = False if (0 in index_tuple[0]) else True
    elif fix_type == "suffix":
        is_exist = False if query_len in index_tuple[1] else True
    elif fix_type == "infix":
        is_exist = False if len(index_tuple[0]) != 0 else True
    elif fix_type == "exact":
        is_exist = False if (0 in index_tuple[0]) and (query_len in index_tuple[1]) else True
    else:
        raise "fix_type should be one of 'prefix', 'suffix', 'infix'"

    return is_exist
