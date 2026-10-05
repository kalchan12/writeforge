"""Base abstraction for modular and composable metric analyzers."""

from abc import ABC, abstractmethod
from typing import Sequence
from rightforge.models import Document, MetricResult


class BaseAnalyzer(ABC):
    """Abstract base class for all modular metric analyzers."""

    @abstractmethod
    def analyze(self, target: Document | str) -> list[MetricResult]:
        """Extract a list of MetricResult items from the given Document or text string.

        Args:
            target: A Document instance or raw text string.

        Returns:
            A list of computed MetricResult objects.
        """
        pass

    @staticmethod
    def _extract_text(target: Document | str) -> str:
        """Extract raw text string from Document or str target."""
        if isinstance(target, Document):
            return target.text
        return target
