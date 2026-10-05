"""Verify package structure, versions, and module importability."""

import rightforge
import rightforge.analysis
import rightforge.core
import rightforge.models
import rightforge.text
from apps.api.main import app


def test_package_version() -> None:
    """Ensure the top-level package exposes a semantic version."""
    assert rightforge.__version__ == "0.1.0"


def test_package_exports() -> None:
    """Ensure key domain models are exposed at the top level."""
    assert hasattr(rightforge, "Document")
    assert hasattr(rightforge, "MetricResult")
    assert hasattr(rightforge, "AnalysisResult")
    assert hasattr(rightforge, "PerplexityAnalyzer")
    assert hasattr(rightforge, "PerplexityReport")
    assert hasattr(rightforge, "RevisionPlanner")
    assert hasattr(rightforge, "RevisionPlan")
    assert hasattr(rightforge, "RevisionExecutor")
    assert hasattr(rightforge, "RevisionExecutionResult")
    assert hasattr(rightforge, "DatabaseManager")


def test_api_app_instantiated() -> None:
    """Ensure the FastAPI application is importable and configured."""
    assert app.title == "RightForge API"
    assert app.version == "0.1.0"
