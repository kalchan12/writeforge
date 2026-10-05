"""Core domain models for text representation and analysis results."""

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from pydantic import BaseModel, Field


class Document(BaseModel):
    """Represents a text document undergoing analysis."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MetricResult(BaseModel):
    """Represents an individual measured metric value."""

    name: str
    value: float | int | str | bool | dict[str, Any] | list[Any]
    description: str | None = None


class AnalysisResult(BaseModel):
    """Represents the structured outcome of analyzing a document."""

    document_id: str | None = None
    metrics: dict[str, MetricResult] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def add_metric(self, metric: MetricResult) -> None:
        """Add or update an individual metric result."""
        self.metrics[metric.name] = metric
