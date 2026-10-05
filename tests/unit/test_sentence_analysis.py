"""Deterministic unit tests for SentenceAnalyzer."""

from rightforge.analysis import SentenceAnalyzer


def test_sentence_empty_text() -> None:
    analyzer = SentenceAnalyzer()
    metrics = {m.name: m.value for m in analyzer.analyze("")}

    assert metrics["sentence_count"] == 0
    assert metrics["sentence_length_mean"] == 0.0
    assert metrics["sentence_length_variance"] == 0.0
    assert metrics["sentence_length_std_dev"] == 0.0
    assert metrics["shortest_sentence_length"] == 0
    assert metrics["longest_sentence_length"] == 0


def test_sentence_single_sentence() -> None:
    analyzer = SentenceAnalyzer()
    text = "A quick test sentence."
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["sentence_count"] == 1
    assert metrics["sentence_length_mean"] == 4.0
    assert metrics["sentence_length_variance"] == 0.0
    assert metrics["sentence_length_std_dev"] == 0.0
    assert metrics["shortest_sentence_length"] == 4
    assert metrics["longest_sentence_length"] == 4


def test_sentence_variance_and_std_dev() -> None:
    analyzer = SentenceAnalyzer()
    # Sentence 1: 2 words ("Two words.")
    # Sentence 2: 6 words ("Here are six words right now.")
    # Mean: (2 + 6) / 2 = 4.0
    # Variance: ((2-4)^2 + (6-4)^2)/2 = (4 + 4)/2 = 4.0
    # Std Dev: sqrt(4.0) = 2.0
    text = "Two words. Here are six words right now."
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["sentence_count"] == 2
    assert metrics["sentence_length_mean"] == 4.0
    assert metrics["sentence_length_variance"] == 4.0
    assert metrics["sentence_length_std_dev"] == 2.0
    assert metrics["shortest_sentence_length"] == 2
    assert metrics["longest_sentence_length"] == 6
