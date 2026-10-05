# Design Principles & Conventions

## 1. Core Design Principles

1. **Determinism First**: Text analysis metrics should produce consistent and reproducible outputs given identical input text.
2. **Composability**: Analyzers should be small, single-purpose classes or functions that can be chained or executed independently.
3. **Explicit Data Contracts**: All data structures crossing boundaries must be modeled using strict Pydantic schemas.
4. **Separation of Presentation and Computation**: The calculation of a metric must never be coupled to how it is rendered in an API or UI.

## 2. API Conventions

* **RESTful JSON**: All API communication occurs over standard HTTP using JSON payloads.
* **Health Endpoint**: Always accessible at `GET /health` with `status: "healthy"`.
* **Path Naming**: Lowercase, kebab-case or resource-oriented paths (e.g., `/analysis/basic`, `/analysis/linguistic`).
* **Request Validation**: Use Pydantic models for all request bodies. Reject malformed payloads with 422 Unprocessable Entity.
* **Standard Error Responses**: Return informative JSON error payloads with `{"detail": "..."}` or structured validation errors.

## 3. Domain Model Conventions

* Models reside in `engine/rightforge/models/`.
* Base models inherit from `pydantic.BaseModel`.
* Use explicit type annotations for all attributes (`str`, `int`, `float`, `list[str]`, etc.).
* Dates and timestamps must always be timezone-aware (preferably UTC via `datetime.now(timezone.utc)`).
* Avoid deeply nested mutable hierarchies where simple flat dictionaries or records suffice.

## 4. UI Principles

* Minimal, focused, and responsive.
* Avoid cluttering the interface with speculative controls.
* Clear visual distinction between measured facts (deterministic statistics) and probabilistic estimates (future models).

## 5. Error Handling

* Fail early on invalid input types or unparseable formats.
* Do not suppress exceptions silently; capture and provide diagnostic messaging.
* The engine should raise custom Python exceptions derived from a base `RightForgeError`, allowing API layers to translate them into appropriate HTTP status codes.

## 6. Naming Conventions

* **Python Modules & Packages**: `snake_case` (e.g., `document.py`, `rightforge`).
* **Python Classes**: `PascalCase` (e.g., `Document`, `AnalysisResult`, `LexicalAnalyzer`).
* **Python Functions & Variables**: `snake_case` (e.g., `calculate_metrics()`).
* **TypeScript Files & Components**: `PascalCase.tsx` for React components, `camelCase.ts` for utilities.
