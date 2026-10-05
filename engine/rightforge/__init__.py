"""RightForge: Local-first writing analysis and author-style research platform."""

__version__ = "0.1.0"

from rightforge.analysis import (
    BaseAnalyzer,
    BasicTextAnalyzer,
    LexicalAnalyzer,
    LinguisticAnalyzer,
    PunctuationAnalyzer,
    SentenceAnalyzer,
    StylometryAnalyzer,
)
from rightforge.models import (
    AnalysisResult,
    AuthorProfile,
    Document,
    MetricBaseline,
    MetricResult,
)
from rightforge.profiles import ProfileAggregator

__all__ = [
    "__version__",
    "AnalysisResult",
    "AuthorProfile",
    "BaseAnalyzer",
    "BasicTextAnalyzer",
    "Document",
    "LexicalAnalyzer",
    "LinguisticAnalyzer",
    "MetricBaseline",
    "MetricResult",
    "ProfileAggregator",
    "PunctuationAnalyzer",
    "SentenceAnalyzer",
    "StylometryAnalyzer",
]
