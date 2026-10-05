"""Composite analyzer orchestrating lexical, sentence, and punctuation analyzers."""

from rightforge.analysis.base import BaseAnalyzer
from rightforge.analysis.lexical import LexicalAnalyzer
from rightforge.analysis.punctuation import PunctuationAnalyzer
from rightforge.analysis.sentence import SentenceAnalyzer
from rightforge.models import AnalysisResult, Document, MetricResult


class LinguisticAnalyzer(BaseAnalyzer):
    """Composes modular lexical, sentence, and punctuation analyzers into a single pipeline."""

    def __init__(
        self,
        lexical_analyzer: LexicalAnalyzer | None = None,
        sentence_analyzer: SentenceAnalyzer | None = None,
        punctuation_analyzer: PunctuationAnalyzer | None = None,
    ) -> None:
        self.lexical_analyzer = lexical_analyzer or LexicalAnalyzer()
        self.sentence_analyzer = sentence_analyzer or SentenceAnalyzer()
        self.punctuation_analyzer = punctuation_analyzer or PunctuationAnalyzer()

    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Run all constituent analyzers and return combined MetricResult items."""
        metrics: list[MetricResult] = []
        metrics.extend(self.lexical_analyzer.analyze(target))
        metrics.extend(self.sentence_analyzer.analyze(target))
        metrics.extend(self.punctuation_analyzer.analyze(target))
        return metrics

    def analyze_document(self, target: Document | str) -> AnalysisResult:
        """Run analysis and package into a structured AnalysisResult."""
        document_id = target.id if isinstance(target, Document) else None
        metadata = target.metadata if isinstance(target, Document) else {}

        result = AnalysisResult(document_id=document_id, metadata=metadata)
        for metric in self.analyze(target):
            result.add_metric(metric)
        return result
