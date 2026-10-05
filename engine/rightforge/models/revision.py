"""Domain models for rule-guided stylistic revision planning."""

from pydantic import BaseModel, Field


class RevisionGoal(BaseModel):
    """High-level stylistic or metric goal guiding the revision process."""

    metric_name: str = Field(..., description="Target metric identifier (e.g. mean_sentence_length)")
    description: str = Field(..., description="Human-readable explanation of why this target was set")
    current_value: float = Field(..., description="Observed metric value in current document")
    target_value: float = Field(..., description="Desired target value or profile baseline mean")
    direction: str = Field(..., description="'increase', 'decrease', or 'maintain'")
    severity: str = Field(default="medium", description="'low', 'medium', or 'high' priority")


class SentenceRevisionTarget(BaseModel):
    """Sentence-level concrete intervention suggestion."""

    sentence_index: int = Field(..., description="0-indexed position of sentence in document")
    original_text: str = Field(..., description="Verbatim sentence text")
    issue_type: str = Field(
        ...,
        description="Category of issue (e.g. excessive_length, cadence_monotony, repetitive_opener)",
    )
    suggestion: str = Field(..., description="Actionable prescriptive guidance for revising the sentence")
    priority: int = Field(default=2, description="1 (high), 2 (medium), or 3 (low)")


class RevisionPlan(BaseModel):
    """Synthesized revision strategy containing goals and granular sentence interventions."""

    document_id: str | None = None
    target_author: str | None = None
    goals: list[RevisionGoal] = Field(
        default_factory=list, description="Global metric targets guiding style adjustment"
    )
    sentence_targets: list[SentenceRevisionTarget] = Field(
        default_factory=list, description="Granular sentence-level revision recommendations"
    )
    total_suggestions: int = Field(
        ..., description="Total count of sentence-level recommendations generated"
    )
    summary: str = Field(..., description="Executive summary of the revision recommendations")
