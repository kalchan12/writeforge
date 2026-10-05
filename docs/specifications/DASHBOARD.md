# Web UI & Research Dashboard Specification

## 1. Overview & Purpose

The **RightForge Web UI & Research Dashboard** is a local-first interface built with Next.js 14, React 18, and TypeScript. It connects directly to the RightForge FastAPI backend running on `http://localhost:8000`.

It provides authors and linguistic researchers with an interactive workbench to evaluate texts, visualize information-theoretic token probabilities, construct author writing profiles, and execute controlled style-conditioned revisions.

---

## 2. Core Interactive Views (Tabs)

### Tab 1: Document Metrics & Stylometry
* **Surface Statistics**: Word count, sentence count, paragraph count, and average words per sentence.
* **Sentence Cadence**: Sentence length standard deviation with dynamic vs. low-variance badges.
* **Vocabulary Richness**: Type-Token Ratio (TTR), Yule's K Characteristic, and Simpson's Index.
* **Readability**: Flesch Reading Ease score and Flesch-Kincaid Grade Level.
* **Semantic Coherence**: Adjacent paragraph and sentence lexical continuity scores, content word repetition rates, and abrupt transition flags.

### Tab 2: Cadence & Perplexity Visualizer
* **Sentence Trajectory Chart**: Interactive SVG curve plotting sentence-by-sentence perplexity progression.
* **Burstiness Index**: Document-level coefficient of variation ($CV = \sigma_{\text{PPL}} / \mu_{\text{PPL}}$) with cadence badge (Human vs. Synthetic).
* **Sentence Inspection**: Interactive click-to-inspect card showing token count, perplexity score, and verbatim sentence text.

### Tab 3: Author Writing Profiles
* **Profile Builder**: Accepts multiple sample documents and constructs a quantitative author signature with metric baselines.
* **Consistency Comparator**: Evaluates target text against the active profile, outputting an overall consistency score ($0.0 - 1.0$) and identifying statistical outlier metrics with standard deviation z-scores.

### Tab 4: Controlled Revision Workbench
* **Diagnostic Strategy**: Formulates global directional revision goals and granular sentence-level interventions.
* **Inference Configuration**: Supports one-click execution via local Ollama HTTP daemon (`http://localhost:11434`) or offline deterministic mock mode.
* **Verification & Side-by-Side Diff**: Displays original vs. revised candidate text alongside before-and-after metric shifts and consistency score deltas.

---

## 3. Architecture & Data Flow

* **Client**: Typed API client in `apps/web/src/lib/api.ts` connecting to all 9 FastAPI backend endpoints.
* **Zero External Telemetry**: All requests execute over localhost without external CDN or cloud dependencies.
