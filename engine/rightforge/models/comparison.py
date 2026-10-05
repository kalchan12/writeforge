"""Domain models for comparing text documents against Author Writing Profiles."""

from pydantic import BaseModel, Field


class MetricDeviation(BaseModel):
    """Measures deviation of an observed metric value from an author's baseline distribution."""

    metric_name: str
    observed_value: float
    baseline_mean: float
    baseline_std_dev: float
    z_score: float
    absolute_z_score: float
    is_outlier: bool
    description: str | None = None


class ConsistencyReport(BaseModel):
    """Structured report assessing stylistic fidelity of a document relative to an author profile."""

    author_profile_id: str
    author_name: str
    document_id: str | None = None
    consistency_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Composite author-style consistency score between 0.0 (divergent) and 1.0 (identical)",
    )
    evaluated_metrics_count: int
    outlier_count: int
    outliers: list[str] = Field(
        default_factory=list,
        description="List of metric names exceeding the outlier threshold",
    )
    deviations: dict[str, MetricDeviation] = Field(
        default_factory=dict,
        description="Detailed metric-by-metric deviation records",
    )
    summary: str = Field(..., description="Concise qualitative summary of consistency findings")
