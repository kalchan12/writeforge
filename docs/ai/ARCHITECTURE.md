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
| **Domain Models** | `engine/rightforge/models/` | Base entities: `Document`, `MetricResult`, `AnalysisResult` | Pydantic, Python stdlib |
| **Text Processing** | `engine/rightforge/text/` | Tokenization, sentence splitting, normalization | Python stdlib, regex (later spaCy) |
| **Analysis** | `engine/rightforge/analysis/` | Modular analyzers (lexical, sentence, punctuation) | `rightforge.models`, `rightforge.text` |
| **Core Utilities** | `engine/rightforge/core/` | Base classes, configuration primitives | Python stdlib |
| **API Application** | `apps/api/` | HTTP routing, request validation, error formatting | FastAPI, Pydantic, `rightforge.*` |
| **Frontend Web** | `apps/web/` | Visual interface, interactive feedback | React, Next.js, TypeScript |

## 4. Current Phase 0 Architecture

In Phase 0, the architecture is intentionally minimal:
* `apps/api/main.py`: Exposes `GET /health` with structured status.
* `engine/rightforge/models/document.py`: Defines immutable and validated base models (`Document`, `MetricResult`, `AnalysisResult`).
* `apps/web/`: Single-page health check verification shell.

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

Note: Future architecture nodes are not active in Phase 0.
