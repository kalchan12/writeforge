"""Text processing, segmentation, syllable estimation, and function word lexicons."""

from rightforge.text.ai_markers import (
    AI_SIGNATURE_PHRASES,
    AI_SIGNATURE_WORDS,
    AI_TRANSITION_STARTERS,
    detect_ai_lexical_markers,
)
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
    "AI_SIGNATURE_PHRASES",
    "AI_SIGNATURE_WORDS",
    "AI_TRANSITION_STARTERS",
    "detect_ai_lexical_markers",
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
