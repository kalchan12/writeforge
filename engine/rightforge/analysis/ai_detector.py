"""Composite AI detection analyzer using multi-signal heuristic scoring."""

import math

from rightforge.analysis.base import BaseAnalyzer
from rightforge.analysis.linguistic import LinguisticAnalyzer
from rightforge.analysis.perplexity import PerplexityAnalyzer
from rightforge.analysis.semantics import SemanticCoherenceAnalyzer
from rightforge.analysis.stylometry import StylometryAnalyzer
from rightforge.models.ai_detection import AIDetectionReport, AISignal
from rightforge.models.document import Document


def _sigmoid_score(value: float, midpoint: float, steepness: float) -> float:
    """Map a value to 0-1 via sigmoid. Higher value → higher output."""
    x = steepness * (value - midpoint)
    x = max(-20.0, min(20.0, x))  # clamp to prevent overflow
    return 1.0 / (1.0 + math.exp(-x))


def _inverse_sigmoid_score(value: float, midpoint: float, steepness: float) -> float:
    """Map a value to 0-1 via inverted sigmoid. Higher value → lower output (more human)."""
    return 1.0 - _sigmoid_score(value, midpoint, steepness)


class AIDetector(BaseAnalyzer):
    """Computes a composite AI probability score from multiple linguistic signals.

    Combines burstiness, sentence length variation, perplexity range, type-token
    ratio, function word usage, coherence uniformity, and readability to produce
    a single 0-100% AI probability score.
    """

    def __init__(self) -> None:
        self._perplexity_analyzer = PerplexityAnalyzer()
        self._linguistic_analyzer = LinguisticAnalyzer()
        self._stylometry_analyzer = StylometryAnalyzer()
        self._coherence_analyzer = SemanticCoherenceAnalyzer()

    def analyze(self, target: Document | str) -> list:
        """Satisfy BaseAnalyzer interface — delegates to detect()."""
        report = self.detect(target)
        return []

    def detect(self, target: Document | str) -> AIDetectionReport:
        """Run all analyzers and compute composite AI detection score."""
        text = self._extract_text(target)

        if not text.strip():
            return AIDetectionReport(
                ai_score=0.0,
                ai_score_percent=0,
                verdict="No Content",
                confidence="low",
                signals=[],
                summary="No text provided for analysis.",
            )

        # Collect raw signals from existing analyzers
        ppl_report = self._perplexity_analyzer.analyze_perplexity(target)
        ling_result = self._linguistic_analyzer.analyze(target)
        stylo_result = self._stylometry_analyzer.analyze(target)
        coherence_report = self._coherence_analyzer.analyze_coherence(target)

        # Build metric lookup dicts
        ling_metrics = {m.name: m.value for m in ling_result}
        stylo_metrics = {m.name: m.value for m in stylo_result}

        # Extract raw values
        burstiness = ppl_report.burstiness
        sent_len_std = ling_metrics.get("sentence_length_std_dev", 0.0)
        ttr = ling_metrics.get("type_token_ratio", 0.5)
        func_word_ratio = stylo_metrics.get("function_word_ratio", 0.4)
        flesch_grade = stylo_metrics.get("flesch_kincaid_grade", 10.0)
        mean_para_coherence = coherence_report.mean_paragraph_coherence
        sentence_count = ppl_report.sentence_count

        # Perplexity range ratio
        if ppl_report.min_sentence_perplexity > 0 and sentence_count > 1:
            ppl_ratio = ppl_report.max_sentence_perplexity / ppl_report.min_sentence_perplexity
        else:
            ppl_ratio = 1.0

        # ── Signal 1: Burstiness (Cadence Variation) (25%) ──
        # Synthetic text with uniform length/structure has low burstiness (<0.10)
        # Dynamic human texts typically fall around 0.12 - 0.35+
        burstiness_score = _inverse_sigmoid_score(burstiness, 0.14, 18.0)

        # ── Signal 2: Sentence length std dev (25%) ──
        # Highly diagnostic of AI: LLMs write sentences of similar lengths (std dev < 2.0).
        # Human writing fluctuates with short & long sentences (std dev > 5.0).
        sent_std_score = _inverse_sigmoid_score(sent_len_std, 4.0, 0.9)

        # ── Signal 3: Perplexity range ratio (15%) ──
        # Uniform AI text clusters tightly (ratio < 1.25). Human text has diverse clauses (> 1.4).
        ppl_ratio_score = _inverse_sigmoid_score(ppl_ratio, 1.35, 6.0)

        # ── Signal 4: Type-Token Ratio (10%) ──
        # Very high TTR (>0.90) in moderate-length text = AI-like avoidance of natural repetition.
        ttr_score = _sigmoid_score(ttr, 0.88, 12.0)

        # ── Signal 5: Function word ratio (10%) ──
        # AI text tends to have lower function word ratio (<0.32). Human writing 0.38 - 0.55.
        func_score = _inverse_sigmoid_score(func_word_ratio, 0.35, 10.0)

        # ── Signal 6: Coherence uniformity (10%) ──
        if coherence_report.paragraph_count > 1:
            coherence_score = _sigmoid_score(mean_para_coherence, 0.18, 10.0)
        else:
            coherence_score = 0.35  # neutral for single-paragraph text

        # ── Signal 7: Readability clustering (5%) ──
        grade_distance = abs(flesch_grade - 11.0)
        readability_score = _inverse_sigmoid_score(grade_distance, 3.5, 0.8)

        # Build signal list
        signals = [
            AISignal(
                name="Sentence Length Variation",
                raw_value=round(sent_len_std, 2),
                sub_score=round(sent_std_score, 3),
                weight=0.30,
                description="Standard deviation of sentence lengths. Low (<2.5) = uniform/AI-like.",
            ),
            AISignal(
                name="Burstiness (Cadence Variation)",
                raw_value=round(burstiness, 4),
                sub_score=round(burstiness_score, 3),
                weight=0.15,
                description="Sentence-to-sentence perplexity variation. Low = uniform/AI-like.",
            ),
            AISignal(
                name="Perplexity Range",
                raw_value=round(ppl_ratio, 2),
                sub_score=round(ppl_ratio_score, 3),
                weight=0.15,
                description="Max-to-min sentence perplexity ratio. Low = uniform/AI-like.",
            ),
            AISignal(
                name="Function Word Usage",
                raw_value=round(func_word_ratio, 4),
                sub_score=round(func_score, 3),
                weight=0.20,
                description="Ratio of function words. Low (<0.32) = AI-like (avoids filler words).",
            ),
            AISignal(
                name="Vocabulary Uniformity",
                raw_value=round(ttr, 4),
                sub_score=round(ttr_score, 3),
                weight=0.10,
                description="Type-token ratio. Very high = AI-like avoidance of repetition.",
            ),
            AISignal(
                name="Coherence Uniformity",
                raw_value=round(mean_para_coherence, 4),
                sub_score=round(coherence_score, 3),
                weight=0.05,
                description="Paragraph transition uniformity. Very uniform = AI-like.",
            ),
            AISignal(
                name="Readability Clustering",
                raw_value=round(flesch_grade, 2),
                sub_score=round(readability_score, 3),
                weight=0.05,
                description="Proximity to typical AI readability level (grade 10-12).",
            ),
        ]

        # Compute weighted composite
        composite = sum(s.sub_score * s.weight for s in signals)
        composite = max(0.0, min(1.0, composite))
        ai_percent = round(composite * 100)

        # Determine verdict
        if composite < 0.35:
            verdict = "Likely Human"
        elif composite < 0.65:
            verdict = "Mixed / Uncertain"
        else:
            verdict = "Likely AI"

        # Determine confidence based on text length and signal agreement
        if sentence_count < 3:
            confidence = "low"
        elif sentence_count < 8:
            confidence = "medium"
        else:
            # Check signal agreement: if signals strongly agree, high confidence
            high_signals = sum(1 for s in signals if s.sub_score > 0.7)
            low_signals = sum(1 for s in signals if s.sub_score < 0.3)
            if high_signals >= 5 or low_signals >= 5:
                confidence = "high"
            elif high_signals >= 3 or low_signals >= 3:
                confidence = "medium"
            else:
                confidence = "medium"

        # Build summary
        top_signals = sorted(signals, key=lambda s: s.sub_score * s.weight, reverse=True)[:3]
        top_names = ", ".join(s.name.lower() for s in top_signals)

        if composite >= 0.65:
            summary = (
                f"This text shows strong AI-generated characteristics ({ai_percent}% AI probability). "
                f"Key indicators: {top_names}. The writing exhibits patterns typical of "
                f"machine-generated content, including uniform cadence and predictable structure."
            )
        elif composite >= 0.35:
            summary = (
                f"This text shows mixed signals ({ai_percent}% AI probability). "
                f"Some characteristics suggest AI involvement while others appear human-written. "
                f"Top contributing signals: {top_names}."
            )
        else:
            summary = (
                f"This text appears to be human-written ({ai_percent}% AI probability). "
                f"The writing shows natural variation in cadence, structure, and vocabulary "
                f"that is consistent with human authorship."
            )

        return AIDetectionReport(
            ai_score=round(composite, 4),
            ai_score_percent=ai_percent,
            verdict=verdict,
            confidence=confidence,
            signals=signals,
            summary=summary,
        )
