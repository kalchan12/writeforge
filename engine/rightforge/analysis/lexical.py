"""Modular analyzer for lexical diversity, vocabulary richness, and word characteristics."""

import math
from rightforge.analysis.base import BaseAnalyzer
from rightforge.models import Document, MetricResult
from rightforge.text.segmentation import tokenize_words

DEFAULT_LONG_WORD_THRESHOLD = 7


class LexicalAnalyzer(BaseAnalyzer):
    """Computes lexical diversity, type-token ratio, and word length metrics."""

    def __init__(self, long_word_threshold: int = DEFAULT_LONG_WORD_THRESHOLD) -> None:
        self.long_word_threshold = long_word_threshold

    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Extract lexical metrics from text or document."""
        text = self._extract_text(target)
        words = tokenize_words(text)
        total_words = len(words)

        if total_words == 0:
            return [
                MetricResult(
                    name="total_word_count",
                    value=0,
                    description="Total word token count",
                ),
                MetricResult(
                    name="unique_word_count",
                    value=0,
                    description="Count of distinct vocabulary words (case-insensitive)",
                ),
                MetricResult(
                    name="type_token_ratio",
                    value=0.0,
                    description="Ratio of unique words to total words (V / N)",
                ),
                MetricResult(
                    name="root_type_token_ratio",
                    value=0.0,
                    description="Guiraud's root type-token ratio (V / sqrt(N))",
                ),
                MetricResult(
                    name="average_word_length",
                    value=0.0,
                    description="Average character length of words",
                ),
                MetricResult(
                    name="long_word_count",
                    value=0,
                    description=f"Count of words with length >= {self.long_word_threshold}",
                ),
                MetricResult(
                    name="long_word_ratio",
                    value=0.0,
                    description=f"Ratio of words with length >= {self.long_word_threshold} to total words",
                ),
            ]

        words_lower = [w.lower() for w in words]
        unique_words = set(words_lower)
        unique_word_count = len(unique_words)

        ttr = round(unique_word_count / total_words, 4)
        root_ttr = round(unique_word_count / math.sqrt(total_words), 4)

        total_word_chars = sum(len(w) for w in words)
        avg_word_length = round(total_word_chars / total_words, 4)

        long_word_count = sum(1 for w in words if len(w) >= self.long_word_threshold)
        long_word_ratio = round(long_word_count / total_words, 4)

        return [
            MetricResult(
                name="total_word_count",
                value=total_words,
                description="Total word token count",
            ),
            MetricResult(
                name="unique_word_count",
                value=unique_word_count,
                description="Count of distinct vocabulary words (case-insensitive)",
            ),
            MetricResult(
                name="type_token_ratio",
                value=ttr,
                description="Ratio of unique words to total words (V / N)",
            ),
            MetricResult(
                name="root_type_token_ratio",
                value=root_ttr,
                description="Guiraud's root type-token ratio (V / sqrt(N))",
            ),
            MetricResult(
                name="average_word_length",
                value=avg_word_length,
                description="Average character length of words",
            ),
            MetricResult(
                name="long_word_count",
                value=long_word_count,
                description=f"Count of words with length >= {self.long_word_threshold}",
            ),
            MetricResult(
                name="long_word_ratio",
                value=long_word_ratio,
                description=f"Ratio of words with length >= {self.long_word_threshold} to total words",
            ),
        ]
