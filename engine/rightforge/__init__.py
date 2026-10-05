"""RightForge: Local-first writing analysis and author-style research platform."""

__version__ = "0.1.0"

from rightforge.analysis import (
    BaseAnalyzer,
    BasicTextAnalyzer,
    LexicalAnalyzer,
    LinguisticAnalyzer,
    PunctuationAnalyzer,
    SemanticCoherenceAnalyzer,
    SentenceAnalyzer,
    StylometryAnalyzer,
)
from rightforge.ml import FEATURE_NAMES, StylometricVectorizer
from rightforge.models import (
    AnalysisResult,
    AuthorProfile,
    ConsistencyReport,
    Document,
    MetricBaseline,
    MetricDeviation,
    MetricResult,
    SemanticCoherenceReport,
    TransitionScore,
)
from rightforge.profiles import ProfileAggregator, ProfileComparator

__all__ = [
    "__version__",
    "AnalysisResult",
    "AuthorProfile",
    "BaseAnalyzer",
    "BasicTextAnalyzer",
    "ConsistencyReport",
    "Document",
    "FEATURE_NAMES",
    "LexicalAnalyzer",
    "LinguisticAnalyzer",
    "MetricBaseline",
    "MetricDeviation",
    "MetricResult",
    "ProfileAggregator",
    "ProfileComparator",
    "PunctuationAnalyzer",
    "SemanticCoherenceAnalyzer",
    "SemanticCoherenceReport",
    "SentenceAnalyzer",
    "StylometricVectorizer",
    "StylometryAnalyzer",
    "TransitionScore",
]
