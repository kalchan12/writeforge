"""Deterministic unit tests for profile models and baseline calculations."""

from datetime import datetime
from rightforge.models.profile import AuthorProfile, MetricBaseline


def test_metric_baseline_instantiation_and_zscore() -> None:
    baseline = MetricBaseline(
        name="avg_words_per_sentence",
        mean=15.0,
        variance=4.0,
        std_dev=2.0,
        min_value=12.0,
        max_value=18.0,
        sample_count=5,
        description="Average words per sentence",
    )

    assert baseline.name == "avg_words_per_sentence"
    assert baseline.mean == 15.0
    assert baseline.std_dev == 2.0
    assert baseline.z_score(15.0) == 0.0
    assert baseline.z_score(17.0) == 1.0
    assert baseline.z_score(11.0) == -2.0
    assert baseline.is_within_bounds(17.0, num_std_devs=1.0) is True
    assert baseline.is_within_bounds(20.0, num_std_devs=2.0) is False


def test_metric_baseline_zero_std_dev() -> None:
    baseline = MetricBaseline(
        name="fixed_metric",
        mean=10.0,
        variance=0.0,
        std_dev=0.0,
        min_value=10.0,
        max_value=10.0,
        sample_count=1,
    )
    assert baseline.z_score(10.0) == 0.0
    assert baseline.z_score(12.0) == 0.0
    assert baseline.is_within_bounds(10.0) is True
    assert baseline.is_within_bounds(10.5) is False


def test_author_profile_instantiation_and_add_baseline() -> None:
    profile = AuthorProfile(
        author_name="Alice Author",
        document_count=3,
        metadata={"genre": "academic"},
    )
    assert len(profile.id) > 0
    assert profile.author_name == "Alice Author"
    assert profile.document_count == 3
    assert profile.metadata["genre"] == "academic"
    assert isinstance(profile.created_at, datetime)

    baseline = MetricBaseline(
        name="type_token_ratio",
        mean=0.65,
        variance=0.01,
        std_dev=0.1,
        min_value=0.55,
        max_value=0.75,
        sample_count=3,
    )
    profile.add_baseline(baseline)
    assert "type_token_ratio" in profile.baselines
    assert profile.baselines["type_token_ratio"].mean == 0.65
