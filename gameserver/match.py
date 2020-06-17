import logging
from typing import Iterable, Optional

# noinspection Mypy
from fuzzywuzzy import process


def match(input_str: str, choices: Iterable[str], threshold: int = 75) -> Optional[str]:
    """
    Matches a given input string against a set of possibilities.
    :param input_str: The input string
    :param choices: Candidates
    :param threshold: Minimum score of best match to return result
    :return: The closest candidate, or None if none were close
    """

    input_str = input_str.lower()
    choice, score = process.extractOne(input_str, choices)
    logging.debug(f"Chose {choice} with score {score}")
    if score >= threshold:
        return choice
    else:
        return None
