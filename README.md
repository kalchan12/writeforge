# RightForge

RightForge is a local-first writing analysis and author-style research platform.

## Overview

RightForge is designed to explore linguistic patterns, stylometry, author consistency, and writing characteristics without compromising author privacy or relying on black-box external services.

> **Research & Integrity Boundary**: RightForge is a research and writing-analysis platform. It is **not** designed to bypass academic-integrity systems, defeat commercial AI detectors, or guarantee evasion. Instead, it provides rigorous linguistic analysis, writing quality insights, stylometric characterization, and responsible evaluation.

## Current Stage

**Phase 0 — Foundation**: The repository establishes the core project structure, documentation architecture, base domain models (`Document`, `MetricResult`, `AnalysisResult`), minimal FastAPI service with health verification, and minimal Next.js frontend skeleton.

See [PLAN.md](file:///home/kal/writeforge/PLAN.md) and [docs/ai/AGENTS.md](file:///home/kal/writeforge/docs/ai/AGENTS.md) for detailed architectural blueprints.

## Repository Layout

```text
rightforge/
├── apps/
│   ├── api/             # FastAPI application service
│   └── web/             # Next.js web application
├── engine/
│   └── rightforge/      # Core analysis engine (pure Python)
│       ├── analysis/    # Composable analyzers
│       ├── core/        # Common utilities & abstractions
│       ├── models/      # Domain models (Document, AnalysisResult, MetricResult)
│       └── text/        # Text processing primitives
├── tests/
│   ├── unit/            # Deterministic unit tests
│   ├── integration/     # Service and endpoint integration tests
│   └── fixtures/        # Test text fixtures
├── docs/
│   ├── ai/              # AI operating system & development guides
│   ├── research/        # Research methodologies & notes
│   └── specifications/  # Technical specifications for engine modules
├── scripts/             # Development and evaluation scripts
└── data/                # Local data storage (raw, processed, samples)
```

## Quickstart

### Backend & Core Engine

Prerequisites: Python 3.12+ and `uv` (or `venv` / `pip`).

```bash
# Setup virtual environment and install dependencies
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Run tests
pytest

# Start development API server
uvicorn apps.api.main:app --reload --port 8000
```

Verify health:
```bash
curl http://localhost:8000/health
```

### Frontend

Prerequisites: Node.js 20+ and `npm`.

```bash
cd apps/web
npm install
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000).

## License

MIT License. See [LICENSE](file:///home/kal/writeforge/LICENSE).
