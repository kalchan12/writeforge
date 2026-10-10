"""Pydantic models for composite AI detection scoring."""

from pydantic import BaseModel, Field


class AISignal(BaseModel):
    """Individual signal contributing to the composite AI detection score."""

    name: str = Field(..., description="Human-readable signal name")
    raw_value: float = Field(..., description="Raw metric value observed in the text")
    sub_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Normalized signal score (0.0 = human-like, 1.0 = AI-like)",
    )
    weight: float = Field(..., description="Weight of this signal in the composite score")
    description: str = Field(..., description="Explanation of what this signal measures")


class AIDetectionReport(BaseModel):
    """Composite AI detection probability report."""

    ai_score: float = Field(
        ..., ge=0.0, le=1.0,
        description="Composite AI probability (0.0 = definitely human, 1.0 = definitely AI)",
    )
    ai_score_percent: int = Field(
        ..., ge=0, le=100,
        description="AI probability as integer percentage",
    )
    verdict: str = Field(..., description="Human-readable verdict: Likely Human, Mixed/Uncertain, or Likely AI")
    confidence: str = Field(..., description="Confidence level: low, medium, or high")
    signals: list[AISignal] = Field(default_factory=list, description="Individual signal breakdown")
    summary: str = Field(..., description="Human-readable explanation of the analysis")
