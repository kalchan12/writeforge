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
- [x] **Lexical Cohesion & Flow Engine**: Implemented `SemanticCoherenceAnalyzer` in `engine/rightforge/analysis/semantics.py`:
  - Segment-by-segment content word extraction (excluding function words).
  - Jaccard similarity and overlap coefficients for adjacent sentences and paragraphs.
  - Document-wide lexical chaining tracking content word repetition rates across paragraphs.
  - Abrupt transition / topic shift identification.
- [x] **API Endpoint**: Exposed `POST /analysis/coherence`.
- [x] **Deterministic Tests**: Added 8 unit and integration tests (**77 tests total, 100% passing**).
- [x] **Documentation**: Updated `docs/specifications/ANALYZER.md` and `docs/ai/ARCHITECTURE.md`.

---

## 3. Current State

- **Active Phase**: Phase 6 Complete.
- **Engine**: Pure-Python analysis, profiling, comparison, and semantic flow measurement.
- **Tests**: 77 passed in pytest in ~1.7s.
- **Service**: FastAPI server exposing:
  - `GET /health`
  - `POST /analysis/basic`
  - `POST /analysis/linguistic`
  - `POST /analysis/stylometry`
  - `POST /analysis/coherence`
  - `POST /profiles/create`
  - `POST /profiles/compare`

---

## 4. Known Limitations

- **No Classical ML Pipelines Yet**: Stylometric and coherence metrics are extracted deterministically; vectorization pipelines and supervised authorship/style classifiers are scheduled for Phase 7.
- **No Persistence**: Storage remains in-memory.
- **No Heavy Deep Learning**: Explicitly deferred to Phase 8 (Transformer-Based Research).

---

## 5. Next Milestone: Phase 7 — Classical ML Experiments

The next bounded objective will implement classical machine learning feature extraction and classification baselines:
1. **Feature Vectorizer**: `StylometricVectorizer` in `engine/rightforge/ml/vectorizer.py` extracting normalized numerical feature arrays from documents.
2. **Evaluation Harness**: Experiment runner script in `scripts/evaluate_classifier.py` using scikit-learn (RandomForest / LogisticRegression / SVM) to classify sample authorship corpora.
3. **Research Notes**: Document empirical results and feature importance rankings in `docs/research/EXPERIMENTS.md`.
4. **Deterministic Tests**: Verifying vectorizer dimension consistency, zero-variance handling, and model reproducibility.
