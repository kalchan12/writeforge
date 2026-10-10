"""Domain models for RightForge."""

from rightforge.models.ai_detection import AIDetectionReport, AISignal
from rightforge.models.comparison import ConsistencyReport, MetricDeviation
from rightforge.models.document import AnalysisResult, Document, MetricResult
from rightforge.models.execution import RevisionExecutionResult
from rightforge.models.profile import AuthorProfile, MetricBaseline
from rightforge.models.revision import RevisionGoal, RevisionPlan, SentenceRevisionTarget
from rightforge.models.semantics import SemanticCoherenceReport, TransitionScore
from rightforge.models.transformers import PerplexityReport, SentencePerplexity

__all__ = [
    "AIDetectionReport",
    "AISignal",
    "AnalysisResult",
    "AuthorProfile",
    "ConsistencyReport",
    "Document",
    "MetricBaseline",
    "MetricDeviation",
    "MetricResult",
    "PerplexityReport",
    "RevisionExecutionResult",
    "RevisionGoal",
    "RevisionPlan",
    "SemanticCoherenceReport",
    "SentencePerplexity",
    "SentenceRevisionTarget",
    "TransitionScore",
]
