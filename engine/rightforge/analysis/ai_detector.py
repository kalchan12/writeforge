"""Composite AI detection analyzer using multi-signal heuristic scoring and lexical signatures."""

import math
import re

from rightforge.analysis.base import BaseAnalyzer
from rightforge.analysis.linguistic import LinguisticAnalyzer
from rightforge.analysis.perplexity import PerplexityAnalyzer
from rightforge.analysis.semantics import SemanticCoherenceAnalyzer
from rightforge.analysis.stylometry import StylometryAnalyzer
from rightforge.models.ai_detection import AIDetectionReport, AISignal
from rightforge.models.document import Document
from rightforge.text.ai_markers import (
    AI_SIGNATURE_PHRASES,
    AI_SIGNATURE_WORDS,
    AI_TRANSITION_STARTERS,
)
from rightforge.text.segmentation import split_sentences, tokenize_words


def _sigmoid_score(value: float, midpoint: float, steepness: float) -> float:
    """Map a value to 0-1 via sigmoid. Higher value → higher output."""
    x = steepness * (value - midpoint)
    x = max(-20.0, min(20.0, x))  # clamp to prevent overflow
    return 1.0 / (1.0 + math.exp(-x))


def _inverse_sigmoid_score(value: float, midpoint: float, steepness: float) -> float:
    """Map a value to 0-1 via inverted sigmoid. Higher value → lower output (more human)."""
    return 1.0 - _sigmoid_score(value, midpoint, steepness)


class AIDetector(BaseAnalyzer):
    """Computes a high-accuracy composite AI probability score from multiple linguistic

    and lexical signature signals.
    Combines vocabulary fingerprints (ChatGPT/LLM overused words & transitions),
    burstiness, sentence length cadence, perplexity ratio, type-token ratio,
    function word usage, and coherence uniformity.
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

        # Tokenize and extract sentences
        sentences = split_sentences(text)
        words = tokenize_words(text, lowercase=True)
        total_words = len(words)
        sentence_count = len(sentences)

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

        # ── Signal 1: AI Vocabulary Fingerprint (Overused words & phrases) (25%) ──
        # Detect ChatGPT hallmarks like 'delve', 'tapestry', 'testament', 'foster', 'leverage'
        matched_ai_words = [w for w in words if w in AI_SIGNATURE_WORDS]
        ai_word_density = (len(matched_ai_words) / total_words) if total_words > 0 else 0.0

        matched_phrases_count = 0
        for pattern, name, weight in AI_SIGNATURE_PHRASES:
            matches = pattern.findall(text)
            matched_phrases_count += len(matches) * weight

        # Transition starters like 'Furthermore,', 'Moreover,', 'In conclusion,'
        starter_matches = 0
        for s in sentences:
            if any(starter.match(s) for starter in AI_TRANSITION_STARTERS):
                starter_matches += 1

        phrase_density = (matched_phrases_count / max(sentence_count, 1))
        starter_ratio = (starter_matches / max(sentence_count, 1))

        # Composite vocabulary signature score: density > 1.5% is typical of ChatGPT
        vocab_signature_val = ai_word_density * 100.0 + phrase_density * 3.0 + starter_ratio * 2.0
        vocab_signature_score = _sigmoid_score(vocab_signature_val, 1.2, 2.5)

        # ── Signal 2: Sentence Length Cadence Variation (20%) ──
        # Humans naturally alternate between short (staccato) and long sentences.
        # AI models gravitate toward ~15-22 word sentences with std dev < 3.0.
        sent_std_score = _inverse_sigmoid_score(sent_len_std, 4.5, 0.8)

        # ── Signal 3: Perplexity Range Ratio (15%) ──
        if ppl_report.min_sentence_perplexity > 0 and sentence_count > 1:
            ppl_ratio = ppl_report.max_sentence_perplexity / ppl_report.min_sentence_perplexity
        else:
            ppl_ratio = 1.0
        ppl_ratio_score = _inverse_sigmoid_score(ppl_ratio, 1.45, 4.0)

        # ── Signal 4: Cadence Burstiness (15%) ──
        # Coefficient of variation of perplexity across sentences
        burstiness_score = _inverse_sigmoid_score(burstiness, 0.16, 12.0)

        # ── Signal 5: Function Word Ratio (10%) ──
        # AI text avoids natural conversational function words and fillers (<0.33)
        # Natural human writing typically scores 0.38 - 0.55
        func_score = _inverse_sigmoid_score(func_word_ratio, 0.36, 10.0)

        # ── Signal 6: Vocabulary Uniformity (Type-Token Ratio) (10%) ──
        # LLMs intentionally avoid repeating content words, creating unnaturally high TTR (>0.90)
        ttr_score = _sigmoid_score(ttr, 0.86, 12.0)

        # ── Signal 7: Readability & Structure Clustering (5%) ──
        grade_distance = abs(flesch_grade - 11.5)
        readability_score = _inverse_sigmoid_score(grade_distance, 3.5, 0.7)

        # Build signal list with clear human-readable weights and details
        signals = [
            AISignal(
                name="AI Vocabulary Fingerprint",
                raw_value=round(vocab_signature_val, 2),
                sub_score=round(vocab_signature_score, 3),
                weight=0.25,
                description=f"Frequency of known LLM hallmarks & transitions ({len(matched_ai_words)} words, {int(matched_phrases_count)} phrases detected).",
            ),
            AISignal(
                name="Sentence Length Cadence",
                raw_value=round(sent_len_std, 2),
                sub_score=round(sent_std_score, 3),
                weight=0.20,
                description="Standard deviation of sentence lengths. Low variance indicates synthetic uniformity.",
            ),
            AISignal(
                name="Perplexity Variation (Burstiness)",
                raw_value=round(burstiness, 4),
                sub_score=round(burstiness_score, 3),
                weight=0.15,
                description="Fluctuation in sentence predictability. Uniform cadence indicates automated generation.",
            ),
            AISignal(
                name="Predictability Range",
                raw_value=round(ppl_ratio, 2),
                sub_score=round(ppl_ratio_score, 3),
                weight=0.15,
                description="Ratio of maximum to minimum sentence perplexity across clauses.",
            ),
            AISignal(
                name="Function Word Distribution",
                raw_value=round(func_word_ratio, 4),
                sub_score=round(func_score, 3),
                weight=0.10,
                description="Proportion of natural prepositions, pronouns, and conjunctions.",
            ),
            AISignal(
                name="Lexical Repetition Avoidance",
                raw_value=round(ttr, 4),
                sub_score=round(ttr_score, 3),
                weight=0.10,
                description="Type-token ratio. Elevated ratios reflect artificial word-repetition avoidance.",
            ),
            AISignal(
                name="Academic Readability Level",
                raw_value=round(flesch_grade, 2),
                sub_score=round(readability_score, 3),
                weight=0.05,
                description="Proximity to the typical grade 10-12 readability cluster favored by LLMs.",
            ),
        ]

        # Compute weighted composite
        composite = sum(s.sub_score * s.weight for s in signals)

        # Non-linear calibration: when strong multi-signal convergence occurs (high vocab + uniform cadence),
        # amplify the confidence to match commercial detectors (GPTZero / Turnitin)
        if vocab_signature_score > 0.8 and sent_std_score > 0.6:
            composite = min(1.0, composite * 1.25)
        elif sent_std_score > 0.85 and (func_score > 0.7 or ttr_score > 0.75):
            composite = min(1.0, composite * 1.2)

        composite = max(0.0, min(1.0, composite))
        ai_percent = round(composite * 100)

        # Determine verdict with industry-standard 0.30 / 0.60 cutoffs
        if composite <= 0.35:
            verdict = "Likely Human"
        elif composite <= 0.60:
            verdict = "Mixed / Uncertain"
        else:
            verdict = "Likely AI"

        # Determine confidence based on text length and signal agreement
        if sentence_count < 3 or total_words < 30:
            confidence = "low"
        elif sentence_count < 6 or total_words < 70:
            confidence = "medium"
        else:
            high_signals = sum(1 for s in signals if s.sub_score > 0.65)
            low_signals = sum(1 for s in signals if s.sub_score < 0.35)
            if high_signals >= 4 or low_signals >= 4:
                confidence = "high"
            else:
                confidence = "medium"

        # Build qualitative diagnostic summary
        top_signals = sorted(signals, key=lambda s: s.sub_score * s.weight, reverse=True)[:3]
        top_names = ", ".join(s.name.lower() for s in top_signals)

        if composite >= 0.65:
            summary = (
                f"This text shows strong AI-generated characteristics ({ai_percent}% AI probability). "
                f"Key indicators: {top_names}. The writing exhibits patterns typical of "
                f"machine-generated content, including formulaic sentence cadences and known statistical signatures."
            )
        elif composite >= 0.35:
            summary = (
                f"This text shows mixed signals ({ai_percent}% AI probability). "
                f"Some characteristics suggest AI involvement while others appear natural. "
                f"Top contributing signals: {top_names}."
            )
        else:
            summary = (
                f"This text appears to be human-written ({ai_percent}% AI probability). "
                f"The writing shows authentic structural variation, natural rhythm, and vocabulary "
                f"consistent with human authorship."
            )

        return AIDetectionReport(
            ai_score=round(composite, 4),
            ai_score_percent=ai_percent,
            verdict=verdict,
            confidence=confidence,
            signals=signals,
            summary=summary,
        )
