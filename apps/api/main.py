"""FastAPI entrypoint for the RightForge application."""

from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

from rightforge.analysis import (
    BasicTextAnalyzer,
    LinguisticAnalyzer,
    StylometryAnalyzer,
)
from rightforge.models import AnalysisResult, AuthorProfile, Document
from rightforge.profiles import ProfileAggregator

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
