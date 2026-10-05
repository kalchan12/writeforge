# RightForge Project Plan

## 1. Project Overview

RightForge is a local-first writing analysis and author-style research platform. It focuses on deterministic linguistic statistics, stylometric profiling, writing quality assessment, and responsible AI-assisted revision.

---

## 2. Completed Milestones

### Phase 0 — Foundation
- [x] **Repository Architecture**: Clean folder boundaries (`apps/`, `engine/rightforge/`, `tests/`, `docs/`, `scripts/`, `data/`).
- [x] **Python Packaging**: Configured `pyproject.toml` with Hatchling backend, Python 3.12+, and initial dependencies.
- [x] **Domain Models**: Base entities `Document`, `MetricResult`, `AnalysisResult`.
- [x] **API Boundary**: FastAPI service with `GET /health`.
- [x] **Web Application Skeleton**: Next.js + TypeScript application.
- [x] **Testing & CI**: Pytest suite and GitHub Actions workflow.
- [x] **Documentation System**: AI operating guidelines and contracts.

### Phase 1 — Basic Document Statistics
- [x] **Text Segmentation**: Deterministic sentences, paragraphs, and words.
- [x] **Basic Text Analyzer**: 10 surface metrics (`BasicTextAnalyzer`).
- [x] **API Endpoint**: `POST /analysis/basic`.
- [x] **Tests & Docs**: Deterministic tests and specification updates.

### Phase 2 — Linguistic Metrics
- [x] **Modular Analyzers**: `LexicalAnalyzer`, `SentenceAnalyzer`, `PunctuationAnalyzer`.
- [x] **Composite Pipeline**: `LinguisticAnalyzer` pipeline.
- [x] **API Endpoint**: `POST /analysis/linguistic`.
- [x] **Tests & Docs**: Deterministic coverage and documentation updates.

### Phase 3 — Stylometric Analysis
- [x] **Phonetic Syllables**: Deterministic `count_syllables()`.
- [x] **Function Words**: Curated closed-class lexicons.
- [x] **Stylometry Analyzer**: Vocabulary richness (Hapax/Dis legomena, Yule's K, Simpson's D), function word distributions, and readability indices (Flesch Reading Ease, Flesch-Kincaid Grade Level).
- [x] **API Endpoint**: `POST /analysis/stylometry`.
- [x] **Tests & Docs**: Deterministic tests and specification updates.

### Phase 4 — Writing Profiles
- [x] **Profile Domain Models**: `AuthorProfile` and `MetricBaseline` in `engine/rightforge/models/profile.py`.
- [x] **Profile Aggregation Engine**: `ProfileAggregator` in `engine/rightforge/profiles/aggregator.py`.
- [x] **API Endpoint**: `POST /profiles/create`.
- [x] **Tests & Docs**: Deterministic tests and specification updates.

### Phase 5 — Profile Comparison & Consistency Scoring
- [x] **Comparison Domain Models**: `MetricDeviation` and `ConsistencyReport` in `engine/rightforge/models/comparison.py`.
- [x] **Profile Comparator Engine**: `ProfileComparator` in `engine/rightforge/profiles/comparator.py`.
- [x] **API Endpoint**: `POST /profiles/compare`.
- [x] **Tests & Docs**: Deterministic tests and specification updates.

### Phase 6 — Semantic Similarity & Coherence
- [x] **Semantic Domain Models**: `SemanticCoherenceReport` and `TransitionScore` in `engine/rightforge/models/semantics.py`.
- [x] **Lexical Cohesion & Flow Engine**: `SemanticCoherenceAnalyzer` in `engine/rightforge/analysis/semantics.py`.
- [x] **API Endpoint**: `POST /analysis/coherence`.
- [x] **Tests & Docs**: Deterministic tests and specification updates.

### Phase 7 — Classical ML Experiments
- [x] **Feature Vectorizer**: Implemented `StylometricVectorizer` in `engine/rightforge/ml/vectorizer.py` extracting 31-dimensional normalized numerical feature arrays.
- [x] **ML Pipeline Integration**: Compatible with scikit-learn transformer interface (`fit`, `transform`, `fit_transform`).
- [x] **Evaluation Harness**: Created `scripts/evaluate_classifier.py` implementing Stratified K-Fold cross-validation across distinct style classes.
- [x] **Empirical Findings Logged**: Documented classification accuracy and top discriminative features (Gini importance) in `docs/research/EXPERIMENTS.md`.
- [x] **Deterministic Tests**: Added 4 unit tests verifying vector matrix shapes, zero-variance handling, and vector stability (**81 tests total, 100% passing**).
- [x] **Documentation**: Updated `docs/research/EXPERIMENTS.md` and `docs/ai/ARCHITECTURE.md`.

### Phase 8 — Transformer-Based Research (Perplexity & Burstiness Modeling)
- [x] **Perplexity Domain Models**: `SentencePerplexity` and `PerplexityReport` in `engine/rightforge/models/transformers.py`.
- [x] **Probability Model Abstraction**: `BaseProbabilityModel`, deterministic `NgramProbabilityModel` (Lidstone smoothed bigrams), and lazy-loaded `HuggingFaceProbabilityModel` in `engine/rightforge/ml/`.
- [x] **Perplexity & Burstiness Engine**: `PerplexityAnalyzer` in `engine/rightforge/analysis/perplexity.py` computing token logprobs, sentence perplexity, and burstiness ($CV = \sigma / \mu$).
- [x] **API Endpoint**: `POST /analysis/perplexity` returning `PerplexityReport`.
- [x] **Research Evaluation Harness**: `scripts/evaluate_perplexity.py` (EXP-002) evaluating perplexity and burstiness across synthetic, human narrative, and academic prose.
- [x] **Tests & Documentation**: Added unit and integration tests (**93 tests total, 100% passing**). Updated `docs/research/DETECTION.md`, `docs/ai/ARCHITECTURE.md`.

### Phase 9 — Controlled Revision Engine
- [x] **Revision Domain Models**: `RevisionGoal`, `SentenceRevisionTarget`, and `RevisionPlan` in `engine/rightforge/models/revision.py`.
- [x] **Revision Planning Engine**: `RevisionPlanner` in `engine/rightforge/revision/planner.py` analyzing consistency deviations and generating actionable sentence-level target interventions (excessive length, cadence monotony, repetitive openers, lexical redundancy).
- [x] **Dual-Mode Planning**: Supports both standalone quality heuristic mode and profile-guided alignment mode against reference `AuthorProfile`.
- [x] **API Endpoint**: `POST /revision/plan` returning `RevisionPlan`.
- [x] **Tests & Documentation**: Added unit and integration tests (**104 tests total, 100% passing**). Created `docs/specifications/REVISION.md` and updated `docs/ai/ARCHITECTURE.md`.

### Phase 10 — Local LLM Integration
- [x] **LLM Provider Abstraction**: `BaseLLMProvider` (ABC), `MockLLMProvider` (deterministic testing), and `OllamaProvider` (local HTTP daemon) in `engine/rightforge/llm/`.
- [x] **Prompt Engineering Engine**: `RevisionPromptBuilder` in `engine/rightforge/llm/prompts.py` enforcing strict style conditioning, factual preservation, and anti-hallucination guardrails.
- [x] **Revision Execution & Verification Pipeline**: `RevisionExecutor` in `engine/rightforge/revision/executor.py` running style-conditioned revision and computing pre- and post-revision metric snapshots (`RevisionExecutionResult`).
- [x] **API Endpoint**: `POST /revision/execute` returning `RevisionExecutionResult`.
- [x] **Tests & Documentation**: Added unit and integration tests (**116 tests total, 100% passing**). Created `docs/specifications/LLM_INTEGRATION.md` and updated `docs/ai/ARCHITECTURE.md`.

---

## 3. Current State

- **Active Phase**: Phase 10 Complete.
- **Engine**: Pure-Python analysis, profiling, comparison, ML vectorization, deterministic perplexity/burstiness, revision planning, and local LLM execution.
- **Tests**: 116 passed in pytest in ~2.8s.
- **Service**: 9 FastAPI endpoints operational.
- **Research**: EXP-001 (authorship classification) and EXP-002 (perplexity & burstiness) benchmark harnesses operational.

---

### Phase 11 — Web UI & Research Dashboard
- [x] **Typed API Client**: `apps/web/src/lib/api.ts` and `apps/web/src/types/api.ts` connecting all 9 backend FastAPI endpoints with strict TypeScript types.
- [x] **Interactive Dashboard Layout**: Next.js 14 tabbed application in `apps/web/src/app/page.tsx` with live backend status indicator and research presets.
- [x] **Metric Scorecards**: `MetricCard` components displaying surface statistics, cadence standard deviation, readability indices, and semantic flow continuity.
- [x] **Cadence & Perplexity Trajectory Chart**: Interactive SVG visualizer (`PerplexityGraph`) plotting per-sentence perplexity progression, burstiness coefficient ($CV$), and click-to-inspect sentence detail.
- [x] **Author Profile Workbench**: `ProfilePanel` allowing interactive author corpus profiling, baseline visualization, and consistency scoring.
- [x] **Controlled Revision Workbench**: `RevisionPanel` supporting diagnostic plan inspection, inference execution (Local Ollama vs Mock), side-by-side comparison, and metric shift verification.
- [x] **Production Build Verified**: `next build` passes with zero errors (`Static` pages generated, 0 lint or type errors).

---

## 3. Current State

- **Active Phase**: Phase 11 Complete.
- **Engine**: Pure-Python analysis, profiling, comparison, ML vectorization, deterministic perplexity/burstiness, revision planning, and local LLM execution.
- **Web UI**: Next.js 14 research dashboard operational and connecting to FastAPI backend.
- **Tests**: 116 passed in pytest in ~2.8s; Next.js production build passing.
- **Service**: 9 FastAPI endpoints operational.
- **Research**: EXP-001 (authorship classification) and EXP-002 (perplexity & burstiness) benchmark harnesses operational.

---

## 4. Known Limitations

- **No Native Desktop Packaging Yet**: Application runs via web browser and local terminal; native packaging (Tauri / SQLite local persistence) is scheduled for Phase 12.

---

## 5. Next Milestone: Phase 12 — Desktop Packaging & Production Hardening

The final bounded objective will package RightForge into a standalone application:
1. **Local SQLite Persistence**: SQLite database schema for persistent local document history, custom author profiles, and revision audit logs.
2. **Offline Bundling & Launcher**: Single-binary or launcher workflow for zero-configuration desktop operation.
3. **End-to-End Hardening**: Final performance audits, memory profiling, and release verification.
