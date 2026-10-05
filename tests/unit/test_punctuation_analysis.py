"""Deterministic unit tests for PunctuationAnalyzer."""

from rightforge.analysis import PunctuationAnalyzer


def test_punctuation_empty_text() -> None:
    analyzer = PunctuationAnalyzer()
    metrics = {m.name: m.value for m in analyzer.analyze("")}

    assert metrics["total_punctuation_count"] == 0
    assert metrics["punctuation_density_per_char"] == 0.0
    assert metrics["punctuation_density_per_word"] == 0.0


def test_punctuation_individual_counts() -> None:
    analyzer = PunctuationAnalyzer()
    text = 'Hello, world! How are you? (Fine; yes: "good" — really).'
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["punct_comma_count"] == 1
    assert metrics["punct_period_count"] == 1
    assert metrics["punct_semicolon_count"] == 1
    assert metrics["punct_colon_count"] == 1
    assert metrics["punct_parentheses_count"] == 2
    assert metrics["punct_question_count"] == 1
    assert metrics["punct_exclamation_count"] == 1
    assert metrics["punct_dash_count"] == 1
    assert metrics["punct_quote_count"] == 2

    # Total: 1+1+1+1+2+1+1+1+2 = 11
    assert metrics["total_punctuation_count"] == 11
    assert metrics["punctuation_density_per_char"] > 0.0
    assert metrics["punctuation_density_per_word"] > 0.0
