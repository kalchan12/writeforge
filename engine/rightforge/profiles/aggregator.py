"""Profile aggregator compiling document analyses into author writing profiles."""

import math
from collections import defaultdict
from typing import Any, Sequence
from rightforge.analysis.basic import BasicTextAnalyzer
from rightforge.analysis.linguistic import LinguisticAnalyzer
from rightforge.analysis.stylometry import StylometryAnalyzer
from rightforge.models.document import AnalysisResult, Document, MetricResult
from rightforge.models.profile import AuthorProfile, MetricBaseline


class ProfileAggregator:
    """Aggregates multiple analyzed documents into an AuthorProfile with metric baselines."""

    def __init__(self) -> None:
        self.basic_analyzer = BasicTextAnalyzer()
        self.linguistic_analyzer = LinguisticAnalyzer()
        self.stylometry_analyzer = StylometryAnalyzer()

    def create_profile(
        self,
        author_name: str,
        documents: Sequence[Document | str],
        metadata: dict[str, Any] | None = None,
    ) -> AuthorProfile:
        """Create an AuthorProfile by analyzing multiple documents from an author.

        Args:
            author_name: Name or identifier of the author.
            documents: Sequence of Document instances or raw text strings.
            metadata: Optional metadata dictionary for the profile.

        Returns:
            An AuthorProfile populated with baseline statistics.
        """
        if not documents:
            raise ValueError("Cannot create an AuthorProfile from an empty document list.")

        # Analyze each document across all analytical dimensions
        analysis_results: list[AnalysisResult] = []
        for doc in documents:
            doc_obj = doc if isinstance(doc, Document) else Document(text=doc)
            combined_result = AnalysisResult(document_id=doc_obj.id, metadata=doc_obj.metadata)

            for m in self.basic_analyzer.analyze(doc_obj).metrics.values():
                combined_result.add_metric(m)
            for m in self.linguistic_analyzer.analyze(doc_obj):
                combined_result.add_metric(m)
            for m in self.stylometry_analyzer.analyze(doc_obj):
                combined_result.add_metric(m)

            analysis_results.append(combined_result)

        return self.aggregate_analysis_results(
            author_name=author_name,
            results=analysis_results,
            metadata=metadata,
        )

    def aggregate_analysis_results(
        self,
        author_name: str,
        results: Sequence[AnalysisResult],
        metadata: dict[str, Any] | None = None,
    ) -> AuthorProfile:
        """Aggregate existing AnalysisResults into an AuthorProfile.

        Args:
            author_name: Name or identifier of the author.
            results: Sequence of AnalysisResult instances.
            metadata: Optional metadata dictionary.

        Returns:
            AuthorProfile containing computed baselines.
        """
        if not results:
            raise ValueError("Cannot aggregate an empty collection of AnalysisResults.")

        metric_values: dict[str, list[float]] = defaultdict(list)
        metric_descriptions: dict[str, str | None] = {}

        for res in results:
            for name, m in res.metrics.items():
                if isinstance(m.value, (int, float)) and not isinstance(m.value, bool):
                    metric_values[name].append(float(m.value))
                    if m.description and name not in metric_descriptions:
                        metric_descriptions[name] = m.description

        baselines: dict[str, MetricBaseline] = {}
        sample_count = len(results)

        for name, vals in metric_values.items():
            if not vals:
                continue

            n = len(vals)
            mean_val = sum(vals) / n
            variance = sum((x - mean_val) ** 2 for x in vals) / n if n > 0 else 0.0
            std_dev = math.sqrt(variance)

            baseline = MetricBaseline(
                name=name,
                mean=round(mean_val, 4),
                variance=round(variance, 4),
                std_dev=round(std_dev, 4),
                min_value=round(min(vals), 4),
                max_value=round(max(vals), 4),
                sample_count=n,
                description=metric_descriptions.get(name),
            )
            baselines[name] = baseline

        return AuthorProfile(
            author_name=author_name,
            document_count=sample_count,
            baselines=baselines,
            metadata=metadata or {},
        )
