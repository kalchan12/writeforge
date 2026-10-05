"""Deterministic syllable estimation for English words."""

import re

# Regex matching groups of vowels
_VOWEL_GROUPS = re.compile(r"[aeiouy]+", re.IGNORECASE)


def count_syllables(word: str) -> int:
    """Estimate the syllable count of a word using deterministic phonetic rules.

    Args:
        word: A single word string.

    Returns:
        Estimated syllable count (integer >= 1 for non-empty words).
    """
    clean_word = re.sub(r"[^a-zA-Z]", "", word).lower()
    if not clean_word:
        return 0

    if len(clean_word) <= 3:
        return 1

    # Count vowel groups
    vowel_matches = _VOWEL_GROUPS.findall(clean_word)
    count = len(vowel_matches)

    # Adjust for silent 'e' at the end (e.g. 'make', 'game', but not 'me', 'the')
    # Words ending in '-le' with a preceding consonant (table, candle) pronounce /əl/,
    # so the 'e' is not silent; it contributes to that second syllable and was already counted.
    # Words ending in 'ee' or 'ye' (free, tree) form a single vowel group.
    if clean_word.endswith("e") and not clean_word.endswith("le") and not clean_word.endswith("ee"):
        if count > 1:
            count -= 1

    # Adjust for '-ed' past tense suffix (e.g., 'looked' = 1, but 'wanted', 'needed' = 2)
    if clean_word.endswith("ed") and len(clean_word) > 3:
        if clean_word[-3] not in ("t", "d"):
            if count > 1:
                count -= 1

    # Adjust for '-es' plural/third-person suffix (e.g. 'likes' = 1, but 'watches', 'kisses' = 2)
    if clean_word.endswith("es") and len(clean_word) > 3:
        if clean_word[-3] not in ("s", "x", "z", "c", "h"):
            if count > 1:
                count -= 1

    return max(1, count)
