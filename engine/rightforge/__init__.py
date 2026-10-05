"""RightForge: Local-first writing analysis and author-style research platform."""

__version__ = "0.1.0"

from rightforge.analysis import (
    BaseAnalyzer,
    BasicTextAnalyzer,
    LexicalAnalyzer,
    LinguisticAnalyzer,
    PerplexityAnalyzer,
    PunctuationAnalyzer,
    SemanticCoherenceAnalyzer,
    SentenceAnalyzer,
    StylometryAnalyzer,
)
from rightforge.ml import (
    FEATURE_NAMES,
    BaseProbabilityModel,
    HuggingFaceProbabilityModel,
    NgramProbabilityModel,
    StylometricVectorizer,
)
from rightforge.models import (
    AnalysisResult,
    AuthorProfile,
    ConsistencyReport,
    Document,
    MetricBaseline,
    MetricDeviation,
    MetricResult,
    PerplexityReport,
    SemanticCoherenceReport,
    SentencePerplexity,
    TransitionScore,
)
from rightforge.profiles import ProfileAggregator, ProfileComparator

__all__ = [
    "__version__",
    "AnalysisResult",
    "AuthorProfile",
    "BaseAnalyzer",
    "BaseProbabilityModel",
    "BasicTextAnalyzer",
    "ConsistencyReport",
    "Document",
    "FEATURE_NAMES",
    "HuggingFaceProbabilityModel",
    "LexicalAnalyzer",
    "LinguisticAnalyzer",
    "MetricBaseline",
    "MetricDeviation",
    "MetricResult",
    "NgramProbabilityModel",
    "PerplexityAnalyzer",
    "PerplexityReport",
    "ProfileAggregator",
    "ProfileComparator",
    "PunctuationAnalyzer",
    "SemanticCoherenceAnalyzer",
    "SemanticCoherenceReport",
    "SentenceAnalyzer",
    "SentencePerplexity",
    "StylometricVectorizer",
    "StylometryAnalyzer",
    "TransitionScore",
]
