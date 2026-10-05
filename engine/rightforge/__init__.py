"""RightForge: Local-first writing analysis and author-style research platform."""

__version__ = "0.1.0"

from rightforge.analysis import BasicTextAnalyzer
from rightforge.models import AnalysisResult, Document, MetricResult

__all__ = [
    "__version__",
    "AnalysisResult",
    "BasicTextAnalyzer",
    "Document",
    "MetricResult",
]
