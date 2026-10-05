"""Deterministic text segmentation and tokenization primitives."""

import re

# Common English honorifics and abbreviations to avoid false sentence breaks
ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr",
    "vs", "etc", "e.g", "i.e", "vol", "dept", "est",
}

# Regex to identify word tokens (including standard intra-word apostrophes and hyphens)
_WORD_REGEX = re.compile(r"\b[^\W\d_]+(?:['’][^\W\d_]+)?\b", re.UNICODE)


def split_paragraphs(text: str) -> list[str]:
    """Split text into non-empty paragraphs separated by one or more blank lines.

    Args:
        text: Raw text content.

    Returns:
        List of trimmed paragraph strings.
    """
    if not text or not text.strip():
        return []
    raw_paras = re.split(r"\n\s*\n+", text.strip())
    return [p.strip() for p in raw_paras if p.strip()]


def split_sentences(text: str) -> list[str]:
    """Split text into sentences deterministically without splitting on abbreviations or decimal numbers.

    Handles terminal punctuation (. ! ?) optionally followed by closing quotes or parentheses.

    Args:
        text: Raw text content.

    Returns:
        List of trimmed sentence strings.
    """
    if not text or not text.strip():
        return []

    cleaned = text.strip()

    # Pattern matches terminal punctuation [.!?]+ followed by optional closing quotes/brackets,
    # followed by whitespace or string end.
    potential_breaks = list(re.finditer(r"([.!?]+[\"\'”’\)\]]*)(?=\s+|$)", cleaned))
    if not potential_breaks:
        return [cleaned]

    sentences: list[str] = []
    start_idx = 0

    for match in potential_breaks:
        punct_cluster = match.group(1)
        end_punct_idx = match.end()

        # Check if preceding token is an abbreviation (e.g., 'Dr.', 'e.g.')
        # Extract the token immediately preceding the punctuation
        preceding_text = cleaned[start_idx:match.start()].strip()
        last_word_match = re.search(r"([A-Za-z0-9.]+)\s*$", preceding_text)

        is_abbreviation = False
        if last_word_match and punct_cluster.startswith("."):
            token = last_word_match.group(1).lower().rstrip(".")
            if token in ABBREVIATIONS:
                is_abbreviation = True
            elif len(token) == 1 and token.isalpha():
                is_abbreviation = True

        if not is_abbreviation:
            sentence = cleaned[start_idx:end_punct_idx].strip()
            if sentence:
                sentences.append(sentence)
            start_idx = end_punct_idx

    # Capture any remainder
    remainder = cleaned[start_idx:].strip()
    if remainder:
        sentences.append(remainder)

    return sentences if sentences else [cleaned]


def tokenize_words(text: str) -> list[str]:
    """Extract words from text, ignoring standalone punctuation and numerals.

    Args:
        text: Raw text content.

    Returns:
        List of word strings.
    """
    if not text or not text.strip():
        return []
    return _WORD_REGEX.findall(text)
