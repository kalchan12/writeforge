"""Deterministic unit tests for SemanticCoherenceAnalyzer."""

from rightforge.analysis import SemanticCoherenceAnalyzer
from rightforge.models import Document


def test_coherence_empty_text() -> None:
    analyzer = SemanticCoherenceAnalyzer()
    report = analyzer.analyze_coherence("")

    assert report.paragraph_count == 0
    assert report.sentence_count == 0
    assert report.mean_paragraph_coherence == 0.0
    assert report.mean_sentence_coherence == 0.0
    assert report.abrupt_transitions_count == 0


def test_coherence_single_paragraph() -> None:
    analyzer = SemanticCoherenceAnalyzer()
    text = "Machine learning models require clean datasets for reliable evaluation."
    report = analyzer.analyze_coherence(text)

    assert report.paragraph_count == 1
    assert report.mean_paragraph_coherence == 1.0
    assert report.abrupt_transitions_count == 0


def test_coherence_cohesive_paragraphs() -> None:
    analyzer = SemanticCoherenceAnalyzer(abrupt_shift_threshold=0.05)

    # Cohesive text sharing topics: "astronomy", "telescope", "galaxies"
    p1 = "Astronomers use optical telescopes to observe distant galaxies across deep space."
    p2 = "These galaxies contain billions of stars that modern telescopes can resolve with precision."
    p3 = "By studying these stars, telescopes allow astronomers to map cosmic evolution."

    text = f"{p1}\n\n{p2}\n\n{p3}"
    report = analyzer.analyze_coherence(text)

    assert report.paragraph_count == 3
    assert len(report.paragraph_transitions) == 2
    assert report.mean_paragraph_coherence > 0.10
    assert report.abrupt_transitions_count == 0
    assert report.lexical_repetition_rate >= 0.20

    # Verify shared terms between paragraph 1 and 2
    t1 = report.paragraph_transitions[0]
    assert "galaxies" in t1.shared_terms
    assert "telescopes" in t1.shared_terms


def test_coherence_disjointed_paragraphs_flag_abrupt_shifts() -> None:
    analyzer = SemanticCoherenceAnalyzer(abrupt_shift_threshold=0.05)

    # Disjointed text with zero content-word overlap
    p1 = "Quantum algorithms leverage superposition and entanglement to factor prime numbers."
    p2 = "Medieval bakers crafted sourdough loaves using stone hearths and wheat flour."
    p3 = "Marine biologists track humpback whales migrating through Antarctic waters."

    text = f"{p1}\n\n{p2}\n\n{p3}"
    report = analyzer.analyze_coherence(text)

    assert report.paragraph_count == 3
    assert report.mean_paragraph_coherence == 0.0
    assert report.abrupt_transitions_count == 2
    assert report.lexical_repetition_rate == 0.0
    assert "disjunct" in report.summary.lower() or "segmented" in report.summary.lower()


def test_coherence_analyzer_metric_results() -> None:
    analyzer = SemanticCoherenceAnalyzer()
    doc = Document(text="First paragraph with content.\n\nSecond paragraph with content.")
    metrics = {m.name: m.value for m in analyzer.analyze(doc)}

    assert "mean_paragraph_coherence" in metrics
    assert "mean_sentence_coherence" in metrics
    assert "lexical_repetition_rate" in metrics
    assert "abrupt_transitions_count" in metrics
    assert metrics["mean_paragraph_coherence"] > 0.0
