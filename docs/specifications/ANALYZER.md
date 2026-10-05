# Analyzer Engine Specification

## 1. Overview

The analyzer engine (`engine/rightforge/analysis/`) is responsible for extracting quantifiable properties and linguistic metrics from text documents.

## 2. Core Interface Contract

Analyzers in RightForge follow a composable, functional design:

```python
class BaseAnalyzer(ABC):
    """Abstract base class for all metric analyzers."""

    @abstractmethod
    def analyze(self, document: Document) -> list[MetricResult]:
        """Extract a collection of MetricResults from the given Document."""
        pass
```

* **Input**: An instance of `rightforge.models.Document`.
* **Output**: A list or dictionary of `rightforge.models.MetricResult` wrapped in an `AnalysisResult`.
* **Side-Effects**: Analyzers must be stateless and free of side-effects.

## 3. Current Phase 0 Status

* **Implemented**: Base domain entities `Document`, `MetricResult`, `AnalysisResult` in `engine/rightforge/models/`.
* **Deferred to Phase 1**: Basic surface statistic analyzer (word count, sentence count, char count, etc.).
* **Deferred to Phase 2**: Modular lexical, sentence, and punctuation analyzers.
