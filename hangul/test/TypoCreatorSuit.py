
import unittest
from pprint import pprint
import pandas as pd
from hangul.main.TypoCreator import KorTypoCreator


if __name__ == "__main__":
    # class
    typo_creator = KorTypoCreator()

    # test keywords
    txt = "스타벅스"

    # keyboard typo
    print(pd.DataFrame(typo_creator.typo_strings(text=txt)))

    # phonetic typo
    ipa_str = typo_creator.han_to_ipa(text=txt)
    print(f"IPA string: {ipa_str}")
    print(pd.DataFrame(typo_creator.ipa_to_han(ipa_string=ipa_str)))
