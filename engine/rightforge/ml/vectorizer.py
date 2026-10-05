"""Feature extraction mapping text documents into normalized stylometric feature vectors."""

from typing import Any, Sequence
from rightforge.analysis.basic import BasicTextAnalyzer
from rightforge.analysis.lexical import LexicalAnalyzer
from rightforge.analysis.punctuation import PunctuationAnalyzer
from rightforge.analysis.semantics import SemanticCoherenceAnalyzer
from rightforge.analysis.sentence import SentenceAnalyzer
from rightforge.analysis.stylometry import StylometryAnalyzer
from rightforge.models.document import Document

FEATURE_NAMES: list[str] = [
    # Surface & Sentence structure
    "avg_words_per_sentence",
    "avg_chars_per_word",
    "sentence_length_std_dev",
    "sentence_length_variance",
    # Lexical richness
    "type_token_ratio",
    "root_type_token_ratio",
    "average_word_length",
    "long_word_ratio",
    # Punctuation densities & marks
    "punct_comma_count",
    "punct_semicolon_count",
    "punct_colon_count",
    "punct_dash_count",
    "punct_quote_count",
    "punctuation_density_per_char",
    "punctuation_density_per_word",
    # Stylometric invariants & vocabulary concentration
    "hapax_legomena_ratio",
    "dis_legomena_ratio",
    "yules_k",
    "simpsons_d",
    "simpsons_diversity",
    # Closed-class function word distributions
    "function_word_ratio",
    "preposition_ratio",
    "pronoun_ratio",
    "conjunction_ratio",
    "auxiliary_verb_ratio",
    "determiner_ratio",
    # Readability
    "flesch_reading_ease",
    "flesch_kincaid_grade",
    # Semantic coherence
    "mean_paragraph_coherence",
    "mean_sentence_coherence",
    "lexical_repetition_rate",
]


class StylometricVectorizer:
    """Extracts fixed-dimensional numerical feature vectors from text documents for ML classifiers."""

    def __init__(self) -> None:
        self.basic_analyzer = BasicTextAnalyzer()
        self.lexical_analyzer = LexicalAnalyzer()
        self.sentence_analyzer = SentenceAnalyzer()
        self.punctuation_analyzer = PunctuationAnalyzer()
        self.stylometry_analyzer = StylometryAnalyzer()
        self.coherence_analyzer = SemanticCoherenceAnalyzer()
        self.feature_names = FEATURE_NAMES

    def vectorize(self, target: Document | str) -> list[float]:
        """Transform a single document or text string into a 1D feature vector.

        Args:
            target: Document or string to vectorize.

        Returns:
            List of float values matching FEATURE_NAMES in exact order.
        """
        doc = target if isinstance(target, Document) else Document(text=target)

        # Collect metrics from all analyzers
        metrics: dict[str, float] = {}

        for m in self.basic_analyzer.analyze(doc).metrics.values():
            if isinstance(m.value, (int, float)) and not isinstance(m.value, bool):
                metrics[m.name] = float(m.value)

        for m in self.lexical_analyzer.analyze(doc):
            metrics[m.name] = float(m.value)

        for m in self.sentence_analyzer.analyze(doc):
            metrics[m.name] = float(m.value)

        for m in self.punctuation_analyzer.analyze(doc):
            metrics[m.name] = float(m.value)

        for m in self.stylometry_analyzer.analyze(doc):
            metrics[m.name] = float(m.value)

        for m in self.coherence_analyzer.analyze(doc):
            metrics[m.name] = float(m.value)

        vector: list[float] = []
        for feat in self.feature_names:
            vector.append(round(metrics.get(feat, 0.0), 4))

        return vector

    def transform(self, targets: Sequence[Document | str]) -> Any:
        """Transform a sequence of documents into a 2D feature matrix (NumPy array)."""
        vectors = [self.vectorize(t) for t in targets]
        try:
            import numpy as np
            return np.array(vectors, dtype=float)
        except ImportError:
            return vectors

    def fit(self, targets: Sequence[Document | str], y: Any = None) -> "StylometricVectorizer":
        """No-op fit method for scikit-learn pipeline compatibility."""
        return self

    def fit_transform(self, targets: Sequence[Document | str], y: Any = None) -> Any:
        """Fit and transform documents in one step."""
        return self.transform(targets)
