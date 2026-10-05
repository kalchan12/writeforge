"""Deterministic unit tests for composite LinguisticAnalyzer."""

from rightforge.analysis import LinguisticAnalyzer
from rightforge.models import Document


def test_linguistic_pipeline_combines_metrics() -> None:
    analyzer = LinguisticAnalyzer()
    text = "The quick brown fox jumps! Does it sleep? Yes; it sleeps."
    result = analyzer.analyze_document(text)

    # Check presence of metrics from all three domains
    # Lexical:
    assert "unique_word_count" in result.metrics
    assert "type_token_ratio" in result.metrics
    assert "root_type_token_ratio" in result.metrics
    assert "long_word_ratio" in result.metrics

    # Sentence:
    assert "sentence_count" in result.metrics
    assert "sentence_length_mean" in result.metrics
    assert "sentence_length_variance" in result.metrics
    assert "sentence_length_std_dev" in result.metrics

    # Punctuation:
    assert "punct_exclamation_count" in result.metrics
    assert "punct_question_count" in result.metrics
    assert "punct_semicolon_count" in result.metrics
    assert "total_punctuation_count" in result.metrics


def test_linguistic_document_input() -> None:
    analyzer = LinguisticAnalyzer()
    doc = Document(id="doc-ling-1", text="Simple text.")
    result = analyzer.analyze_document(doc)

    assert result.document_id == "doc-ling-1"
    assert result.metrics["total_word_count"].value == 2
