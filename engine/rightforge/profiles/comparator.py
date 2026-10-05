"""Profile comparator evaluating document alignment against Author Writing Profiles."""

import math
from typing import Sequence
from rightforge.analysis.basic import BasicTextAnalyzer
from rightforge.analysis.linguistic import LinguisticAnalyzer
from rightforge.analysis.stylometry import StylometryAnalyzer
from rightforge.models.comparison import ConsistencyReport, MetricDeviation
from rightforge.models.document import AnalysisResult, Document
from rightforge.models.profile import AuthorProfile


class ProfileComparator:
    """Compares text documents against Author Writing Profiles to measure stylistic consistency."""

    def __init__(self) -> None:
        self.basic_analyzer = BasicTextAnalyzer()
        self.linguistic_analyzer = LinguisticAnalyzer()
        self.stylometry_analyzer = StylometryAnalyzer()

    def compare(
        self,
        profile: AuthorProfile,
        target: Document | str | AnalysisResult,
        outlier_threshold: float = 2.0,
    ) -> ConsistencyReport:
        """Compare a target document against an AuthorProfile.

        Args:
            profile: The reference AuthorProfile.
            target: A Document, raw text string, or precomputed AnalysisResult.
            outlier_threshold: Number of standard deviations to trigger an outlier flag (default 2.0).

        Returns:
            A structured ConsistencyReport.
        """
        if isinstance(target, AnalysisResult):
            analysis = target
            doc_id = target.document_id
        else:
            doc = target if isinstance(target, Document) else Document(text=target)
            doc_id = doc.id
            analysis = AnalysisResult(document_id=doc.id, metadata=doc.metadata)

            for m in self.basic_analyzer.analyze(doc).metrics.values():
                analysis.add_metric(m)
            for m in self.linguistic_analyzer.analyze(doc):
                analysis.add_metric(m)
            for m in self.stylometry_analyzer.analyze(doc):
                analysis.add_metric(m)

        deviations: dict[str, MetricDeviation] = {}
        fidelity_scores: list[float] = []
        outliers: list[str] = []

        for name, baseline in profile.baselines.items():
            if name not in analysis.metrics:
                continue

            raw_val = analysis.metrics[name].value
            if not isinstance(raw_val, (int, float)) or isinstance(raw_val, bool):
                continue

            observed = float(raw_val)

            # Compute standard score (z-score)
            if baseline.std_dev > 0.0:
                z = (observed - baseline.mean) / baseline.std_dev
            else:
                if math.isclose(observed, baseline.mean, abs_tol=1e-5):
                    z = 0.0
                else:
                    scale = max(abs(baseline.mean), 1.0)
                    z = ((observed - baseline.mean) / scale) * 2.0

            abs_z = abs(z)
            is_outlier = abs_z > outlier_threshold
            if is_outlier:
                outliers.append(name)

            # Gaussian-decay fidelity score: s = exp(-0.5 * (abs_z / 2.0)^2)
            # Scores range strictly between 1.0 (exact match) and 0.0 (extreme divergence)
            metric_score = math.exp(-0.5 * (abs_z / 2.0) ** 2)
            fidelity_scores.append(metric_score)

            deviations[name] = MetricDeviation(
                metric_name=name,
                observed_value=round(observed, 4),
                baseline_mean=baseline.mean,
                baseline_std_dev=baseline.std_dev,
                z_score=round(z, 4),
                absolute_z_score=round(abs_z, 4),
                is_outlier=is_outlier,
                description=baseline.description,
            )

        if fidelity_scores:
            composite_score = round(sum(fidelity_scores) / len(fidelity_scores), 4)
        else:
            composite_score = 0.0

        # Qualitative assessment
        if composite_score >= 0.85:
            fidelity_level = "high"
        elif composite_score >= 0.65:
            fidelity_level = "moderate"
        elif composite_score >= 0.45:
            fidelity_level = "low"
        else:
            fidelity_level = "divergent"

        outlier_text = (
            f"{len(outliers)} stylistic outlier(s) detected ({', '.join(outliers[:3])}{'...' if len(outliers) > 3 else ''})."
            if outliers
            else "No significant stylistic outliers detected."
        )
        summary = (
            f"Document demonstrates {fidelity_level} stylistic alignment with author "
            f"'{profile.author_name}' (consistency score: {composite_score:.2f}). {outlier_text}"
        )

        return ConsistencyReport(
            author_profile_id=profile.id,
            author_name=profile.author_name,
            document_id=doc_id,
            consistency_score=composite_score,
            evaluated_metrics_count=len(deviations),
            outlier_count=len(outliers),
            outliers=outliers,
            deviations=deviations,
            summary=summary,
        )
