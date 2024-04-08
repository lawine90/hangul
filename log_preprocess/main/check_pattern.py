
import re
from unicodedata import normalize


_korean_domain_pattern = re.compile(r"""[가-힣ㄱ-ㅎㅏ-ㅣ]+\.((com)|(net)|(biz)|(kr)|(cn)|(de)|(to)|(info))""")
_all_special_character_pattern = re.compile(r"""^[!@#$%^&*()_+\-={}\[\]:\";|~'`/.,?><]+$""")
_torrent_patterns = [re.compile(p) for p in [r"""\d{6}.*토[렌랜][트토]""", r"""토[렌랜][트토].*\d{6}"""]]
_special_character_infix_patterns = [re.compile(p) for p in [
    r"""[\[^{"《》『★』∥■△▶◀◆○●☞↓─〒♧☆♥♡♣♪※☆「」`\]]""", r"""!{3}""", r"""\*{3}""", r"""&#""", r"\uFEFF",
    r"""[\uFF01-\uFF60]""",  # 전각 영문+숫자+특수기호 범위  (뒤로 일본어와 한글이 있지만 추가 처리하진 않음)
    r"""[\u0000-\u0019]""", r"""[\u0080-\u00A0]""", r"""\u3000""", r"""[\u2000-\u206F]"""
]]
_phon_number_with_korean_pattern = re.compile(r"""^[가-힣 ]{2,}:? ?(\d{2,3}[^\d\w가-힣*])?\d{3,4}[^\d\w가-힣*]\d{4}$""")
_single_korean_pattern = re.compile(r"""[ㄱ-ㅎㅏ-ㅣ]""")
_unicode_abusing_remove_characters_pattern = re.compile(r"""[ㆍ]+""")
_unicode_abusing_check_boundary_pattern = re.compile(
    r"""^[\u1100-\u11FF\u302E-\u302F\u3131-\u318F\u3200-\u321F\u3260-\u327E\uA960-\uA97F\uAC00-\uD7FB\uFFA0-\uFFDF\d]+$""")
_phon_number_v2 = [re.compile(p) for p in [r"""1[568]\d{2}\D?\d{4}""", r"""(02|0[1-8]\d{1})\D?\d{3,4}\D?\d{4}"""]]
_car_number = re.compile(r"""^\d{2} ?[가-힣] ?\d{4}$""")

# 매칭 되지 않는 (), {}, [], <> 키워드
_unmatched_brackets = [re.compile(p) for p in [
    r"""([\[][^\]]*$|[{][^}]*$|[\(][^)]*$|[<][^>]*$)""",
    r"""(^[^\[]*[\]]|^[^{]*[}]|^[^\(]*[\)]|^[^<]*[>])"""
]]

# 택배 운송장 번호
_tracking_number = [re.compile(p) for p in [
    r"""(택배|통운|로지스|송장|배송)+.*[0-9\- ]{7}""",
    r"""[0-9\- ]{7}.*(택배|통운|로지스|송장|배송)+"""
]]


# functions...
def unicode_normalize(q: str) -> str:
    return normalize("NFKC", q)


def is_korean_domain(q: str) -> bool:
    """한글 도메인 여부 체크.
        e.g. "카카오.com"
    """
    return bool(_korean_domain_pattern.match(q))


def is_tracking_number(q: str) -> bool:
    """택배송장 패턴 체크. (숫자 7자 이상?)
        e.g. "택배 1234567"
    """
    return any([
        bool(_p.match(unicode_normalize(q)))
        for _p in _tracking_number
    ])


def is_phone_number_v2(q: str) -> bool:
    """전화번호 패턴 체크.
        e.g. "010-4030-1306"
    """
    return any([
        bool(_p.match(unicode_normalize(q)))
        for _p in _phon_number_v2
    ])


def is_car_number(q: str) -> bool:
    """자동차 등록번호 패턴
        e.g. "51 주 4184"
    """
    return bool(_car_number.match(q))


def is_phone_number_with_korean(q: str) -> bool:
    """한국어가 포함된 전화번호 패턴
        e.g. "고객센터: 1577-3754"
    """
    return bool(_phon_number_with_korean_pattern.match(unicode_normalize(q)))


def is_single_korean(q: str) -> bool:
    """자음, 모음만 있는 패턴 체크
        e.g. "ㅋㅋㅋ"
    """
    return bool(_single_korean_pattern.match(q))


def is_special_character(q: str) -> bool:
    """특정한 패턴의 특수기호를 포함한 패턴
        e.g. "!!!세일!!!"
    """
    return any([
        bool(_all_special_character_pattern.match(q)),
        any([_p.match(q) for _p in _special_character_infix_patterns])
    ])


def is_torrent_pattern(q: str) -> bool:
    """토렌트 패턴???
        e.g. "토렌트 123456"
    """
    return any([_p.match(q) for _p in _torrent_patterns])


def is_unicode_abusing(q: str) -> bool:
    """...?"""
    cleaned_q = re.sub(_unicode_abusing_remove_characters_pattern, "", q)
    nomalized_q = unicode_normalize(cleaned_q)

    return (cleaned_q != nomalized_q) and bool(_unicode_abusing_check_boundary_pattern.match(nomalized_q))


def is_unmatched_brackets(q: str) -> bool:
    """짝이 맞지 않는 괄호 패턴
        e.g. "세일) 카카오프렌즈"
    """
    return any([_p.match(q) for _p in _unmatched_brackets])

