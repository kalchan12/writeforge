"""Deterministic unit tests for ProfileAggregator."""

import pytest
from rightforge.models.document import Document
from rightforge.profiles.aggregator import ProfileAggregator


def test_aggregator_empty_documents_raises_error() -> None:
    aggregator = ProfileAggregator()
    with pytest.raises(ValueError, match="empty document list"):
        aggregator.create_profile(author_name="Unknown", documents=[])


def test_aggregator_single_document() -> None:
    aggregator = ProfileAggregator()
    text = "The quick brown fox jumps over the lazy dog. It was a sunny morning."
    profile = aggregator.create_profile(author_name="Test Author", documents=[text])

    assert profile.author_name == "Test Author"
    assert profile.document_count == 1
    assert "word_count" in profile.baselines
    assert "type_token_ratio" in profile.baselines
    assert "yules_k" in profile.baselines

    # With 1 sample, variance and std_dev must be 0.0, and min == max == mean
    word_baseline = profile.baselines["word_count"]
    assert word_baseline.sample_count == 1
    assert word_baseline.std_dev == 0.0
    assert word_baseline.min_value == word_baseline.max_value == word_baseline.mean


def test_aggregator_multi_document_distributions() -> None:
    aggregator = ProfileAggregator()

    # Document 1: 4 words ("One two three four.")
    # Document 2: 8 words ("Five six seven eight nine ten eleven twelve.")
    doc1 = Document(text="One two three four.")
    doc2 = Document(text="Five six seven eight nine ten eleven twelve.")

    profile = aggregator.create_profile(
        author_name="Sample Author",
        documents=[doc1, doc2],
        metadata={"corpus": "numbered"},
    )

    assert profile.document_count == 2
    assert profile.metadata["corpus"] == "numbered"

    # word_count: [4, 8] -> mean = 6.0, variance = ((4-6)^2 + (8-6)^2)/2 = (4+4)/2 = 4.0, std_dev = 2.0
    wc_baseline = profile.baselines["word_count"]
    assert wc_baseline.sample_count == 2
    assert wc_baseline.mean == 6.0
    assert wc_baseline.variance == 4.0
    assert wc_baseline.std_dev == 2.0
    assert wc_baseline.min_value == 4.0
    assert wc_baseline.max_value == 8.0
