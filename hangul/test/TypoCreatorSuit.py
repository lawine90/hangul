
import unittest
from pprint import pprint
import pandas as pd
from hangul.main.TypoCreator import TypoCreator


if __name__ == "__main__":
    # class
    typo_creator = TypoCreator()

    # test keywords
    txt = "스타벅스"

    print(pd.DataFrame(typo_creator.typo_strings(text=txt)))
