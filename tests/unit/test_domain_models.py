"""Deterministic unit tests for base domain models."""

from datetime import datetime, timezone
from rightforge.models import AnalysisResult, Document, MetricResult


def test_document_instantiation_defaults() -> None:
    """Document should populate id and created_at if omitted."""
    doc = Document(text="Hello world.")
    assert len(doc.id) > 0
    assert doc.text == "Hello world."
    assert doc.metadata == {}
    assert isinstance(doc.created_at, datetime)
    assert doc.created_at.tzinfo is not None


def test_document_custom_attributes() -> None:
    """Document should respect custom id and metadata."""
    custom_time = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    doc = Document(
        id="doc-123",
        text="Sample document text.",
        metadata={"author": "Researcher", "corpus": "test"},
        created_at=custom_time,
    )
    assert doc.id == "doc-123"
    assert doc.text == "Sample document text."
    assert doc.metadata["author"] == "Researcher"
    assert doc.created_at == custom_time


def test_metric_result_instantiation() -> None:
    """MetricResult should preserve name, value, and description."""
    metric = MetricResult(
        name="char_count",
        value=42,
        description="Total number of characters",
    )
    assert metric.name == "char_count"
    assert metric.value == 42
    assert metric.description == "Total number of characters"


def test_analysis_result_aggregation() -> None:
    """AnalysisResult should collect MetricResult instances cleanly."""
    result = AnalysisResult(document_id="doc-abc")
    assert result.document_id == "doc-abc"
    assert len(result.metrics) == 0

    metric1 = MetricResult(name="word_count", value=10)
    metric2 = MetricResult(name="char_count", value=50)

    result.add_metric(metric1)
    result.add_metric(metric2)

    assert len(result.metrics) == 2
    assert result.metrics["word_count"].value == 10
    assert result.metrics["char_count"].value == 50
