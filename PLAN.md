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
- [x] **Deterministic Text Segmentation**: Implemented `split_paragraphs`, `split_sentences`, and `tokenize_words` in `engine/rightforge/text/segmentation.py` with robust handling of abbreviations, decimals, quotes, and Unicode.
- [x] **Basic Text Analyzer**: Implemented `BasicTextAnalyzer` in `engine/rightforge/analysis/basic.py` producing 10 exact surface metrics:
  - `character_count`
  - `non_whitespace_char_count`
  - `word_count`
  - `sentence_count`
  - `paragraph_count`
  - `avg_words_per_sentence`
  - `avg_chars_per_word`
  - `min_sentence_length`
  - `max_sentence_length`
  - `sentence_length_std_dev`
- [x] **API Endpoint**: Exposed `POST /analysis/basic` in `apps/api/main.py` with Pydantic request validation and structured `AnalysisResult` responses.
- [x] **Unit & Integration Tests**: Added 21 new tests across `tests/unit/test_segmentation.py`, `tests/unit/test_basic_analysis.py`, and `tests/integration/test_basic_analysis_api.py` (total 29 tests, 100% passing).
- [x] **Documentation Updated**: Synchronized `docs/specifications/ANALYZER.md` and `docs/ai/ARCHITECTURE.md`.

---

## 3. Current State

- **Active Phase**: Phase 1 Complete.
- **Engine**: Pure Python core analysis modules operational without heavy external dependencies.
- **Tests**: 29 passed in pytest.
- **Service**: FastAPI server exposing `GET /health` and `POST /analysis/basic`.

---

## 4. Known Limitations

- **No Linguistic Metrics Yet**: Phase 1 only calculates surface statistics. Vocabulary diversity, type-token ratio (TTR), and punctuation frequencies are deferred to Phase 2.
- **No Persistence**: Storage remains in-memory.
- **No Machine Learning / LLMs**: Explicitly deferred by architectural contract until metric foundations are complete.

---

## 5. Next Milestone: Phase 2 — Linguistic Metrics

The next bounded objective will implement modular linguistic analyzers:
1. **Lexical metrics**: unique word count, type-token ratio (TTR), root TTR, long-word ratio.
2. **Sentence structure**: sentence-length variance, distribution percentiles.
3. **Punctuation analyzer**: frequency and density of specific punctuation marks (commas, semicolons, colons, dashes, question marks).
4. Composable analyzer architecture: `LexicalAnalyzer`, `SentenceAnalyzer`, `PunctuationAnalyzer`.
5. API endpoint `POST /analysis/linguistic`.
6. Deterministic unit and integration tests.
