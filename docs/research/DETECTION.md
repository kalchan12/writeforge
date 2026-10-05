# AI Detection Research Foundation

## 1. Overview & Research Stance

RightForge treats AI-generated text detection as an active scientific research field rather than an adversarial contest.

* **Research Objective**: Understand the statistical, information-theoretic, and stylistic signals that distinguish algorithmic text generation from human writing.
* **Non-Goals**: RightForge is **not** an evasion toolkit, scrambler, or academic-integrity bypass utility. It does not provide "guaranteed undetectability" claims.

## 2. Common Detection Paradigms

1. **Perplexity & Token Probability**:
   * Evaluates the cross-entropy or average log-likelihood of token sequences under a reference language model.
   * Machine-generated text tends to exhibit consistently lower perplexity (predictable token trajectories) compared to human text.
2. **Burstiness & Perplexity Variance**:
   * Measures fluctuations in sentence length, structure, and token perplexity across a document.
   * Human writing typically displays high burstiness (interleaving short/long sentences and common/uncommon phrasing), while standard LLM outputs often display uniform cadence.
3. **Classifier Models (Supervised Detectors)**:
   * Fine-tuned transformers (e.g., RoBERTa-based discriminators) trained on paired human and synthetic corpora.
   * Often prone to out-of-distribution failure, domain shifts, and vulnerability to stylistic variation.

## 3. Known Limitations & Research Questions

* **False Positive Disparity**: Studies indicate higher false positive rates for non-native English speakers due to lower lexical entropy.
* **Sensitivity to Topic and Genre**: Technical or formulaic human writing is frequently misclassified as synthetic.
* **Calibration Decay**: Rapid evolution of generation models limits the temporal stability of static detector weights.
