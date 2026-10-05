"""Stylometric analysis of authorial invariants, vocabulary richness, and readability."""

from collections import Counter
from rightforge.analysis.base import BaseAnalyzer
from rightforge.models import AnalysisResult, Document, MetricResult
from rightforge.text.function_words import (
    ALL_FUNCTION_WORDS,
    AUXILIARY_VERBS,
    CONJUNCTIONS,
    DETERMINERS,
    PREPOSITIONS,
    PRONOUNS,
)
from rightforge.text.segmentation import split_sentences, tokenize_words
from rightforge.text.syllables import count_syllables


class StylometryAnalyzer(BaseAnalyzer):
    """Computes stylometric invariants, vocabulary richness, function word usage, and readability."""

    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Compute stylometric metrics from target text or document."""
        text = self._extract_text(target)
        words = tokenize_words(text)
        sentences = split_sentences(text)

        total_words = len(words)
        total_sentences = len(sentences)

        if total_words == 0:
            return self._empty_metrics()

        words_lower = [w.lower() for w in words]
        word_counts = Counter(words_lower)
        spectrum = Counter(word_counts.values())

        # 1. Vocabulary Richness (Hapax / Dis Legomena, Yule's K, Simpson's D)
        hapax_count = spectrum.get(1, 0)
        dis_count = spectrum.get(2, 0)
        hapax_ratio = round(hapax_count / total_words, 4)
        dis_ratio = round(dis_count / total_words, 4)

        # Yule's K Characteristic: 10^4 * (sum(i^2 * V_i) - N) / N^2
        sum_i2_vi = sum((count**2) for count in word_counts.values())
        yules_k = round(
            (10000.0 * (sum_i2_vi - total_words)) / (total_words**2), 4
        )

        # Simpson's D Index: sum(n_i * (n_i - 1)) / (N * (N - 1))
        if total_words > 1:
            numerator = sum(n * (n - 1) for n in word_counts.values())
            simpsons_d = round(numerator / (total_words * (total_words - 1)), 4)
            simpsons_diversity = round(1.0 - simpsons_d, 4)
        else:
            simpsons_d = 0.0
            simpsons_diversity = 0.0

        # 2. Function Word Distributions
        func_word_count = sum(1 for w in words_lower if w in ALL_FUNCTION_WORDS)
        func_word_ratio = round(func_word_count / total_words, 4)

        prep_count = sum(1 for w in words_lower if w in PREPOSITIONS)
        prep_ratio = round(prep_count / total_words, 4)

        pron_count = sum(1 for w in words_lower if w in PRONOUNS)
        pron_ratio = round(pron_count / total_words, 4)

        conj_count = sum(1 for w in words_lower if w in CONJUNCTIONS)
        conj_ratio = round(conj_count / total_words, 4)

        aux_count = sum(1 for w in words_lower if w in AUXILIARY_VERBS)
        aux_ratio = round(aux_count / total_words, 4)

        det_count = sum(1 for w in words_lower if w in DETERMINERS)
        det_ratio = round(det_count / total_words, 4)

        # 3. Readability & Syllable Metrics
        total_syllables = sum(count_syllables(w) for w in words)
        syllables_per_word = round(total_syllables / total_words, 4)

        if total_sentences > 0:
            asl = total_words / total_sentences  # Average Sentence Length
            asw = total_syllables / total_words  # Average Syllables per Word

            # Flesch Reading Ease: 206.835 - (1.015 * ASL) - (84.6 * ASW)
            flesch_reading_ease = round(206.835 - (1.015 * asl) - (84.6 * asw), 2)

            # Flesch-Kincaid Grade Level: (0.39 * ASL) + (11.8 * ASW) - 15.59
            flesch_kincaid_grade = round((0.39 * asl) + (11.8 * asw) - 15.59, 2)
        else:
            flesch_reading_ease = 0.0
            flesch_kincaid_grade = 0.0

        return [
            MetricResult(
                name="hapax_legomena_count",
                value=hapax_count,
                description="Words occurring exactly once in the text (V_1)",
            ),
            MetricResult(
                name="hapax_legomena_ratio",
                value=hapax_ratio,
                description="Ratio of once-occurring words to total tokens (V_1 / N)",
            ),
            MetricResult(
                name="dis_legomena_count",
                value=dis_count,
                description="Words occurring exactly twice in the text (V_2)",
            ),
            MetricResult(
                name="dis_legomena_ratio",
                value=dis_ratio,
                description="Ratio of twice-occurring words to total tokens (V_2 / N)",
            ),
            MetricResult(
                name="yules_k",
                value=yules_k,
                description="Yule's K vocabulary richness characteristic",
            ),
            MetricResult(
                name="simpsons_d",
                value=simpsons_d,
                description="Simpson's dominance index D",
            ),
            MetricResult(
                name="simpsons_diversity",
                value=simpsons_diversity,
                description="Simpson's diversity index (1 - D)",
            ),
            MetricResult(
                name="function_word_count",
                value=func_word_count,
                description="Count of closed-class function word tokens",
            ),
            MetricResult(
                name="function_word_ratio",
                value=func_word_ratio,
                description="Ratio of function words to total word tokens",
            ),
            MetricResult(
                name="preposition_ratio",
                value=prep_ratio,
                description="Ratio of preposition tokens to total word tokens",
            ),
            MetricResult(
                name="pronoun_ratio",
                value=pron_ratio,
                description="Ratio of pronoun tokens to total word tokens",
            ),
            MetricResult(
                name="conjunction_ratio",
                value=conj_ratio,
                description="Ratio of conjunction tokens to total word tokens",
            ),
            MetricResult(
                name="auxiliary_verb_ratio",
                value=aux_ratio,
                description="Ratio of auxiliary verb tokens to total word tokens",
            ),
            MetricResult(
                name="determiner_ratio",
                value=det_ratio,
                description="Ratio of determiner tokens to total word tokens",
            ),
            MetricResult(
                name="total_syllables",
                value=total_syllables,
                description="Estimated total syllable count across all words",
            ),
            MetricResult(
                name="syllables_per_word",
                value=syllables_per_word,
                description="Average syllable count per word token",
            ),
            MetricResult(
                name="flesch_reading_ease",
                value=flesch_reading_ease,
                description="Flesch Reading Ease readability index (higher is easier)",
            ),
            MetricResult(
                name="flesch_kincaid_grade",
                value=flesch_kincaid_grade,
                description="Flesch-Kincaid Grade Level index",
            ),
        ]

    def analyze_document(self, target: Document | str) -> AnalysisResult:
        """Run stylometric analysis and package into a structured AnalysisResult."""
        document_id = target.id if isinstance(target, Document) else None
        metadata = target.metadata if isinstance(target, Document) else {}

        result = AnalysisResult(document_id=document_id, metadata=metadata)
        for metric in self.analyze(target):
            result.add_metric(metric)
        return result

    @staticmethod
    def _empty_metrics() -> list[MetricResult]:
        """Return zeroed MetricResult records for empty inputs."""
        metric_names = [
            ("hapax_legomena_count", 0),
            ("hapax_legomena_ratio", 0.0),
            ("dis_legomena_count", 0),
            ("dis_legomena_ratio", 0.0),
            ("yules_k", 0.0),
            ("simpsons_d", 0.0),
            ("simpsons_diversity", 0.0),
            ("function_word_count", 0),
            ("function_word_ratio", 0.0),
            ("preposition_ratio", 0.0),
            ("pronoun_ratio", 0.0),
            ("conjunction_ratio", 0.0),
            ("auxiliary_verb_ratio", 0.0),
            ("determiner_ratio", 0.0),
            ("total_syllables", 0),
            ("syllables_per_word", 0.0),
            ("flesch_reading_ease", 0.0),
            ("flesch_kincaid_grade", 0.0),
        ]
        return [
            MetricResult(name=name, value=val, description="Empty input default")
            for name, val in metric_names
        ]
