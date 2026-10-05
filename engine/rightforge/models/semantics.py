"""Domain models for semantic coherence, lexical flow, and transition analysis."""

from pydantic import BaseModel, Field


class TransitionScore(BaseModel):
    """Measures semantic and lexical continuity between adjacent text segments."""

    from_index: int = Field(..., description="0-indexed source segment position")
    to_index: int = Field(..., description="0-indexed target segment position")
    jaccard_similarity: float = Field(..., ge=0.0, le=1.0)
    overlap_coefficient: float = Field(..., ge=0.0, le=1.0)
    shared_terms: list[str] = Field(default_factory=list)
    is_abrupt_shift: bool = Field(
        ..., description="True if lexical overlap falls below continuity threshold"
    )


class SemanticCoherenceReport(BaseModel):
    """Structured assessment of document-wide topical cohesion and segment transitions."""

    document_id: str | None = None
    paragraph_count: int
    sentence_count: int
    mean_paragraph_coherence: float = Field(
        ..., ge=0.0, le=1.0, description="Average Jaccard continuity between adjacent paragraphs"
    )
    mean_sentence_coherence: float = Field(
        ..., ge=0.0, le=1.0, description="Average Jaccard continuity between adjacent sentences"
    )
    lexical_repetition_rate: float = Field(
        ..., ge=0.0, le=1.0, description="Proportion of content words carried across paragraphs"
    )
    abrupt_transitions_count: int = Field(
        ..., description="Count of adjacent paragraph transitions with minimal lexical continuity"
    )
    paragraph_transitions: list[TransitionScore] = Field(
        default_factory=list, description="Ordered segment-by-segment continuity records"
    )
    summary: str = Field(..., description="Qualitative summary of document coherence")
