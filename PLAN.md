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
- [x] **Profile Domain Models**: `AuthorProfile` and `MetricBaseline` in `engine/rightforge/models/profile.py` supporting empirical distribution statistics, z-score calculations, and deviation boundary evaluations.
- [x] **Profile Aggregation Engine**: Implemented `ProfileAggregator` in `engine/rightforge/profiles/aggregator.py` executing multi-tier analysis across document corpora and computing exact statistical baselines.
- [x] **API Endpoint**: Exposed `POST /profiles/create` in `apps/api/main.py`.
- [x] **Deterministic Tests**: Added 9 new unit and integration tests (**65 tests total, 100% passing**).
- [x] **Documentation**: Created `docs/specifications/WRITING_PROFILE.md` and updated `docs/ai/ARCHITECTURE.md`.

---

## 3. Current State

- **Active Phase**: Phase 4 Complete.
- **Engine**: Pure-Python analysis and author profile aggregation.
- **Tests**: 65 passed in pytest in ~1.5s.
- **Service**: FastAPI server exposing `GET /health`, `POST /analysis/basic`, `POST /analysis/linguistic`, `POST /analysis/stylometry`, and `POST /profiles/create`.

---

## 4. Known Limitations

- **No Document-to-Profile Comparison Yet**: Profiles can be generated, but automated comparative scoring (evaluating a new draft against an existing profile and generating consistency scores) is scheduled for Phase 5.
- **No Persistence**: Profiles and documents remain in-memory; local SQLite storage will be introduced in later phases.
- **No Machine Learning / LLMs**: Explicitly deferred by architectural contract until metric foundations are complete.

---

## 5. Next Milestone: Phase 5 — Profile Comparison & Consistency Scoring

The next bounded objective will implement document-to-profile comparison:
1. **Comparison Domain Model**: Define `ComparisonResult`, `MetricDeviation`, and `ConsistencyReport` in `engine/rightforge/models/comparison.py`.
2. **Profile Comparator Engine**: Implement `ProfileComparator` in `engine/rightforge/profiles/comparator.py`:
   - Compute individual metric z-scores and deviation flags.
   - Calculate aggregated consistency score ($0.0 - 1.0$) using weighted composite metric distance.
   - Identify significant stylistic outliers (e.g. abrupt shifts in function word usage or sentence cadence).
3. **API Endpoint**: `POST /profiles/compare` (evaluates a document against a target profile).
4. **Deterministic Tests**: Verification of exact deviation scores, boundary flags, and consistency ratings.
