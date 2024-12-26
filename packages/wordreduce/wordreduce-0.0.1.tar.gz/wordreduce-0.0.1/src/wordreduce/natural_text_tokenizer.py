import re
from typing import List

from unidecode import unidecode


LETTER = re.compile("[a-z ]", re.IGNORECASE)


def tokenize(text: str) -> List[str]:
    _text = unidecode(text).lower()
    letters = [letter for letter in _text if LETTER.match(letter)]
    return "".join(letters).split()