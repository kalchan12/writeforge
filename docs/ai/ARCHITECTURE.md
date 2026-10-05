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
* **Research / ML Layer** consumes the engine as a library without introducing ML coupling into the core engine models or API runtime.

## 3. Component Responsibilities

| Component | Path | Responsibility | Allowed Dependencies |
| :--- | :--- | :--- | :--- |
| **Domain Models** | `engine/rightforge/models/` | Base entities: `Document`, `MetricResult`, `AnalysisResult`, `AuthorProfile`, `MetricBaseline`, `MetricDeviation`, `ConsistencyReport`, `SemanticCoherenceReport`, `TransitionScore` | Pydantic, Python stdlib |
| **Text Processing** | `engine/rightforge/text/` | Deterministic segmentation, syllable estimation, function word dictionaries | Python stdlib, regex |
| **Analysis** | `engine/rightforge/analysis/` | Modular analyzers (`BaseAnalyzer`, `BasicTextAnalyzer`, `LexicalAnalyzer`, `SentenceAnalyzer`, `PunctuationAnalyzer`, `StylometryAnalyzer`, `SemanticCoherenceAnalyzer`, `LinguisticAnalyzer`) | `rightforge.models`, `rightforge.text` |
| **Profiles** | `engine/rightforge/profiles/` | Multi-document profile aggregation (`ProfileAggregator`) and alignment scoring (`ProfileComparator`) | `rightforge.models`, `rightforge.analysis` |
| **ML & Vectorization** | `engine/rightforge/ml/` | Stylometric feature extraction (`StylometricVectorizer`) | `rightforge.analysis`, `numpy` (optional) |
| **Storage & Persistence** | `engine/rightforge/storage/` | SQLite persistence with WAL mode (`DatabaseManager`) for documents, profiles, and audit logs | `sqlite3`, Python stdlib |
| **Research Scripts** | `scripts/` | Benchmark harnesses, model training, validation experiments, desktop launcher | `rightforge.*`, `scikit-learn`, `numpy` |
| **Core Utilities** | `engine/rightforge/core/` | Base classes, configuration primitives | Python stdlib |
| **API Application** | `apps/api/` | HTTP routing, request validation (`GET /health`, `POST /analysis/*`, `POST /profiles/*`, `GET /profiles`, `POST /revision/*`, `GET /revision/logs`) | FastAPI, Pydantic, `rightforge.*` |
| **Frontend Web** | `apps/web/` | Visual interface, interactive feedback | React, Next.js, TypeScript |

## 4. Completed Architecture (Phases 0–12)

* `engine/rightforge/storage/`:
  * `db.py`: `DatabaseManager` providing SQLite persistence with WAL mode, non-blocking concurrent connections, and ACID transactions for `documents`, `author_profiles`, and `revision_logs`.
* `engine/rightforge/ml/`:
  * `probability.py`: `BaseProbabilityModel` (ABC) and deterministic `NgramProbabilityModel` with Lidstone smoothing.
  * `hf_model.py`: Optional lazy-loaded `HuggingFaceProbabilityModel` for local transformer weights.
  * `vectorizer.py`: `StylometricVectorizer` extracting 31-dimensional normalized numerical feature vectors compatible with scikit-learn transformers.
* `engine/rightforge/analysis/`:
  * `perplexity.py`: `PerplexityAnalyzer` computing sentence perplexity trajectories and burstiness ($CV = \sigma / \mu$).
  * Modular deterministic text analyzers: basic, lexical, sentence, punctuation, stylometry, semantics, and perplexity.
* `engine/rightforge/llm/`:
  * `base.py`: `BaseLLMProvider` (ABC) and `MockLLMProvider` for deterministic testing.
  * `ollama.py`: `OllamaProvider` connecting to local inference daemons over HTTP.
  * `prompts.py`: `RevisionPromptBuilder` formatting style-conditioned prompts and anti-hallucination guardrails.
* `engine/rightforge/revision/`:
  * `planner.py`: `RevisionPlanner` formulating rule-governed revision goals and granular sentence interventions (`RevisionPlan`).
  * `executor.py`: `RevisionExecutor` executing style-conditioned LLM revisions and conducting pre/post metric verification (`RevisionExecutionResult`).
* `scripts/`:
  * `desktop_launcher.py`: Standalone offline desktop launcher orchestrating concurrent API + Web services, port verification, readiness probing, browser dispatch, and graceful shutdown.
  * `evaluate_perplexity.py`: Perplexity and burstiness evaluation across diverse and synthetic text genres (EXP-002).
  * `evaluate_classifier.py`: Cross-validation classification harness testing stylistic discrimination (EXP-001).
* `apps/api/main.py`: RESTful endpoints for basic, linguistic, stylometric, coherence, perplexity, and revision planning/execution, alongside profile creation, listing, retrieval, and revision audit logs.
* `apps/web/`:
  * `src/lib/api.ts`: Typed API client connecting to FastAPI backend endpoints.
  * `src/components/`: Interactive components (`MetricCard`, `PerplexityGraph`, `ProfilePanel`, `RevisionPanel`).
  * `src/app/page.tsx`: Tabbed research dashboard unifying metric analysis, perplexity trajectory charting, author profile management, and controlled revision execution.

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
