# RightForge Project Plan

## 1. Project Overview

RightForge is a local-first writing analysis and author-style research platform. It focuses on deterministic linguistic statistics, stylometric profiling, writing quality assessment, and responsible AI-assisted revision.

---

## 2. Completed Milestones

### Phase 0 — Foundation
- [x] **Repository Architecture**: Established clean folder boundaries (`apps/`, `engine/rightforge/`, `tests/`, `docs/`, `scripts/`, `data/`).
- [x] **Python Packaging**: Configured `pyproject.toml` with Hatchling build backend, Python 3.12+ requirement, and strict dependencies (`fastapi`, `uvicorn`, `pydantic`).
- [x] **Domain Models**: Implemented lightweight, validated domain models in `engine/rightforge/models/document.py` (`Document`, `MetricResult`, `AnalysisResult`).
- [x] **API Boundary**: Built FastAPI service entrypoint in `apps/api/main.py` with structured `GET /health` endpoint.
- [x] **Web Application Skeleton**: Created Next.js + TypeScript application in `apps/web/` with automated health status connectivity.
- [x] **Testing Suite**: Configured pytest suite with deterministic unit and integration tests.
- [x] **Documentation System**: Created comprehensive AI operating guidelines and architectural contracts (`docs/ai/`, `docs/research/`, `docs/specifications/`).
- [x] **Continuous Integration**: Configured GitHub Actions CI pipeline in `.github/workflows/ci.yml`.

### Phase 1 — Basic Document Statistics
- [x] **Deterministic Text Segmentation**: Implemented `split_paragraphs`, `split_sentences`, and `tokenize_words` in `engine/rightforge/text/segmentation.py`.
- [x] **Basic Text Analyzer**: Implemented `BasicTextAnalyzer` producing 10 surface metrics.
- [x] **API Endpoint**: Exposed `POST /analysis/basic`.
- [x] **Unit & Integration Tests**: Deterministic unit and endpoint tests.

### Phase 2 — Linguistic Metrics
- [x] **Composable Analyzer Framework**: Defined `BaseAnalyzer` contract in `engine/rightforge/analysis/base.py`.
- [x] **Modular Analyzers**:
  - `LexicalAnalyzer`: unique words, TTR, Root TTR, long-word ratio.
  - `SentenceAnalyzer`: mean sentence length, variance, std dev, min/max length.
  - `PunctuationAnalyzer`: frequencies for commas, periods, semicolons, colons, parentheses, question marks, exclamation marks, dashes, quotes, and punctuation density.
  - `LinguisticAnalyzer`: composite pipeline.
- [x] **API Endpoint**: Exposed `POST /analysis/linguistic`.
- [x] **Tests**: Deterministic unit and integration tests.

### Phase 3 — Stylometric Analysis
- [x] **Syllable Estimation**: Implemented phonetic rule-based `count_syllables` in `engine/rightforge/text/syllables.py`.
- [x] **Function Words Lexicon**: Standard closed-class category dictionaries in `engine/rightforge/text/function_words.py`.
- [x] **Stylometry Analyzer**: Implemented `StylometryAnalyzer` in `engine/rightforge/analysis/stylometry.py`:
  - Vocabulary richness: Hapax legomena ($V_1$), Dis legomena ($V_2$), Yule's K characteristic, Simpson's D dominance and diversity indices.
  - Function word distributions: overall ratio, prepositions, pronouns, conjunctions, auxiliary verbs, determiners.
  - Readability indices: Flesch Reading Ease and Flesch-Kincaid Grade Level.
- [x] **API Endpoint**: Exposed `POST /analysis/stylometry` in `apps/api/main.py`.
- [x] **Deterministic Tests**: Added 13 new unit and integration tests (**56 tests total, 100% passing**).
- [x] **Documentation**: Updated `docs/specifications/ANALYZER.md` and `docs/ai/ARCHITECTURE.md`.

---

## 3. Current State

- **Active Phase**: Phase 3 Complete.
- **Engine**: Pure-Python modular analyzers with zero external ML dependencies.
- **Tests**: 56 passed in pytest in ~1.4s.
- **Service**: FastAPI server exposing `GET /health`, `POST /analysis/basic`, `POST /analysis/linguistic`, and `POST /analysis/stylometry`.

---

## 4. Known Limitations

- **No Multi-Document Author Profiles Yet**: Individual document analysis is complete; aggregating multiple documents into a baseline profile with variance models is scheduled for Phase 4.
- **No Persistence**: Storage remains in-memory.
- **No Machine Learning / LLMs**: Explicitly deferred by architectural contract until metric foundations are complete.

---

## 5. Next Milestone: Phase 4 — Writing Profiles

The next bounded objective will implement author profile aggregation:
1. **Author Profile Domain Model**: Define `AuthorProfile` and `MetricBaseline` (mean, variance, min, max, confidence interval) in `engine/rightforge/models/profile.py`.
2. **Profile Engine**: Implement `ProfileAggregator` taking multiple `AnalysisResult` / `Document` inputs and generating an `AuthorProfile`.
3. **API Endpoints**: `POST /profiles/create` to construct an author profile from sample texts.
4. **Deterministic Tests**: Coverage for profile construction, metric variance bounds, and edge cases.
