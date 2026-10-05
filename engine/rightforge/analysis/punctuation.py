"""Modular analyzer for punctuation frequencies, distributions, and densities."""

import re
from rightforge.analysis.base import BaseAnalyzer
from rightforge.models import Document, MetricResult
from rightforge.text.segmentation import tokenize_words


class PunctuationAnalyzer(BaseAnalyzer):
    """Computes frequencies and densities of standard punctuation marks."""

    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Extract punctuation metrics from text or document."""
        text = self._extract_text(target)
        total_chars = len(text)
        word_count = len(tokenize_words(text))

        # Individual counts
        commas = text.count(",")
        periods = text.count(".")
        semicolons = text.count(";")
        colons = text.count(":")
        parentheses = text.count("(") + text.count(")")
        question_marks = text.count("?")
        exclamation_marks = text.count("!")
        dashes = len(re.findall(r"[-–—]", text))
        quotes = len(re.findall(r"[\"\'“”‘’]", text))

        total_punct = (
            commas
            + periods
            + semicolons
            + colons
            + parentheses
            + question_marks
            + exclamation_marks
            + dashes
            + quotes
        )

        density_per_char = (
            round(total_punct / total_chars, 4) if total_chars > 0 else 0.0
        )
        density_per_word = (
            round(total_punct / word_count, 4) if word_count > 0 else 0.0
        )

        return [
            MetricResult(
                name="punct_comma_count",
                value=commas,
                description="Frequency of commas (,)",
            ),
            MetricResult(
                name="punct_period_count",
                value=periods,
                description="Frequency of periods (.)",
            ),
            MetricResult(
                name="punct_semicolon_count",
                value=semicolons,
                description="Frequency of semicolons (;)",
            ),
            MetricResult(
                name="punct_colon_count",
                value=colons,
                description="Frequency of colons (:)",
            ),
            MetricResult(
                name="punct_parentheses_count",
                value=parentheses,
                description="Frequency of open and closed parentheses",
            ),
            MetricResult(
                name="punct_question_count",
                value=question_marks,
                description="Frequency of question marks (?)",
            ),
            MetricResult(
                name="punct_exclamation_count",
                value=exclamation_marks,
                description="Frequency of exclamation marks (!)",
            ),
            MetricResult(
                name="punct_dash_count",
                value=dashes,
                description="Frequency of hyphens, en-dashes, and em-dashes",
            ),
            MetricResult(
                name="punct_quote_count",
                value=quotes,
                description="Frequency of single, double, and curly quotation marks",
            ),
            MetricResult(
                name="total_punctuation_count",
                value=total_punct,
                description="Total count of standard punctuation marks",
            ),
            MetricResult(
                name="punctuation_density_per_char",
                value=density_per_char,
                description="Ratio of total punctuation marks to total characters",
            ),
            MetricResult(
                name="punctuation_density_per_word",
                value=density_per_word,
                description="Ratio of total punctuation marks to total words",
            ),
        ]
