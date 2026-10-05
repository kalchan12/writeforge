# Architecture Specification

## 1. System Overview

RightForge separates concerns cleanly across three primary layers:
1. **Engine Layer (`engine/rightforge/`)**: Standalone, pure-Python text analysis, domain models, and feature extraction.
2. **Service Layer (`apps/api/`)**: Lightweight FastAPI boundary exposing RESTful endpoints for engine capabilities.
3. **Client Layer (`apps/web/`)**: Next.js client interface communicating with the service layer.

```text
               ┌──────────────────────┐
               │   Next.js Frontend   │ (apps/web)
               └──────────┬───────────┘
                          │ HTTP / JSON
                          ▼
               ┌──────────────────────┐
               │     FastAPI API      │ (apps/api)
               └──────────┬───────────┘
                          │ Python import
                          ▼
               ┌──────────────────────┐
               │ Core Analysis Engine │ (engine/rightforge)
               └──────────────────────┘
```

## 2. Dependency Direction

Strict rules govern dependencies within the repository:

* **Engine Layer** must have **zero knowledge** of FastAPI, HTTP, or the frontend. It must never import from `apps.*`.
* **API Layer** acts as an adapter. It may import domain models and analyzers from `rightforge.*`, translate HTTP requests into engine invocations, and return JSON responses.
* **Web Layer** interacts strictly over HTTP network boundaries (REST).

## 3. Component Responsibilities

| Component | Path | Responsibility | Allowed Dependencies |
| :--- | :--- | :--- | :--- |
| **Domain Models** | `engine/rightforge/models/` | Base entities: `Document`, `MetricResult`, `AnalysisResult`, `AuthorProfile`, `MetricBaseline`, `MetricDeviation`, `ConsistencyReport`, `SemanticCoherenceReport`, `TransitionScore` | Pydantic, Python stdlib |
| **Text Processing** | `engine/rightforge/text/` | Deterministic segmentation, syllable estimation, function word dictionaries | Python stdlib, regex |
| **Analysis** | `engine/rightforge/analysis/` | Modular analyzers (`BaseAnalyzer`, `BasicTextAnalyzer`, `LexicalAnalyzer`, `SentenceAnalyzer`, `PunctuationAnalyzer`, `StylometryAnalyzer`, `SemanticCoherenceAnalyzer`, `LinguisticAnalyzer`) | `rightforge.models`, `rightforge.text` |
| **Profiles** | `engine/rightforge/profiles/` | Multi-document profile aggregation (`ProfileAggregator`) and alignment scoring (`ProfileComparator`) | `rightforge.models`, `rightforge.analysis` |
| **Core Utilities** | `engine/rightforge/core/` | Base classes, configuration primitives | Python stdlib |
| **API Application** | `apps/api/` | HTTP routing, request validation (`GET /health`, `POST /analysis/*`, `POST /profiles/*`) | FastAPI, Pydantic, `rightforge.*` |
| **Frontend Web** | `apps/web/` | Visual interface, interactive feedback | React, Next.js, TypeScript |

## 4. Active Architecture (Phase 6)

* `apps/api/main.py`:
  * `GET /health`: Service health verification.
  * `POST /analysis/basic`: Surface document statistics.
  * `POST /analysis/linguistic`: Lexical diversity, sentence rhythm, and punctuation metrics.
  * `POST /analysis/stylometry`: Stylometric invariants, vocabulary richness, and readability.
  * `POST /analysis/coherence`: Semantic flow, lexical chaining, and transition dynamics.
  * `POST /profiles/create`: Constructs multi-document `AuthorProfile` with metric baselines.
  * `POST /profiles/compare`: Evaluates a document against an `AuthorProfile`, returning deviation z-scores and composite consistency scores ($0.0 - 1.0$).
* `engine/rightforge/models/`:
  * `document.py`: `Document`, `MetricResult`, `AnalysisResult`.
  * `profile.py`: `AuthorProfile`, `MetricBaseline`.
  * `comparison.py`: `MetricDeviation`, `ConsistencyReport`.
  * `semantics.py`: `SemanticCoherenceReport`, `TransitionScore`.
* `engine/rightforge/analysis/`:
  * `semantics.py`: `SemanticCoherenceAnalyzer` measuring Jaccard segment transitions, overlap coefficients, and lexical chaining.
* `engine/rightforge/profiles/`: Aggregator and comparator engines.
* `engine/rightforge/text/`: Segmentation, syllables, and function words.

## 5. Future Target Architecture (Reference Only)

```text
                         RIGHTFORGE
                              │
               ┌──────────────┴──────────────┐
               │                             │
          Application                    Research
               │                             │
        ┌──────┴──────┐               ┌──────┴──────┐
        │             │               │             │
      Web UI         API          Experiments    Datasets
        │             │               │             │
        └──────┬──────┘               └──────┬──────┘
               │                             │
               └──────────────┬──────────────┘
                              │
                       Analysis Engine
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
      Text Analysis       Stylometry          Semantics
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                       Profile Engine
                              │
                              ▼
                     Author Representation
                              │
                              ▼
                    Evaluation / Comparison
                              │
                              ▼
                     Revision Engine
                              │
                              ▼
                         LLM Layer
                              │
              ┌───────────────┼───────────────┐
              │               │               │
            Local           Cloud          Future
             LLM             API          Providers
```
