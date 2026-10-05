# AI Detection Research Foundation

## 1. Overview & Research Stance

RightForge treats AI-generated text detection as an active scientific research field rather than an adversarial contest.

* **Research Objective**: Understand the statistical, information-theoretic, and stylistic signals that distinguish algorithmic text generation from human writing.
* **Non-Goals**: RightForge is **not** an evasion toolkit, scrambler, or academic-integrity bypass utility. It does not provide "guaranteed undetectability" claims.

## 2. Common Detection Paradigms

1. **Perplexity & Token Probability**:
   * Evaluates the cross-entropy or average negative log-likelihood of token sequences under a reference language model:
     $$\text{PPL}(W) = \exp\left(-\frac{1}{N} \sum_{i=1}^N \ln P(w_i \mid w_{<i})\right)$$
   * Machine-generated text tends to exhibit consistently lower perplexity (predictable token trajectories) compared to human text.
2. **Burstiness & Perplexity Variance**:
   * Measures fluctuations in sentence complexity and token perplexity across a document.
   * Formally modeled as the coefficient of variation ($CV$) across sentence-level perplexities:
     $$\text{Burstiness} = \frac{\sigma_{\text{PPL}}}{\mu_{\text{PPL}}} = \frac{\sqrt{\frac{1}{S} \sum_{s=1}^S (\text{PPL}_s - \mu_{\text{PPL}})^2}}{\mu_{\text{PPL}}}$$
   * Human writing typically displays high burstiness ($CV \ge 0.40$), interleaving short staccato bursts with long, complex descriptive clauses.
   * Standard synthetic/LLM generations frequently exhibit uniform cadence ($CV \le 0.22$).
3. **Classifier Models (Supervised Detectors)**:
   * Fine-tuned transformers (e.g., RoBERTa-based discriminators) trained on paired human and synthetic corpora.
   * Often prone to out-of-distribution failure, domain shifts, and vulnerability to stylistic variation.

## 3. RightForge Phase 8 Implementation

RightForge provides a dual-tiered architecture for token probability modeling:
- `NgramProbabilityModel`: A deterministic, zero-dependency, pure-Python Lidstone-smoothed bigram language model for fast, reproducible, offline execution.
- `HuggingFaceProbabilityModel`: An optional wrapper supporting local HuggingFace causal LMs (e.g., `gpt2`, `distilgpt2`) with lazy loading.
- `PerplexityAnalyzer`: Extracts sentence-by-sentence perplexity progression, overall document perplexity, and burstiness ($CV$).
- API Endpoint: `POST /analysis/perplexity` returning `PerplexityReport`.

### Empirical Benchmark (EXP-002)

| Text Category | Sentences | Overall PPL | Mean Sentence PPL | Burstiness ($CV$) | Cadence Classification |
|---|---|---|---|---|---|
| Synthetic / Uniform LLM-style | 5 | 306.87 | 317.65 | **0.2213** | Uniform cadence with low variance |
| Varied Human Prose (High Cadence) | 5 | 241.88 | 270.05 | **0.4270** | Dynamic cadence with high sentence variance |
| Academic / Formal Expository | 4 | 113.08 | 177.31 | **0.6016** | Dynamic cadence with high sentence variance |

## 4. Known Limitations & Research Questions

* **False Positive Disparity**: Studies indicate higher false positive rates for non-native English speakers due to lower lexical entropy.
* **Sensitivity to Topic and Genre**: Technical or formulaic human writing is frequently misclassified as synthetic when detectors over-index on uniform sentence length.
* **Calibration Decay**: Rapid evolution of generation models limits the temporal stability of static detector weights.
