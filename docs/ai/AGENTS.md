# RightForge Agent Guidelines

Welcome to **RightForge**. This document is the primary instruction file that every AI coding agent must read before inspecting, modifying, or creating code in this repository.

---

## 1. Project Identity

* **Project Name**: RightForge
* **Mission**: A local-first writing analysis and author-style research platform.
* **Long-Term Vision**: Linguistic analysis, stylometry, author writing-profile modeling, writing-quality analysis, semantic preservation, and controlled AI-assisted revision.
* **Current Status**: **Phase 0 — Foundation**. Only base project layout, documentation contracts, base domain models (`Document`, `MetricResult`, `AnalysisResult`), minimal API health check, and minimal web shell are active.

---

## 2. Core Development Philosophy

Every agent working on RightForge must strictly adhere to these principles:

1. **Build small, composable capabilities** before complex systems.
2. **Prefer explicit code** over premature abstractions.
3. **Do not implement speculative features**.
4. **Do not create unnecessary services or infrastructure**.
5. **Keep the core analysis engine independent from the UI and API**.
6. **Keep research/ML code separate** from application infrastructure.
7. **Make every major component independently testable**.
8. **Favor local-first operation**; protect user privacy and avoid telemetry.
9. **Avoid unnecessary external APIs**.
10. **Preserve algorithm and model swappability**.
11. **Every architectural decision must be recorded** in `docs/ai/DECISIONS.md`.
12. **Never silently alter project architecture**.
13. **Never add dependencies without a clear, documented rationale**.
14. **Do not create placeholder implementations** that pretend to work.
15. **If something is deferred, document it** rather than implementing a fake version.

---

## 3. Scope & Research Boundary

RightForge is a research and writing-analysis platform.

* **Strict Boundary**: It must **NOT** be designed around bypassing academic-integrity systems, defeating commercial AI detectors, or guaranteeing that text will evade detection.
* **Positive Focus**: The platform focuses on:
  * Linguistic characterization and metric measurement.
  * Stylometry and authorial consistency modeling.
  * Semantic preservation and writing quality.
  * Responsible AI-assisted revision.
  * Empirical evaluation of AI-writing detection systems as external reference benchmarks.

---

## 4. The RightForge Agent Development Loop

When assigned any task or prompt, follow this 11-step execution loop:

```text
1. READ
   Read project documentation (AGENTS.md, CONTEXT.md, ARCHITECTURE.md, PLAN.md).

2. INSPECT
   Inspect current repository state, existing modules, and tests.

3. SCOPE
   Isolate exactly what this specific milestone requires. Reject scope creep.

4. PLAN
   Formulate a concise, bounded plan before editing files.

5. IMPLEMENT
   Implement only the requested capability with minimal complexity.

6. TEST
   Add deterministic tests verifying true behavior and edge cases.

7. REVIEW
   Check architecture boundaries, security, and potential regressions.

8. DOCUMENT
   Update relevant specifications, architecture notes, and PLAN.md.

9. VERIFY
   Run the test suite and confirm operational health.

10. REPORT
    Summarize completed work, files changed, and active limitations.

11. STOP
    Do not automatically proceed into future milestones.
```

---

## 5. Technology Standards

* **Engine**: Python 3.12+, pure Python text analysis, modular analyzers.
* **API**: FastAPI, Pydantic v2, Uvicorn. Keep endpoints thin and decoupled from engine logic.
* **Frontend**: Next.js (App Router), TypeScript, responsive minimal styling.
* **Testing**: `pytest`, deterministic unit and integration tests.
* **Database**: Local SQLite (deferred until persistence milestone).
* **Research**: Dedicated `docs/research/` specifications, duckdb/pandas only when justified.
