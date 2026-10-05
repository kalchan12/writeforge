"""Domain models for Author Writing Profiles and metric baselines."""

import math
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field


class MetricBaseline(BaseModel):
    """Statistical distribution baseline for a specific metric across an author's corpus."""

    name: str
    mean: float
    variance: float
    std_dev: float
    min_value: float
    max_value: float
    sample_count: int
    description: str | None = None

    def z_score(self, value: float) -> float:
        """Calculate the standard score (z-score) of an observation relative to this baseline."""
        if self.std_dev == 0.0:
            return 0.0
        return (value - self.mean) / self.std_dev

    def is_within_bounds(self, value: float, num_std_devs: float = 2.0) -> bool:
        """Check if an observed value lies within a specified standard deviation band."""
        if self.std_dev == 0.0:
            return math.isclose(value, self.mean, abs_tol=1e-5)
        return abs(self.z_score(value)) <= num_std_devs


class AuthorProfile(BaseModel):
    """Represents the quantitative stylistic signature of an author."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    author_name: str
    document_count: int
    baselines: dict[str, MetricBaseline] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_baseline(self, baseline: MetricBaseline) -> None:
        """Add or update a metric baseline in the profile."""
        self.baselines[baseline.name] = baseline
        self.updated_at = datetime.now(timezone.utc)
