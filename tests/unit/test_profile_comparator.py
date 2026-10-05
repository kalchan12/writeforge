"""Deterministic unit tests for ProfileComparator and consistency scoring."""

from rightforge.models.profile import AuthorProfile, MetricBaseline
from rightforge.profiles.aggregator import ProfileAggregator
from rightforge.profiles.comparator import ProfileComparator


def test_comparator_exact_match() -> None:
    aggregator = ProfileAggregator()
    comparator = ProfileComparator()

    sample_texts = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast dark creature leaps above the resting canine.",
    ]
    profile = aggregator.create_profile("Author A", sample_texts)

    # Comparing against identical text should yield very high consistency and zero outliers
    report = comparator.compare(profile, sample_texts[0], outlier_threshold=2.0)

    assert report.author_name == "Author A"
    assert report.consistency_score >= 0.85
    assert report.outlier_count == 0
    assert len(report.deviations) > 0


def test_comparator_divergent_text_triggers_outliers() -> None:
    comparator = ProfileComparator()

    # Create a synthetic profile with very specific, narrow baselines
    profile = AuthorProfile(
        author_name="Minimalist",
        document_count=5,
        baselines={
            "avg_words_per_sentence": MetricBaseline(
                name="avg_words_per_sentence",
                mean=4.0,
                variance=0.25,
                std_dev=0.5,
                min_value=3.5,
                max_value=4.5,
                sample_count=5,
            ),
            "punct_semicolon_count": MetricBaseline(
                name="punct_semicolon_count",
                mean=0.0,
                variance=0.0,
                std_dev=0.0,
                min_value=0.0,
                max_value=0.0,
                sample_count=5,
            ),
        },
    )

    # Highly complex text with long sentences and many semicolons
    complex_text = (
        "This is an exceedingly elaborate and convoluted sentence designed specifically to test "
        "the boundary conditions of the stylometric profile comparator; furthermore, we deliberately "
        "introduce multiple semicolons; and in addition, we elongate the syntax beyond any reasonable measure."
    )

    report = comparator.compare(profile, complex_text, outlier_threshold=2.0)

    assert report.consistency_score < 0.60
    assert report.outlier_count >= 1
    assert "avg_words_per_sentence" in report.outliers or "punct_semicolon_count" in report.outliers
    assert "avg_words_per_sentence" in report.deviations
    assert report.deviations["avg_words_per_sentence"].is_outlier is True
