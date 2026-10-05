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
from rightforge.llm import (
    BaseLLMProvider,
    MockLLMProvider,
    OllamaProvider,
    RevisionPromptBuilder,
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
    RevisionExecutionResult,
    RevisionGoal,
    RevisionPlan,
    SemanticCoherenceReport,
    SentencePerplexity,
    SentenceRevisionTarget,
    TransitionScore,
)
from rightforge.profiles import ProfileAggregator, ProfileComparator
from rightforge.revision import RevisionExecutor, RevisionPlanner

__all__ = [
    "__version__",
    "AnalysisResult",
    "AuthorProfile",
    "BaseAnalyzer",
    "BaseLLMProvider",
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
    "MockLLMProvider",
    "NgramProbabilityModel",
    "OllamaProvider",
    "PerplexityAnalyzer",
    "PerplexityReport",
    "ProfileAggregator",
    "ProfileComparator",
    "PunctuationAnalyzer",
    "RevisionExecutionResult",
    "RevisionExecutor",
    "RevisionGoal",
    "RevisionPlan",
    "RevisionPlanner",
    "RevisionPromptBuilder",
    "SemanticCoherenceAnalyzer",
    "SemanticCoherenceReport",
    "SentenceAnalyzer",
    "SentencePerplexity",
    "SentenceRevisionTarget",
    "StylometricVectorizer",
    "StylometryAnalyzer",
    "TransitionScore",
]
