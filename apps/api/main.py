"""FastAPI entrypoint for the RightForge application."""

from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

from rightforge.analysis import (
    BasicTextAnalyzer,
    LinguisticAnalyzer,
    PerplexityAnalyzer,
    SemanticCoherenceAnalyzer,
    StylometryAnalyzer,
)
from rightforge.models import (
    AnalysisResult,
    AuthorProfile,
    ConsistencyReport,
    Document,
    PerplexityReport,
    RevisionPlan,
    SemanticCoherenceReport,
)
from rightforge.profiles import ProfileAggregator, ProfileComparator
from rightforge.revision import RevisionPlanner

app = FastAPI(
    title="RightForge API",
    description="Local-first writing analysis and author-style research platform API",
    version="0.1.0",
)


class HealthResponse(BaseModel):
    """Structured response for service health verification."""

    status: str
    service: str
    version: str


class TextAnalysisRequest(BaseModel):
    """Request payload for document analysis endpoints."""

    text: str = Field(..., description="The input text content to analyze")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional metadata attributes"
    )


class ProfileDocumentItem(BaseModel):
    """Document entry for profile creation."""

    text: str = Field(..., description="Document text content")
    metadata: dict[str, Any] = Field(default_factory=dict)


class CreateProfileRequest(BaseModel):
    """Request payload for author profile generation."""

    author_name: str = Field(..., min_length=1, description="Author identifier or name")
    documents: list[ProfileDocumentItem] = Field(
        ..., min_length=1, description="Sample documents from the author"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional profile metadata"
    )


class CompareProfileRequest(BaseModel):
    """Request payload for comparing a document against an author profile."""

    profile: AuthorProfile = Field(..., description="Target reference AuthorProfile")
    text: str = Field(..., min_length=1, description="Document text to evaluate")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional document metadata"
    )
    outlier_threshold: float = Field(
        default=2.0,
        ge=0.5,
        le=5.0,
        description="Standard deviation threshold for outlier identification",
    )


class RevisionPlanRequest(BaseModel):
    """Request payload for revision strategy generation."""

    text: str = Field(..., min_length=1, description="Document text to generate revision guidance for")
    profile: AuthorProfile | None = Field(
        default=None, description="Optional target AuthorProfile to steer style alignment"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional document metadata"
    )
    outlier_threshold: float = Field(
        default=2.0,
        ge=0.5,
        le=5.0,
        description="Standard deviation threshold for outlier identification",
    )


@app.get("/health", response_model=HealthResponse)
def get_health() -> dict[str, Any]:
    """Basic health check endpoint confirming the API service is operational."""
    return {
        "status": "healthy",
        "service": "rightforge-api",
        "version": "0.1.0",
    }


@app.post("/analysis/basic", response_model=AnalysisResult)
def analyze_basic(request: TextAnalysisRequest) -> AnalysisResult:
    """Analyze a document and compute deterministic surface text statistics."""
    doc = Document(text=request.text, metadata=request.metadata)
    analyzer = BasicTextAnalyzer()
    return analyzer.analyze(doc)


@app.post("/analysis/linguistic", response_model=AnalysisResult)
def analyze_linguistic(request: TextAnalysisRequest) -> AnalysisResult:
    """Analyze a document and compute modular linguistic metrics (lexical, sentence, punctuation)."""
    doc = Document(text=request.text, metadata=request.metadata)
    analyzer = LinguisticAnalyzer()
    return analyzer.analyze_document(doc)


@app.post("/analysis/stylometry", response_model=AnalysisResult)
def analyze_stylometry(request: TextAnalysisRequest) -> AnalysisResult:
    """Analyze a document and compute stylometric metrics (vocabulary richness, function words, readability)."""
    doc = Document(text=request.text, metadata=request.metadata)
    analyzer = StylometryAnalyzer()
    return analyzer.analyze_document(doc)


@app.post("/analysis/coherence", response_model=SemanticCoherenceReport)
def analyze_coherence(request: TextAnalysisRequest) -> SemanticCoherenceReport:
    """Analyze document semantic coherence, lexical flow, and paragraph transitions."""
    doc = Document(text=request.text, metadata=request.metadata)
    analyzer = SemanticCoherenceAnalyzer()
    return analyzer.analyze_coherence(doc)


@app.post("/analysis/perplexity", response_model=PerplexityReport)
def analyze_perplexity(request: TextAnalysisRequest) -> PerplexityReport:
    """Analyze token probability trajectories, sentence perplexity, and burstiness."""
    doc = Document(text=request.text, metadata=request.metadata)
    analyzer = PerplexityAnalyzer()
    return analyzer.analyze_perplexity(doc)


@app.post("/profiles/create", response_model=AuthorProfile)
def create_profile(request: CreateProfileRequest) -> AuthorProfile:
    """Construct an AuthorProfile with metric baselines aggregated across author documents."""
    docs = [Document(text=d.text, metadata=d.metadata) for d in request.documents]
    aggregator = ProfileAggregator()
    return aggregator.create_profile(
        author_name=request.author_name,
        documents=docs,
        metadata=request.metadata,
    )


@app.post("/profiles/compare", response_model=ConsistencyReport)
def compare_profile(request: CompareProfileRequest) -> ConsistencyReport:
    """Evaluate document alignment and consistency score relative to an AuthorProfile."""
    doc = Document(text=request.text, metadata=request.metadata)
    comparator = ProfileComparator()
    return comparator.compare(
        profile=request.profile,
        target=doc,
        outlier_threshold=request.outlier_threshold,
    )


@app.post("/revision/plan", response_model=RevisionPlan)
def plan_revision(request: RevisionPlanRequest) -> RevisionPlan:
    """Construct rule-governed revision recommendations and style goals."""
    doc = Document(text=request.text, metadata=request.metadata)
    planner = RevisionPlanner()
    return planner.generate_plan(
        target=doc,
        profile=request.profile,
        outlier_threshold=request.outlier_threshold,
    )
