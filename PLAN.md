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
- [x] **Basic Text Analyzer**: Implemented `BasicTextAnalyzer` in `engine/rightforge/analysis/basic.py` producing 10 surface metrics.
- [x] **API Endpoint**: Exposed `POST /analysis/basic`.
- [x] **Unit & Integration Tests**: Deterministic unit and endpoint tests.

### Phase 2 — Linguistic Metrics
- [x] **Composable Analyzer Framework**: Defined `BaseAnalyzer` contract in `engine/rightforge/analysis/base.py`.
- [x] **Lexical Analyzer**: Implemented `LexicalAnalyzer` (`unique_word_count`, `type_token_ratio`, `root_type_token_ratio`, `average_word_length`, `long_word_ratio`).
- [x] **Sentence Analyzer**: Implemented `SentenceAnalyzer` (`sentence_count`, `sentence_length_mean`, `sentence_length_variance`, `sentence_length_std_dev`, `shortest_sentence_length`, `longest_sentence_length`).
- [x] **Punctuation Analyzer**: Implemented `PunctuationAnalyzer` (frequencies for commas, periods, semicolons, colons, parentheses, question marks, exclamation marks, dashes, quotes, and punctuation density per char and per word).
- [x] **Composite Pipeline**: Implemented `LinguisticAnalyzer` in `engine/rightforge/analysis/linguistic.py` orchestrating constituent modular analyzers into a unified `AnalysisResult`.
- [x] **API Endpoint**: Exposed `POST /analysis/linguistic` in `apps/api/main.py`.
- [x] **Deterministic Tests**: Added 14 new tests across lexical, sentence, punctuation, composite, and API integration suites (**43 tests total, 100% passing**).
- [x] **Documentation**: Updated `docs/specifications/ANALYZER.md` and `docs/ai/ARCHITECTURE.md`.

---

## 3. Current State

- **Active Phase**: Phase 2 Complete.
- **Engine**: Pure-Python modular analyzers with zero external ML dependencies.
- **Tests**: 43 passed in pytest in ~1.3s.
- **Service**: FastAPI server exposing `GET /health`, `POST /analysis/basic`, and `POST /analysis/linguistic`.

---

## 4. Known Limitations

- **No Stylometric Fingerprinting Yet**: Authorship invariants, function word distributions, and Yule's K are scheduled for Phase 3.
- **No Persistence**: Storage remains in-memory.
- **No Machine Learning / LLMs**: Explicitly deferred by architectural contract until metric foundations are complete.

---

## 5. Next Milestone: Phase 3 — Stylometric Analysis

The next bounded objective will implement authorial fingerprinting and stylometry metrics:
1. **Function word distribution**: Relative frequencies of closed-class function words (prepositions, conjunctions, pronouns, auxiliary verbs).
2. **Vocabulary richness metrics**: Yule's K characteristic ($K = 10^4 \cdot \frac{\sum i^2 V_i - N}{N^2}$), Simpson's D index, Hapax legomena and Dis legomena counts.
3. **Readability indices**: Flesch Reading Ease and Flesch-Kincaid Grade Level (using deterministic syllable estimation).
4. `StylometryAnalyzer` component and `POST /analysis/stylometry` endpoint.
5. Deterministic unit and integration tests.
