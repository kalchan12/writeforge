"""Unit tests for deterministic text segmentation and tokenization."""

from rightforge.text.segmentation import (
    split_paragraphs,
    split_sentences,
    tokenize_words,
)


def test_split_paragraphs_empty_and_whitespace() -> None:
    assert split_paragraphs("") == []
    assert split_paragraphs("   \n\t   \n  ") == []


def test_split_paragraphs_single_and_multi() -> None:
    single = "This is a single paragraph without breaks."
    assert split_paragraphs(single) == [single]

    multi = "Paragraph one.\n\nParagraph two.\n\n\nParagraph three."
    result = split_paragraphs(multi)
    assert result == ["Paragraph one.", "Paragraph two.", "Paragraph three."]


def test_split_sentences_empty_and_whitespace() -> None:
    assert split_sentences("") == []
    assert split_sentences("   \t  \n  ") == []


def test_split_sentences_standard() -> None:
    text = "First sentence. Second sentence! Third sentence?"
    assert split_sentences(text) == [
        "First sentence.",
        "Second sentence!",
        "Third sentence?",
    ]


def test_split_sentences_without_trailing_punctuation() -> None:
    text = "A simple sentence without end punctuation"
    assert split_sentences(text) == ["A simple sentence without end punctuation"]


def test_split_sentences_abbreviations_and_initials() -> None:
    text = "Dr. Watson visited Mr. Holmes. He was relieved to see him."
    assert split_sentences(text) == [
        "Dr. Watson visited Mr. Holmes.",
        "He was relieved to see him.",
    ]

    initials = "J. K. Rowling wrote books. They are popular."
    assert split_sentences(initials) == [
        "J. K. Rowling wrote books.",
        "They are popular.",
    ]


def test_split_sentences_decimals() -> None:
    text = "The value of pi is approximately 3.14. It is an irrational number."
    assert split_sentences(text) == [
        "The value of pi is approximately 3.14.",
        "It is an irrational number.",
    ]


def test_split_sentences_quotes_and_brackets() -> None:
    text = 'She whispered, "Do not go!" Then she walked away.'
    assert split_sentences(text) == [
        'She whispered, "Do not go!"',
        "Then she walked away.",
    ]


def test_tokenize_words_empty_and_whitespace() -> None:
    assert tokenize_words("") == []
    assert tokenize_words("   \n\t  ") == []


def test_tokenize_words_contractions_and_unicode() -> None:
    text = "Don't panic! It's a naïve résumé with café aromas."
    tokens = tokenize_words(text)
    assert tokens == ["Don't", "panic", "It's", "a", "naïve", "résumé", "with", "café", "aromas"]


def test_tokenize_words_strips_numbers_and_symbols() -> None:
    text = "Section 42: There were 100 apples ($5.50 each) & 3 oranges."
    tokens = tokenize_words(text)
    assert tokens == ["Section", "There", "were", "apples", "each", "oranges"]
