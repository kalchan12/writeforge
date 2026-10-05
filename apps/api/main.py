"""FastAPI entrypoint for the RightForge application."""

from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel

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


@app.get("/health", response_model=HealthResponse)
def get_health() -> dict[str, Any]:
    """Basic health check endpoint confirming the API service is operational."""
    return {
        "status": "healthy",
        "service": "rightforge-api",
        "version": "0.1.0",
    }
