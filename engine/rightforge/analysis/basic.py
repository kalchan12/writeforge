"""Basic deterministic text analyzer for surface document statistics."""

import math
import re
from typing import Sequence
from rightforge.models import AnalysisResult, Document, MetricResult
from rightforge.text.segmentation import (
    split_paragraphs,
    split_sentences,
    tokenize_words,
)


class BasicTextAnalyzer:
    """Calculates deterministic surface text metrics for a document or text string."""

    def analyze(self, target: Document | str) -> AnalysisResult:
        """Analyze document or text string to compute deterministic surface statistics.

        Args:
            target: A Document instance or raw text string.

        Returns:
            An AnalysisResult containing calculated MetricResult objects.
        """
        if isinstance(target, Document):
            document_id = target.id
            text = target.text
        else:
            document_id = None
            text = target

        result = AnalysisResult(document_id=document_id)

        # 1. Character counts
        total_chars = len(text)
        non_ws_chars = len(re.sub(r"\s+", "", text))

        # 2. Segmentations
        paragraphs = split_paragraphs(text)
        sentences = split_sentences(text)
        words = tokenize_words(text)

        word_count = len(words)
        sentence_count = len(sentences)
        paragraph_count = len(paragraphs)

        # 3. Sentence lengths in words
        sentence_word_counts: list[int] = []
        for s in sentences:
            s_words = tokenize_words(s)
            sentence_word_counts.append(len(s_words))

        # 4. Averages and distributions
        if sentence_count > 0:
            avg_words_per_sentence = round(word_count / sentence_count, 4)
            min_sentence_length = min(sentence_word_counts)
            max_sentence_length = max(sentence_word_counts)
            sentence_length_std_dev = round(
                self._calculate_std_dev(sentence_word_counts), 4
            )
        else:
            avg_words_per_sentence = 0.0
            min_sentence_length = 0
            max_sentence_length = 0
            sentence_length_std_dev = 0.0

        if word_count > 0:
            total_word_chars = sum(len(w) for w in words)
            avg_chars_per_word = round(total_word_chars / word_count, 4)
        else:
            avg_chars_per_word = 0.0

        # Construct MetricResults
        metrics = [
            MetricResult(
                name="character_count",
                value=total_chars,
                description="Total character count including whitespace",
            ),
            MetricResult(
                name="non_whitespace_char_count",
                value=non_ws_chars,
                description="Character count excluding all whitespace",
            ),
            MetricResult(
                name="word_count",
                value=word_count,
                description="Total word token count",
            ),
            MetricResult(
                name="sentence_count",
                value=sentence_count,
                description="Total sentence count",
            ),
            MetricResult(
                name="paragraph_count",
                value=paragraph_count,
                description="Total paragraph count",
            ),
            MetricResult(
                name="avg_words_per_sentence",
                value=avg_words_per_sentence,
                description="Average number of words per sentence",
            ),
            MetricResult(
                name="avg_chars_per_word",
                value=avg_chars_per_word,
                description="Average character length of words",
            ),
            MetricResult(
                name="min_sentence_length",
                value=min_sentence_length,
                description="Word count of the shortest sentence",
            ),
            MetricResult(
                name="max_sentence_length",
                value=max_sentence_length,
                description="Word count of the longest sentence",
            ),
            MetricResult(
                name="sentence_length_std_dev",
                value=sentence_length_std_dev,
                description="Population standard deviation of sentence lengths in words",
            ),
        ]

        for m in metrics:
            result.add_metric(m)

        return result

    @staticmethod
    def _calculate_std_dev(values: Sequence[int | float]) -> float:
        """Calculate population standard deviation deterministically."""
        n = len(values)
        if n <= 1:
            return 0.0
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / n
        return math.sqrt(variance)
