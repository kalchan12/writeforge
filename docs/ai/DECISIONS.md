# Architecture Decision Records (ADR)

This document tracks all significant architectural, design, and structural decisions made in RightForge.

---

## ADR-001: Local-First Architecture

* **Status**: Accepted
* **Date**: Phase 0
* **Context**: RightForge analyzes private, academic, and creative drafts. Sending user text to external cloud services or telemetry collectors risks intellectual property and confidentiality breaches.
* **Decision**: All core analysis, data storage, and future machine learning models run locally on the user's workstation by default.
* **Consequences**:
  * *Advantages*: Absolute user privacy, offline capabilities, zero cloud infrastructure cost, verifiable reproducibility.
  * *Trade-offs*: Dependent on local workstation hardware resources for heavier future computations.

---

## ADR-002: Python 3.12+ for Core Engine

* **Status**: Accepted
* **Date**: Phase 0
* **Context**: Text processing, linguistic analytics, and future machine learning tooling are richest and most mature in the Python ecosystem.
* **Decision**: The core analysis engine (`engine/rightforge`) is built in pure Python 3.12+ using standard library primitives and Pydantic.
* **Consequences**:
  * *Advantages*: Direct access to scientific, NLP, and ML libraries; strong typing via modern type annotations.
  * *Trade-offs*: Requires Python runtime on host.

---

## ADR-003: FastAPI for Service Boundary

* **Status**: Accepted
* **Date**: Phase 0
* **Context**: The engine needs an interface to communicate with web frontends and potential external scripts or desktop shells.
* **Decision**: Expose services through a lightweight FastAPI application located in `apps/api`.
* **Consequences**:
  * *Advantages*: Automatic OpenAPI documentation, high performance with async support, native Pydantic validation.
  * *Trade-offs*: Engine must remain strictly decoupled from FastAPI to allow standalone Python usage.

---

## ADR-004: Next.js + TypeScript for Web Interface

* **Status**: Accepted
* **Date**: Phase 0
* **Context**: A modern, responsive user interface is needed for document inspection and interaction.
* **Decision**: Use Next.js (App Router) with TypeScript in `apps/web`.
* **Consequences**:
  * *Advantages*: Type safety, modern component ecosystem, straightforward future desktop embedding via Tauri/webview.
  * *Trade-offs*: Requires Node.js development toolchain alongside Python.

---

## ADR-005: Minimal Initial Domain Modeling

* **Status**: Accepted
* **Date**: Phase 0
* **Context**: Starting with premature abstractions for profiles, rewriting, or embeddings creates technical debt.
* **Decision**: Phase 0 only defines `Document`, `MetricResult`, and `AnalysisResult`.
* **Consequences**:
  * *Advantages*: Clean, minimal foundation that is 100% verified and extensible.
  * *Trade-offs*: Further domain models must be introduced incrementally in corresponding roadmap phases.
