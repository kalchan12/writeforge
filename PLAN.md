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
- [x] **Profile Comparator Engine**: `ProfileComparator` in `engine/rightforge/profiles/comparator.py`:
  - Normalized Gaussian-decay fidelity scoring: $s_i = \exp\left(-\frac{1}{2} \left(\frac{|z_i|}{2.0}\right)^2\right)$.
  - Bounded composite consistency score in $[0.0, 1.0]$.
  - Automatic outlier detection ($|z| > \text{threshold}$).
  - Qualitative alignment assessment (high, moderate, low, divergent).
- [x] **API Endpoint**: `POST /profiles/compare`.
- [x] **Deterministic Tests**: Added 4 unit and integration tests (**69 tests total, 100% passing**).
- [x] **Documentation**: Updated `docs/specifications/WRITING_PROFILE.md` and `docs/ai/ARCHITECTURE.md`.

---

## 3. Current State

- **Active Phase**: Phase 5 Complete.
- **Engine**: Pure-Python analysis, profile creation, and automated style consistency comparison.
- **Tests**: 69 passed in pytest in ~1.6s.
- **Service**: FastAPI server exposing:
  - `GET /health`
  - `POST /analysis/basic`
  - `POST /analysis/linguistic`
  - `POST /analysis/stylometry`
  - `POST /profiles/create`
  - `POST /profiles/compare`

---

## 4. Known Limitations

- **No Semantic Flow Analysis Yet**: Style and surface invariants are modeled, but semantic topic cohesion, sentence-to-sentence transition flow, and lexical chaining are scheduled for Phase 6.
- **No Persistence**: Storage remains in-memory; SQLite persistence scheduled for full application phase.
- **No Machine Learning / LLMs**: Explicitly deferred by architectural contract until metric and semantic foundations are complete.

---

## 5. Next Milestone: Phase 6 — Semantic Similarity & Coherence

The next bounded objective will implement semantic and coherence analysis:
1. **Semantic Models**: `SemanticCoherenceReport`, `TransitionScore` in `engine/rightforge/models/semantics.py`.
2. **Lexical Cohesion & Flow Engine**: `SemanticCoherenceAnalyzer` in `engine/rightforge/analysis/semantics.py`:
   - Paragraph-to-paragraph and sentence-to-sentence lexical overlap (Jaccard and Dice similarity of content words).
   - Lexical chaining and noun phrase repetition tracking.
   - Transition smoothness scoring.
3. **API Endpoint**: `POST /analysis/coherence`.
4. **Deterministic Tests**: Verifying flow scores across coherent vs. disjointed texts.
