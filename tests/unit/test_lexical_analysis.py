"""Deterministic unit tests for LexicalAnalyzer."""

from rightforge.analysis import LexicalAnalyzer


def test_lexical_empty_text() -> None:
    analyzer = LexicalAnalyzer()
    metrics = {m.name: m.value for m in analyzer.analyze("")}

    assert metrics["total_word_count"] == 0
    assert metrics["unique_word_count"] == 0
    assert metrics["type_token_ratio"] == 0.0
    assert metrics["root_type_token_ratio"] == 0.0
    assert metrics["average_word_length"] == 0.0
    assert metrics["long_word_count"] == 0
    assert metrics["long_word_ratio"] == 0.0


def test_lexical_repeated_words_case_insensitive() -> None:
    analyzer = LexicalAnalyzer()
    text = "The the THE"
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["total_word_count"] == 3
    assert metrics["unique_word_count"] == 1
    assert metrics["type_token_ratio"] == round(1 / 3, 4)
    assert metrics["average_word_length"] == 3.0


def test_lexical_distinct_words() -> None:
    analyzer = LexicalAnalyzer()
    text = "One two three four"
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    # 4 distinct words: TTR = 1.0, root TTR = 4 / sqrt(4) = 2.0
    assert metrics["total_word_count"] == 4
    assert metrics["unique_word_count"] == 4
    assert metrics["type_token_ratio"] == 1.0
    assert metrics["root_type_token_ratio"] == 2.0


def test_lexical_long_words_threshold() -> None:
    analyzer = LexicalAnalyzer(long_word_threshold=7)
    # Words: "short" (5), "medium" (6), "elephant" (8), "extraordinary" (13)
    text = "Short medium elephant extraordinary."
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["total_word_count"] == 4
    assert metrics["long_word_count"] == 2
    assert metrics["long_word_ratio"] == 0.5
