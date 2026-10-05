"""Domain models for perplexity, token probability trajectories, and burstiness modeling."""

from pydantic import BaseModel, Field


class SentencePerplexity(BaseModel):
    """Perplexity and log-likelihood measurements for an individual sentence."""

    sentence_index: int
    text: str
    token_count: int
    perplexity: float
    mean_logprob: float


class PerplexityReport(BaseModel):
    """Document-level information-theoretic analysis evaluating token probability and burstiness."""

    document_id: str | None = None
    overall_perplexity: float = Field(
        ..., description="Document-wide geometric mean perplexity exp(-1/N * sum(log P(w)))"
    )
    mean_sentence_perplexity: float = Field(
        ..., description="Average sentence-level perplexity"
    )
    burstiness: float = Field(
        ...,
        description="Perplexity fluctuation across sentences (coefficient of variation: std_dev / mean)",
    )
    min_sentence_perplexity: float
    max_sentence_perplexity: float
    sentence_count: int
    sentence_perplexities: list[SentencePerplexity] = Field(
        default_factory=list, description="Per-sentence perplexity progression"
    )
    summary: str = Field(..., description="Qualitative analysis of predictability and cadence")
