"""Semantic coherence and lexical transition analyzer for textual flow."""

from typing import Sequence
from rightforge.analysis.base import BaseAnalyzer
from rightforge.models.document import Document, MetricResult
from rightforge.models.semantics import SemanticCoherenceReport, TransitionScore
from rightforge.text.function_words import ALL_FUNCTION_WORDS
from rightforge.text.segmentation import split_paragraphs, split_sentences, tokenize_words


class SemanticCoherenceAnalyzer(BaseAnalyzer):
    """Computes semantic continuity, topic maintenance, and transition cohesion across text segments."""

    def __init__(self, abrupt_shift_threshold: float = 0.05) -> None:
        self.abrupt_shift_threshold = abrupt_shift_threshold

    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Extract high-level coherence metrics from target."""
        report = self.analyze_coherence(target)
        return [
            MetricResult(
                name="mean_paragraph_coherence",
                value=report.mean_paragraph_coherence,
                description="Average Jaccard lexical continuity between adjacent paragraphs",
            ),
            MetricResult(
                name="mean_sentence_coherence",
                value=report.mean_sentence_coherence,
                description="Average Jaccard lexical continuity between adjacent sentences",
            ),
            MetricResult(
                name="lexical_repetition_rate",
                value=report.lexical_repetition_rate,
                description="Proportion of content words reused across multiple paragraphs",
            ),
            MetricResult(
                name="abrupt_transitions_count",
                value=report.abrupt_transitions_count,
                description="Count of adjacent paragraph transitions with minimal lexical continuity",
            ),
        ]

    def analyze_coherence(
        self,
        target: Document | str,
        abrupt_threshold: float | None = None,
    ) -> SemanticCoherenceReport:
        """Perform comprehensive semantic coherence evaluation across paragraphs and sentences."""
        threshold = (
            abrupt_threshold if abrupt_threshold is not None else self.abrupt_shift_threshold
        )
        text = self._extract_text(target)
        doc_id = target.id if isinstance(target, Document) else None

        paragraphs = split_paragraphs(text)
        sentences = split_sentences(text)

        p_count = len(paragraphs)
        s_count = len(sentences)

        # 1. Paragraph-to-paragraph transitions
        para_transitions: list[TransitionScore] = []
        para_jaccards: list[float] = []

        if p_count > 1:
            for i in range(p_count - 1):
                trans = self._compute_transition(
                    paragraphs[i], paragraphs[i + 1], i, i + 1, threshold
                )
                para_transitions.append(trans)
                para_jaccards.append(trans.jaccard_similarity)
            mean_para_coherence = round(sum(para_jaccards) / len(para_jaccards), 4)
        else:
            mean_para_coherence = 1.0 if p_count == 1 and text.strip() else 0.0

        # 2. Sentence-to-sentence transitions
        sent_jaccards: list[float] = []
        if s_count > 1:
            for i in range(s_count - 1):
                trans = self._compute_transition(
                    sentences[i], sentences[i + 1], i, i + 1, threshold
                )
                sent_jaccards.append(trans.jaccard_similarity)
            mean_sent_coherence = round(sum(sent_jaccards) / len(sent_jaccards), 4)
        else:
            mean_sent_coherence = 1.0 if s_count == 1 and text.strip() else 0.0

        # 3. Document-wide lexical chaining (content word recurrence across paragraphs)
        para_content_sets = [self._extract_content_words(p) for p in paragraphs]
        all_unique_content_words = set().union(*para_content_sets) if para_content_sets else set()

        if len(all_unique_content_words) > 0 and p_count > 1:
            repeated_words = 0
            for word in all_unique_content_words:
                occurrences_in_paras = sum(1 for p_set in para_content_sets if word in p_set)
                if occurrences_in_paras >= 2:
                    repeated_words += 1
            repetition_rate = round(repeated_words / len(all_unique_content_words), 4)
        else:
            repetition_rate = 1.0 if p_count == 1 and all_unique_content_words else 0.0

        abrupt_shifts = sum(1 for t in para_transitions if t.is_abrupt_shift)

        # 4. Qualitative summary
        if p_count <= 1:
            flow_quality = "Single text block"
        elif mean_para_coherence >= 0.15 and abrupt_shifts == 0:
            flow_quality = "Fluid and continuous"
        elif mean_para_coherence >= 0.08:
            flow_quality = "Moderately cohesive"
        else:
            flow_quality = "Segmented or disjunct"

        summary = (
            f"Document exhibits {flow_quality.lower()} semantic flow across {p_count} paragraph(s) "
            f"(mean paragraph coherence: {mean_para_coherence:.2f}, {abrupt_shifts} abrupt shift(s) detected)."
        )

        return SemanticCoherenceReport(
            document_id=doc_id,
            paragraph_count=p_count,
            sentence_count=s_count,
            mean_paragraph_coherence=mean_para_coherence,
            mean_sentence_coherence=mean_sent_coherence,
            lexical_repetition_rate=repetition_rate,
            abrupt_transitions_count=abrupt_shifts,
            paragraph_transitions=para_transitions,
            summary=summary,
        )

    def _compute_transition(
        self,
        seg1: str,
        seg2: str,
        from_idx: int,
        to_idx: int,
        threshold: float,
    ) -> TransitionScore:
        """Compute lexical Jaccard similarity and overlap coefficient between two segments."""
        words1 = self._extract_content_words(seg1)
        words2 = self._extract_content_words(seg2)

        intersection = words1 & words2
        union = words1 | words2

        if union:
            jaccard = round(len(intersection) / len(union), 4)
        else:
            jaccard = 1.0 if not words1 and not words2 else 0.0

        min_len = min(len(words1), len(words2))
        overlap = round(len(intersection) / min_len, 4) if min_len > 0 else 0.0

        is_abrupt = jaccard < threshold

        return TransitionScore(
            from_index=from_idx,
            to_index=to_idx,
            jaccard_similarity=jaccard,
            overlap_coefficient=overlap,
            shared_terms=sorted(list(intersection)),
            is_abrupt_shift=is_abrupt,
        )

    @staticmethod
    def _extract_content_words(text: str) -> set[str]:
        """Extract lowercase content words, filtering out closed-class function words and short tokens."""
        tokens = tokenize_words(text)
        return {
            w.lower()
            for w in tokens
            if w.lower() not in ALL_FUNCTION_WORDS and len(w) > 2
        }
