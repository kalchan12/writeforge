"""Deterministic unit tests for StylometricVectorizer."""

import numpy as np
from rightforge.ml.vectorizer import FEATURE_NAMES, StylometricVectorizer
from rightforge.models.document import Document


def test_vectorizer_feature_names() -> None:
    vectorizer = StylometricVectorizer()
    assert len(vectorizer.feature_names) == 31
    assert "yules_k" in vectorizer.feature_names
    assert "type_token_ratio" in vectorizer.feature_names
    assert "mean_paragraph_coherence" in vectorizer.feature_names


def test_vectorizer_empty_text() -> None:
    vectorizer = StylometricVectorizer()
    vec = vectorizer.vectorize("")

    assert len(vec) == 31
    assert all(isinstance(v, float) for v in vec)
    assert not any(np.isnan(v) or np.isinf(v) for v in vec)


def test_vectorizer_transform_matrix_shape() -> None:
    vectorizer = StylometricVectorizer()
    docs = [
        Document(text="This is a simple first document."),
        Document(text="Here is another document with different length and words."),
        Document(text="Third short text."),
    ]

    matrix = vectorizer.transform(docs)
    assert isinstance(matrix, np.ndarray)
    assert matrix.shape == (3, 31)
    assert not np.isnan(matrix).any()


def test_vectorizer_fit_transform_pipeline() -> None:
    vectorizer = StylometricVectorizer()
    texts = ["Sample text one.", "Sample text two."]
    transformed = vectorizer.fit_transform(texts)

    assert isinstance(transformed, np.ndarray)
    assert transformed.shape == (2, 31)
