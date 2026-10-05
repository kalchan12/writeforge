"""Deterministic unit tests for rule-based syllable estimation."""

from rightforge.text.syllables import count_syllables


def test_syllables_empty_string() -> None:
    assert count_syllables("") == 0
    assert count_syllables("   ") == 0


def test_syllables_single_syllable_words() -> None:
    words = ["cat", "dog", "make", "game", "the", "in", "through"]
    for w in words:
        assert count_syllables(w) == 1, f"Expected 1 syllable for '{w}', got {count_syllables(w)}"


def test_syllables_multi_syllable_words() -> None:
    assert count_syllables("table") == 2
    assert count_syllables("little") == 2
    assert count_syllables("water") == 2
    assert count_syllables("computer") == 3
    assert count_syllables("analysis") == 4
    assert count_syllables("deterministic") == 5


def test_syllables_strips_punctuation() -> None:
    assert count_syllables('"computer!"') == 3
    assert count_syllables("water...") == 2
