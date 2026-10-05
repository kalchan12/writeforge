"""Unit tests for BasicTextAnalyzer."""

from rightforge.analysis import BasicTextAnalyzer
from rightforge.models import Document


def test_analyze_empty_text() -> None:
    analyzer = BasicTextAnalyzer()
    res = analyzer.analyze("")

    assert res.metrics["character_count"].value == 0
    assert res.metrics["non_whitespace_char_count"].value == 0
    assert res.metrics["word_count"].value == 0
    assert res.metrics["sentence_count"].value == 0
    assert res.metrics["paragraph_count"].value == 0
    assert res.metrics["avg_words_per_sentence"].value == 0.0
    assert res.metrics["avg_chars_per_word"].value == 0.0
    assert res.metrics["min_sentence_length"].value == 0
    assert res.metrics["max_sentence_length"].value == 0
    assert res.metrics["sentence_length_std_dev"].value == 0.0


def test_analyze_single_sentence() -> None:
    analyzer = BasicTextAnalyzer()
    text = "The quick brown fox jumps."
    res = analyzer.analyze(text)

    # Word tokens: ["The", "quick", "brown", "fox", "jumps"] -> 5 words
    # Characters: len("The quick brown fox jumps.") = 26
    # Non-whitespace: 26 - 4 spaces = 22
    # Word character lengths: 3 + 5 + 5 + 3 + 5 = 21 -> 21 / 5 = 4.2
    assert res.metrics["character_count"].value == 26
    assert res.metrics["non_whitespace_char_count"].value == 22
    assert res.metrics["word_count"].value == 5
    assert res.metrics["sentence_count"].value == 1
    assert res.metrics["paragraph_count"].value == 1
    assert res.metrics["avg_words_per_sentence"].value == 5.0
    assert res.metrics["avg_chars_per_word"].value == 4.2
    assert res.metrics["min_sentence_length"].value == 5
    assert res.metrics["max_sentence_length"].value == 5
    assert res.metrics["sentence_length_std_dev"].value == 0.0


def test_analyze_multiple_sentences_distribution() -> None:
    analyzer = BasicTextAnalyzer()
    # Sentence 1: 4 words ("One two three four.")
    # Sentence 2: 2 words ("Five six.")
    # Sentence lengths: [4, 2], mean = 3.0, variance = ((4-3)^2 + (2-3)^2)/2 = 1.0, std_dev = 1.0
    text = "One two three four. Five six."
    res = analyzer.analyze(text)

    assert res.metrics["word_count"].value == 6
    assert res.metrics["sentence_count"].value == 2
    assert res.metrics["avg_words_per_sentence"].value == 3.0
    assert res.metrics["min_sentence_length"].value == 2
    assert res.metrics["max_sentence_length"].value == 4
    assert res.metrics["sentence_length_std_dev"].value == 1.0


def test_analyze_multiple_paragraphs() -> None:
    analyzer = BasicTextAnalyzer()
    text = "First paragraph here.\n\nSecond paragraph follows with more text."
    res = analyzer.analyze(text)

    assert res.metrics["paragraph_count"].value == 2
    assert res.metrics["sentence_count"].value == 2


def test_analyze_document_preserves_id() -> None:
    analyzer = BasicTextAnalyzer()
    doc = Document(id="custom-doc-99", text="Simple text for test.")
    res = analyzer.analyze(doc)

    assert res.document_id == "custom-doc-99"
    assert res.metrics["word_count"].value == 4


def test_analyze_whitespace_and_unicode() -> None:
    analyzer = BasicTextAnalyzer()
    text = "   Café   au   lait!   \n\n   Très   bon.   "
    res = analyzer.analyze(text)

    # Words: ["Café", "au", "lait", "Très", "bon"] -> 5 words
    assert res.metrics["word_count"].value == 5
    assert res.metrics["sentence_count"].value == 2
    assert res.metrics["paragraph_count"].value == 2
    assert res.metrics["min_sentence_length"].value == 2
    assert res.metrics["max_sentence_length"].value == 3
