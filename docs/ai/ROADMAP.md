# RightForge Development Roadmap

The development of RightForge proceeds in strictly bounded, incremental phases. Only the currently designated active phase may be worked on.

---

### Phase 0 — Foundation [CURRENT ACTIVE PHASE]
* **Objective**: Establish clean, maintainable, research-oriented foundation and AI operating contracts.
* **Deliverables**:
  * Repository structure (`apps/`, `engine/`, `tests/`, `docs/`, `data/`).
  * Python packaging with `pyproject.toml` and Hatchling backend.
  * Core domain entities: `Document`, `MetricResult`, `AnalysisResult`.
  * Minimal FastAPI service with `GET /health`.
  * Minimal Next.js web application skeleton.
  * Comprehensive AI documentation system (`docs/ai/`, `docs/research/`, `docs/specifications/`).
  * Automated testing configuration with deterministic unit and integration tests.
  * GitHub Actions CI workflow.

---

### Phase 1 — Text Representation & Basic Statistics [UPCOMING]
* **Objective**: Implement deterministic document tokenization and elementary statistics.
* **Scope**: Character count, word count, sentence count, paragraph count, sentence-length distribution (mean, min, max, standard deviation).
* **Boundary**: No ML, no spaCy, no AI detection, no LLM integration.

---

### Phase 2 — Linguistic Metrics
* **Objective**: Expand deterministic text analyzer with modular linguistic analyzers.
* **Scope**:
  * Lexical: unique word count, type-token ratio (TTR), long-word ratio.
  * Sentence structure: length variance, distribution percentiles.
  * Punctuation: punctuation mark frequencies and density.
* **Boundary**: Standard library or lightweight tokenization only.

---

### Phase 3 — Stylometric Analysis
* **Objective**: Authorial fingerprinting and stylometry metrics.
* **Scope**: Function word frequencies, Yule's K characteristic, readability indexes, syntactic markers.

---

### Phase 4 — Writing Profiles
* **Objective**: Aggregating multiple analyzed documents into persistent author writing profiles.
* **Scope**: Author profile schema, baseline metric ranges, variance modeling.

---

### Phase 5 — Profile Comparison & Semantic Analysis
* **Objective**: Measuring document consistency against author profiles and analyzing semantic coherence.
* **Scope**: Stylometric distance metrics, consistency scoring (0.0 - 1.0).

---

### Phase 6 — Classical ML Research
* **Objective**: Feature vector extraction and classical machine learning classification benchmarks.
* **Scope**: Scikit-learn pipelines, cross-validation, baseline evaluations on benchmark corpora.

---

### Phase 7 — Controlled Revision Engine
* **Objective**: Rule-based and metric-guided recommendations for revising text toward target style profiles.
* **Scope**: Targeted suggestions, sentence-level feedback, readability adjustments.

---

### Phase 8 — Local LLM Integration
* **Objective**: Pluggable provider abstraction for local inference (e.g., Ollama).
* **Scope**: Structured style-guided revision prompts, local-only execution.

---

### Phase 9 — Research Benchmarking Suite
* **Objective**: Systematic empirical evaluation and benchmark comparison against detection research baselines.
* **Scope**: Benchmark datasets, evaluation runners, automated metric reporting.

---

### Phase 10 — Desktop Packaging & Production Hardening
* **Objective**: Native cross-platform desktop application.
* **Scope**: Tauri packaging, local SQLite persistence, offline bundling.
