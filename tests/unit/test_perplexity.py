"""Unit tests for perplexity modeling, n-gram language models, and burstiness analysis."""

import pytest
from rightforge.analysis.perplexity import PerplexityAnalyzer
from rightforge.ml.hf_model import HuggingFaceProbabilityModel
from rightforge.ml.probability import NgramProbabilityModel
from rightforge.models.document import Document
from rightforge.models.transformers import PerplexityReport, SentencePerplexity


def test_ngram_model_scoring_validity():
    """Verify n-gram model produces finite negative log-probabilities and perplexity >= 1.0."""
    model = NgramProbabilityModel()
    tokens = ["the", "analytical", "engine", "weaves", "patterns"]

    logprobs = model.score_tokens(tokens)
    assert len(logprobs) == len(tokens)
    assert all(lp < 0.0 for lp in logprobs)

    ppl, mean_lp = model.score_sentence(tokens)
    assert ppl >= 1.0
    assert mean_lp < 0.0


def test_ngram_model_empty_tokens():
    """Verify graceful handling of empty token sequences."""
    model = NgramProbabilityModel()
    assert model.score_tokens([]) == []
    ppl, mean_lp = model.score_sentence([])
    assert ppl == 1.0
    assert mean_lp == 0.0


def test_ngram_model_custom_training():
    """Verify custom training texts update n-gram counts and vocabulary."""
    model = NgramProbabilityModel(reference_corpus=[])
    assert len(model.vocab) == 0

    model.train(["Quantum entanglement defies classical intuition."])
    assert "quantum" in model.vocab
    assert "entanglement" in model.vocab
    assert len(model.vocab) == 5

    tokens = ["quantum", "entanglement"]
    logprobs = model.score_tokens(tokens)
    assert len(logprobs) == 2


def test_perplexity_analyzer_empty_text():
    """Verify analyzer response for empty or whitespace text."""
    analyzer = PerplexityAnalyzer()
    report = analyzer.analyze_perplexity("")

    assert isinstance(report, PerplexityReport)
    assert report.sentence_count == 0
    assert report.overall_perplexity == 0.0
    assert report.burstiness == 0.0
    assert report.sentence_perplexities == []
    assert "no readable sentences" in report.summary.lower()


def test_perplexity_analyzer_single_sentence():
    """Verify analyzer metrics on a single sentence (burstiness should be 0.0)."""
    analyzer = PerplexityAnalyzer()
    doc = Document(text="Science is the systematic enterprise that organizes knowledge.")
    report = analyzer.analyze_perplexity(doc)

    assert report.document_id == doc.id
    assert report.sentence_count == 1
    assert len(report.sentence_perplexities) == 1
    assert report.burstiness == 0.0
    assert report.overall_perplexity > 0.0
    assert report.min_sentence_perplexity == report.max_sentence_perplexity


def test_perplexity_analyzer_multiple_sentences_and_burstiness():
    """Verify per-sentence perplexity progression and positive burstiness across diverse sentences."""
    analyzer = PerplexityAnalyzer()
    text = (
        "The quick brown fox jumps over the lazy dog. "
        "Incomprehensible multi-dimensional quantum fluctuations produce non-deterministic observations! "
        "It was sunny."
    )
    report = analyzer.analyze_perplexity(text)

    assert report.sentence_count == 3
    assert len(report.sentence_perplexities) == 3
    assert report.burstiness > 0.0
    assert report.min_sentence_perplexity <= report.max_sentence_perplexity
    assert report.mean_sentence_perplexity > 0.0

    # Check sentence perplexity item structure
    s0 = report.sentence_perplexities[0]
    assert isinstance(s0, SentencePerplexity)
    assert s0.sentence_index == 0
    assert s0.token_count > 0
    assert s0.perplexity > 0.0


def test_burstiness_comparison_uniform_vs_varied():
    """Verify that varied cadence produces strictly higher burstiness than uniform sentences."""
    analyzer = PerplexityAnalyzer()

    # Uniform text: identical repetitive sentences
    uniform_text = (
        "The engine weaves patterns. "
        "The engine weaves patterns. "
        "The engine weaves patterns."
    )
    uniform_report = analyzer.analyze_perplexity(uniform_text)

    # Varied text: mix of short predictable and long complex sentences
    varied_text = (
        "To be or not to be. "
        "Empirical evidence gathered through rigorous methodology forms the bedrock of modern discovery. "
        "Yes."
    )
    varied_report = analyzer.analyze_perplexity(varied_text)

    assert uniform_report.burstiness < 0.001
    assert varied_report.burstiness > 0.10
    assert varied_report.burstiness > uniform_report.burstiness


def test_perplexity_analyzer_pipeline_metric_results():
    """Verify analyze() method outputs standard MetricResult list for composite pipeline compatibility."""
    analyzer = PerplexityAnalyzer()
    text = "Writing is an exploration. You start from nothing and learn as you proceed."
    metrics = analyzer.analyze(text)

    assert len(metrics) == 6
    names = {m.name for m in metrics}
    assert "overall_perplexity" in names
    assert "mean_sentence_perplexity" in names
    assert "burstiness" in names
    assert "min_sentence_perplexity" in names
    assert "max_sentence_perplexity" in names
    assert "sentence_count" in names


def test_huggingface_model_fallback_error(monkeypatch):
    """Verify HuggingFaceProbabilityModel raises informative ImportError when transformers is unavailable."""
    import sys
    monkeypatch.setitem(sys.modules, "transformers", None)

    hf_model = HuggingFaceProbabilityModel(model_name="nonexistent-model")
    with pytest.raises(ImportError) as exc_info:
        hf_model.score_tokens(["sample", "words"])

    assert "requires 'torch' and 'transformers'" in str(exc_info.value)
