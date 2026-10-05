"""Deterministic unit tests for StylometryAnalyzer."""

from rightforge.analysis import StylometryAnalyzer
from rightforge.models import Document


def test_stylometry_empty_text() -> None:
    analyzer = StylometryAnalyzer()
    metrics = {m.name: m.value for m in analyzer.analyze("")}

    assert metrics["hapax_legomena_count"] == 0
    assert metrics["hapax_legomena_ratio"] == 0.0
    assert metrics["dis_legomena_count"] == 0
    assert metrics["dis_legomena_ratio"] == 0.0
    assert metrics["yules_k"] == 0.0
    assert metrics["simpsons_d"] == 0.0
    assert metrics["function_word_count"] == 0
    assert metrics["flesch_reading_ease"] == 0.0


def test_stylometry_hapax_and_dis_legomena() -> None:
    analyzer = StylometryAnalyzer()
    # Vocabulary:
    # "apple" appears 3 times
    # "banana" appears 2 times (dis legomena)
    # "cherry" appears 1 time (hapax legomena)
    # "date" appears 1 time (hapax legomena)
    # Total tokens = 7
    text = "Apple apple apple. Banana banana. Cherry. Date."
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["hapax_legomena_count"] == 2
    assert metrics["hapax_legomena_ratio"] == round(2 / 7, 4)
    assert metrics["dis_legomena_count"] == 1
    assert metrics["dis_legomena_ratio"] == round(1 / 7, 4)


def test_stylometry_yules_k_extremes() -> None:
    analyzer = StylometryAnalyzer()

    # All unique: Yule's K should be 0.0
    unique_text = "one two three four five"
    metrics_unique = {m.name: m.value for m in analyzer.analyze(unique_text)}
    assert metrics_unique["yules_k"] == 0.0
    assert metrics_unique["simpsons_d"] == 0.0
    assert metrics_unique["simpsons_diversity"] == 1.0

    # All identical tokens: N = 4, sum(i^2 * V_i) = 16
    # Yule's K = 10000 * (16 - 4) / 16 = 7500.0
    # Simpson's D = (4 * 3) / (4 * 3) = 1.0, diversity = 0.0
    identical_text = "same same same same"
    metrics_identical = {m.name: m.value for m in analyzer.analyze(identical_text)}
    assert metrics_identical["yules_k"] == 7500.0
    assert metrics_identical["simpsons_d"] == 1.0
    assert metrics_identical["simpsons_diversity"] == 0.0


def test_stylometry_function_words() -> None:
    analyzer = StylometryAnalyzer()
    # "she went to the market with them"
    # function words: "she" (pron), "to" (prep), "the" (det), "with" (prep), "them" (pron) = 5
    # total words = 7
    text = "She went to the market with them."
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["function_word_count"] == 5
    assert metrics["function_word_ratio"] == round(5 / 7, 4)
    assert metrics["pronoun_ratio"] == round(2 / 7, 4)
    assert metrics["preposition_ratio"] == round(2 / 7, 4)
    assert metrics["determiner_ratio"] == round(1 / 7, 4)


def test_stylometry_readability() -> None:
    analyzer = StylometryAnalyzer()
    # Simple plain English sentence:
    text = "The cat sat on the mat. The dog lay on the rug."
    metrics = {m.name: m.value for m in analyzer.analyze(text)}

    assert metrics["total_syllables"] > 0
    assert metrics["syllables_per_word"] == 1.0  # all monosyllabic words
    # With monosyllabic words and short sentences, Flesch Reading Ease should be very high (> 90)
    assert metrics["flesch_reading_ease"] > 90.0


def test_stylometry_document_preserves_metadata() -> None:
    analyzer = StylometryAnalyzer()
    doc = Document(id="doc-stylo-1", text="Simple text for testing.", metadata={"genre": "fiction"})
    result = analyzer.analyze_document(doc)

    assert result.document_id == "doc-stylo-1"
    assert result.metadata["genre"] == "fiction"
    assert "yules_k" in result.metrics
