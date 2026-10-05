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
from rightforge.models import AnalysisResult, Document, MetricResult

__all__ = [
    "__version__",
    "AnalysisResult",
    "BaseAnalyzer",
    "BasicTextAnalyzer",
    "Document",
    "LexicalAnalyzer",
    "LinguisticAnalyzer",
    "MetricResult",
    "PunctuationAnalyzer",
    "SentenceAnalyzer",
    "StylometryAnalyzer",
]
