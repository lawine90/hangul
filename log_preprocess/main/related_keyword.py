
from typing import List, Tuple

import re
from itertools import islice, tee


_SPLIT_PATTERN = re.compile(pattern=r"[\s|,|\.]+")


def sliding_log(iterable: List[Tuple], size: int = 2) -> List[str]:
    # structure index
    _ts, _kwd = 0, 1

    # sort array by timestamp & select keyword only
    tmp = [t[_kwd] for t in sorted(iterable, key=lambda x: int(x[_ts]))]

    # sliding
    iterators = tee(tmp, size)
    iterators = [islice(iterator, i, None) for i, iterator in enumerate(iterators)]

    return list(filter(lambda t: t[0] != t[1], zip(*iterators)))


def keyword_type(mkey: str, skey: str) -> str:
    """
    keyword types:
        mod: if n of terms in mkey & skey is same and each diff n of terms is 1, then query type is modification
            e.g. {mkey: "카카오톡 쇼핑하기", skey: "카카오톡 선물하기"}
        add: if n of terms in skey is longer then mkey and skey contains mkey, then query type is addition
            e.g. {mkey: "카카오톡", skey: "카카오톡 선물하기"}
        del: reverse case of query type addition, deletion
            e.g. {mkey: "카카오톡 선물하기", skey: "카카오톡"}
    """

    # split in mkey, skey by '\s,.'
    re_mk = set(re.split(_SPLIT_PATTERN, mkey))
    re_sk = set(re.split(_SPLIT_PATTERN, skey))

    # length of mkey, skey and diffs
    mk_len = len(re_mk)
    sk_len = len(re_sk)
    mk_diff_len = len(re_mk.difference(re_sk))
    sk_diff_len = len(re_sk.difference(re_mk))

    # get refinement
    if mk_len > 1 and mk_len == sk_len and mk_diff_len == 1 and sk_diff_len == 1:
        return 'mod'
    elif sk_len - mk_len == 1 and mk_diff_len == 0 and sk_diff_len == 1:
        return 'add'
    elif mk_len - sk_len == 1 and mk_diff_len == 1 and sk_diff_len == 0:
        return 'del'
    else:
        return ''

