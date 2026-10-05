"""Text processing, segmentation, syllable estimation, and function word lexicons."""

from rightforge.text.function_words import (
    ALL_FUNCTION_WORDS,
    AUXILIARY_VERBS,
    CONJUNCTIONS,
    DETERMINERS,
    PREPOSITIONS,
    PRONOUNS,
)
from rightforge.text.segmentation import (
    split_paragraphs,
    split_sentences,
    tokenize_words,
)
from rightforge.text.syllables import count_syllables

__all__ = [
    "ALL_FUNCTION_WORDS",
    "AUXILIARY_VERBS",
    "CONJUNCTIONS",
    "DETERMINERS",
    "PREPOSITIONS",
    "PRONOUNS",
    "count_syllables",
    "split_paragraphs",
    "split_sentences",
    "tokenize_words",
]
