# Project Context

## 1. Project Purpose

RightForge is a local-first writing analysis and author-style research platform. It aims to empower writers, researchers, and editors with deep, transparent linguistic insights, stylistic fingerprinting, and controlled writing revision without sacrificing privacy or relying on centralized third-party servers.

## 2. Current Development Stage

* **Active Stage**: **Phase 0 — Foundation**
* **Active Components**:
  * Repository and workspace configuration (`pyproject.toml`, `.gitignore`, GitHub Actions CI).
  * Documentation contracts and AI operating guidelines (`docs/ai/`, `docs/research/`, `docs/specifications/`).
  * Core domain entities: `Document`, `MetricResult`, `AnalysisResult` in `engine/rightforge/models/`.
  * FastAPI application skeleton with operational verification at `GET /health` (`apps/api/`).
  * Next.js TypeScript frontend skeleton (`apps/web/`).

## 3. Current Capabilities

* Instantiating and validating `Document` text objects with metadata and UTC timestamps.
* Constructing and attaching `MetricResult` records to an `AnalysisResult` container.
* Verifying API service vitality via `GET /health`.
* Validating frontend shell structure and type correctness.

## 4. Explicitly Deferred Capabilities

The following capabilities are deliberately **not** implemented in this phase:

* Perplexity calculation and token probability distributions.
* Machine learning / deep learning inference (PyTorch, Hugging Face).
* AI writing detection or detector-evasion pipelines.
* Spacy or specialized NLP pipelines (until needed by specific linguistic metrics).
* Automated text rewriting or paraphrasing.
* Author profiling algorithms and similarity matrices.
* Vector embeddings and semantic search.
* Local LLM orchestration (Ollama, llama.cpp).
* Persistent database storage (SQLite / DuckDB).
* Tauri desktop packaging.

## 5. Technology Direction

* **Backend**: Python 3.12+, FastAPI, Pydantic v2, Uvicorn, pytest.
* **Text Analysis Engine**: Pure Python initially, standard library text handling, composable analyzers.
* **Frontend**: Next.js (App Router), React 18, TypeScript.
* **Persistence**: Local SQLite when storage becomes active.
* **Tooling**: `uv` package manager.

## 6. Important Constraints

1. **Local-First**: All core analysis must run entirely on the user's workstation without requiring cloud infrastructure.
2. **Deterministic Foundations**: Foundational metrics must produce identical results across operating systems for identical inputs.
3. **Decoupled Architecture**: The core analysis engine (`engine/rightforge`) must never import or depend upon FastAPI or web presentation code.
