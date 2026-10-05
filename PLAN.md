# RightForge Project Plan

## 1. Project Overview

RightForge is a local-first writing analysis and author-style research platform. It focuses on deterministic linguistic statistics, stylometric profiling, writing quality assessment, and responsible AI-assisted revision.

---

## 2. Completed Work (Phase 0 — Foundation)

- [x] **Repository Architecture**: Established clean folder boundaries (`apps/`, `engine/rightforge/`, `tests/`, `docs/`, `scripts/`, `data/`).
- [x] **Python Packaging**: Configured `pyproject.toml` with Hatchling build backend, Python 3.12+ requirement, and strict dependencies (`fastapi`, `uvicorn`, `pydantic`).
- [x] **Domain Models**: Implemented lightweight, validated domain models in `engine/rightforge/models/document.py` (`Document`, `MetricResult`, `AnalysisResult`).
- [x] **API Boundary**: Built FastAPI service entrypoint in `apps/api/main.py` with structured `GET /health` endpoint.
- [x] **Web Application Skeleton**: Created Next.js + TypeScript application in `apps/web/` with automated health status connectivity.
- [x] **Testing Suite**: Configured pytest suite with 100% deterministic unit and integration tests (`tests/unit/`, `tests/integration/`).
- [x] **Documentation System**: Created comprehensive AI operating guidelines and architectural contracts:
  - `docs/ai/AGENTS.md`
  - `docs/ai/CONTEXT.md`
  - `docs/ai/ARCHITECTURE.md`
  - `docs/ai/DESIGN.md`
  - `docs/ai/SECURITY.md`
  - `docs/ai/DEVELOPMENT.md`
  - `docs/ai/TESTING.md`
  - `docs/ai/ROADMAP.md`
  - `docs/ai/DECISIONS.md`
  - `docs/research/DETECTION.md`
  - `docs/research/STYLOMETRY.md`
  - `docs/research/METRICS.md`
  - `docs/research/EXPERIMENTS.md`
  - `docs/specifications/ANALYZER.md`
- [x] **Continuous Integration**: Configured GitHub Actions CI pipeline in `.github/workflows/ci.yml`.

---

## 3. Current State

- **Active Phase**: Phase 0 Complete.
- **Engine**: Pure Python core package `rightforge` installed in editable mode; all tests passing (8 passed).
- **Service**: FastAPI server ready to run on port 8000.
- **Client**: Web frontend initialized in `apps/web`.

---

## 4. Known Limitations

- **No Analysis Metrics Yet**: `engine/rightforge/analysis/` only defines module boundaries; metric extraction is deferred to Phase 1.
- **No Persistence**: SQLite database not yet introduced; all models are in-memory.
- **No Machine Learning / LLMs**: Explicitly deferred by architectural contract until metric foundations are complete.

---

## 5. Next Milestone: Phase 1 — Basic Document Statistics

The next bounded objective will implement basic deterministic document statistics:
1. Character count (total and non-whitespace)
2. Word count
3. Sentence count
4. Paragraph count
5. Sentence length statistics (mean, min, max, standard deviation)
6. Dedicated POST `/analysis/basic` endpoint in `apps/api`
7. Comprehensive deterministic test suite for all edge cases
