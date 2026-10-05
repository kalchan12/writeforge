"""Modular analyzer for sentence structure, length distribution, and cadence."""

import math
from typing import Sequence
from rightforge.analysis.base import BaseAnalyzer
from rightforge.models import Document, MetricResult
from rightforge.text.segmentation import split_sentences, tokenize_words


class SentenceAnalyzer(BaseAnalyzer):
    """Computes sentence length distribution, variance, and structural statistics."""

    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Extract sentence metrics from text or document."""
        text = self._extract_text(target)
        sentences = split_sentences(text)
        sentence_count = len(sentences)

        if sentence_count == 0:
            return [
                MetricResult(
                    name="sentence_count",
                    value=0,
                    description="Total sentence count",
                ),
                MetricResult(
                    name="sentence_length_mean",
                    value=0.0,
                    description="Mean sentence length in words",
                ),
                MetricResult(
                    name="sentence_length_variance",
                    value=0.0,
                    description="Population variance of sentence lengths in words",
                ),
                MetricResult(
                    name="sentence_length_std_dev",
                    value=0.0,
                    description="Population standard deviation of sentence lengths in words",
                ),
                MetricResult(
                    name="shortest_sentence_length",
                    value=0,
                    description="Word count of the shortest sentence",
                ),
                MetricResult(
                    name="longest_sentence_length",
                    value=0,
                    description="Word count of the longest sentence",
                ),
            ]

        lengths = [len(tokenize_words(s)) for s in sentences]
        total_words = sum(lengths)
        mean_len = round(total_words / sentence_count, 4)
        min_len = min(lengths)
        max_len = max(lengths)

        variance = round(self._calculate_variance(lengths, mean_len), 4)
        std_dev = round(math.sqrt(variance), 4)

        return [
            MetricResult(
                name="sentence_count",
                value=sentence_count,
                description="Total sentence count",
            ),
            MetricResult(
                name="sentence_length_mean",
                value=mean_len,
                description="Mean sentence length in words",
            ),
            MetricResult(
                name="sentence_length_variance",
                value=variance,
                description="Population variance of sentence lengths in words",
            ),
            MetricResult(
                name="sentence_length_std_dev",
                value=std_dev,
                description="Population standard deviation of sentence lengths in words",
            ),
            MetricResult(
                name="shortest_sentence_length",
                value=min_len,
                description="Word count of the shortest sentence",
            ),
            MetricResult(
                name="longest_sentence_length",
                value=max_len,
                description="Word count of the longest sentence",
            ),
        ]

    @staticmethod
    def _calculate_variance(values: Sequence[int | float], mean: float) -> float:
        """Calculate population variance."""
        n = len(values)
        if n <= 1:
            return 0.0
        return sum((x - mean) ** 2 for x in values) / n
