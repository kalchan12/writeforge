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

---

## 3. Current State

- **Active Phase**: Phase 8 Complete.
- **Engine**: Pure-Python analysis, profiling, comparison, ML vectorization, and deterministic perplexity/burstiness modeling.
- **Tests**: 93 passed in pytest in ~2.3s.
- **Service**: 7 FastAPI endpoints operational.
- **Research**: EXP-001 (authorship classification) and EXP-002 (perplexity & burstiness) benchmark harnesses operational.

---

## 4. Known Limitations

- **No Revision Suggestion Engine Yet**: Targeted transformation suggestions based on stylometric deviations are scheduled for Phase 9.
- **No LLM Integration Yet**: Scheduled for Phase 10.
- **No Persistence**: Storage remains in-memory.

---

## 5. Next Milestone: Phase 9 — Controlled Revision Engine

The next bounded objective will implement targeted stylistic revision planning:
1. **Revision Domain Models**: `RevisionGoal`, `RevisionPlan`, `SentenceRevisionTarget` in `engine/rightforge/models/revision.py`.
2. **Revision Planning Engine**: `RevisionPlanner` in `engine/rightforge/revision/planner.py` analyzing consistency deviations and generating actionable sentence-level target interventions (e.g., cadence adjustments, lexical diversity enhancement, passive voice modulation).
3. **API Endpoint**: `POST /revision/plan` accepting an `AuthorProfile` and target `Document`.
4. **Deterministic Tests & Documentation**: Unit and integration test coverage.
