"""Unit tests for the RevisionExecutor pipeline."""

from rightforge.llm.base import MockLLMProvider
from rightforge.models.document import Document
from rightforge.models.execution import RevisionExecutionResult
from rightforge.models.profile import AuthorProfile, MetricBaseline
from rightforge.revision.executor import RevisionExecutor


def test_executor_empty_text():
    """Verify executor gracefully rejects empty text with clear error message."""
    executor = RevisionExecutor(provider=MockLLMProvider())
    result = executor.execute("")

    assert isinstance(result, RevisionExecutionResult)
    assert result.success is False
    assert result.revised_text == ""
    assert "empty" in result.error_message.lower()


def test_executor_standalone_revision():
    """Verify end-to-end execution with MockLLMProvider and snapshot metric calculation."""
    canned = "Short words convey clear meaning. Direct prose avoids ambiguity."
    provider = MockLLMProvider(canned_response=canned)
    executor = RevisionExecutor(provider=provider)

    source = (
        "The analytical engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves. "
        "Mathematical calculations require rigorous discipline and uncompromising adherence to symbolic truth."
    )
    result = executor.execute(source)

    assert result.success is True
    assert result.original_text == source
    assert result.revised_text == canned
    assert result.error_message is None
    assert "word_count" in result.metrics_before
    assert "word_count" in result.metrics_after
    assert result.metrics_after["word_count"] > 0
    assert provider.call_count == 1


def test_executor_profile_guided_verification():
    """Verify consistency scores before and after revision are tracked."""
    profile = AuthorProfile(
        author_name="Concise Writer",
        document_count=5,
        baselines={
            "sentence_length_mean": MetricBaseline(
                name="sentence_length_mean",
                mean=5.0,
                variance=0.5,
                std_dev=0.7,
                min_value=4.0,
                max_value=6.0,
                sample_count=5,
            )
        },
    )

    # Canned output with exactly 5 words per sentence to match profile baseline perfectly
    canned = "Short words make sense. Clean prose reads well."
    provider = MockLLMProvider(canned_response=canned)
    executor = RevisionExecutor(provider=provider)

    long_source = (
        "The extraordinarily intricate computational mechanisms manifest significant structural anomalies "
        "across all empirical observation intervals."
    )
    result = executor.execute(target=long_source, profile=profile, outlier_threshold=1.5)

    assert result.success is True
    assert result.consistency_before is not None
    assert result.consistency_after is not None
    # Revised text matches baseline much closer, so consistency score should improve
    assert result.consistency_after >= result.consistency_before


def test_executor_provider_failure_handling():
    """Verify executor handles provider runtime failure without crashing."""
    provider = MockLLMProvider(fail_with_error="Ollama connection timeout (30s)")
    executor = RevisionExecutor(provider=provider)

    result = executor.execute("Sample text for revision.")

    assert result.success is False
    assert result.revised_text == ""
    assert "Ollama connection timeout" in result.error_message
