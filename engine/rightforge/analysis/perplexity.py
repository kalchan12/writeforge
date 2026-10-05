"""Perplexity and burstiness analyzer evaluating information-theoretic predictability."""

import math
from rightforge.analysis.base import BaseAnalyzer
from rightforge.ml.probability import BaseProbabilityModel, NgramProbabilityModel
from rightforge.models.document import Document, MetricResult
from rightforge.models.transformers import PerplexityReport, SentencePerplexity
from rightforge.text.segmentation import split_sentences, tokenize_words


class PerplexityAnalyzer(BaseAnalyzer):
    """Evaluates token probability trajectories, sentence-level perplexity, and burstiness."""

    def __init__(self, model: BaseProbabilityModel | None = None) -> None:
        self.model = model if model is not None else NgramProbabilityModel()

    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Extract information-theoretic metrics for document analysis pipeline."""
        report = self.analyze_perplexity(target)
        return [
            MetricResult(
                name="overall_perplexity",
                value=report.overall_perplexity,
                description="Document-level geometric mean perplexity exp(-1/N * sum(log P(w)))",
            ),
            MetricResult(
                name="mean_sentence_perplexity",
                value=report.mean_sentence_perplexity,
                description="Average sentence-level perplexity",
            ),
            MetricResult(
                name="burstiness",
                value=report.burstiness,
                description="Perplexity fluctuation across sentences (coefficient of variation)",
            ),
            MetricResult(
                name="min_sentence_perplexity",
                value=report.min_sentence_perplexity,
                description="Minimum sentence-level perplexity",
            ),
            MetricResult(
                name="max_sentence_perplexity",
                value=report.max_sentence_perplexity,
                description="Maximum sentence-level perplexity",
            ),
            MetricResult(
                name="sentence_count",
                value=float(report.sentence_count),
                description="Total sentences evaluated for perplexity",
            ),
        ]

    def analyze_perplexity(self, target: Document | str) -> PerplexityReport:
        """Perform comprehensive sentence perplexity tracking and burstiness calculation."""
        text = self._extract_text(target)
        doc_id = target.id if isinstance(target, Document) else None

        sentences = split_sentences(text)
        if not sentences or not text.strip():
            return PerplexityReport(
                document_id=doc_id,
                overall_perplexity=0.0,
                mean_sentence_perplexity=0.0,
                burstiness=0.0,
                min_sentence_perplexity=0.0,
                max_sentence_perplexity=0.0,
                sentence_count=0,
                sentence_perplexities=[],
                summary="Document contains no readable sentences for perplexity analysis.",
            )

        sentence_results: list[SentencePerplexity] = []
        total_tokens = 0
        total_logprob = 0.0

        for idx, sentence in enumerate(sentences):
            tokens = tokenize_words(sentence, lowercase=True)
            if not tokens:
                continue

            logprobs = self.model.score_tokens(tokens)
            sent_logprob_sum = sum(logprobs)
            sent_token_count = len(tokens)
            mean_logprob = sent_logprob_sum / sent_token_count
            sent_ppl = math.exp(-mean_logprob)

            sentence_results.append(
                SentencePerplexity(
                    sentence_index=idx,
                    text=sentence,
                    token_count=sent_token_count,
                    perplexity=round(sent_ppl, 4),
                    mean_logprob=round(mean_logprob, 4),
                )
            )

            total_tokens += sent_token_count
            total_logprob += sent_logprob_sum

        if not sentence_results:
            return PerplexityReport(
                document_id=doc_id,
                overall_perplexity=0.0,
                mean_sentence_perplexity=0.0,
                burstiness=0.0,
                min_sentence_perplexity=0.0,
                max_sentence_perplexity=0.0,
                sentence_count=0,
                sentence_perplexities=[],
                summary="Document yielded zero valid tokens for perplexity analysis.",
            )

        overall_ppl = (
            math.exp(-total_logprob / total_tokens) if total_tokens > 0 else 0.0
        )
        sent_ppls = [s.perplexity for s in sentence_results]
        mean_sent_ppl = sum(sent_ppls) / len(sent_ppls)

        if len(sent_ppls) > 1 and mean_sent_ppl > 0:
            variance = sum((p - mean_sent_ppl) ** 2 for p in sent_ppls) / len(sent_ppls)
            std_dev = math.sqrt(variance)
            burstiness = std_dev / mean_sent_ppl
        else:
            burstiness = 0.0

        min_sent_ppl = min(sent_ppls)
        max_sent_ppl = max(sent_ppls)

        # Characterize cadence from burstiness
        if burstiness >= 0.40:
            burstiness_desc = "dynamic cadence with high sentence-to-sentence variation"
        elif burstiness >= 0.18:
            burstiness_desc = "moderate variability across sentence structures"
        else:
            burstiness_desc = "uniform cadence with low variance (typical of synthetic or repetitive text)"

        summary = (
            f"Document analyzed across {len(sentence_results)} sentence(s) with overall perplexity "
            f"{overall_ppl:.2f} and burstiness {burstiness:.3f} ({burstiness_desc})."
        )

        return PerplexityReport(
            document_id=doc_id,
            overall_perplexity=round(overall_ppl, 4),
            mean_sentence_perplexity=round(mean_sent_ppl, 4),
            burstiness=round(burstiness, 4),
            min_sentence_perplexity=round(min_sent_ppl, 4),
            max_sentence_perplexity=round(max_sent_ppl, 4),
            sentence_count=len(sentence_results),
            sentence_perplexities=sentence_results,
            summary=summary,
        )
