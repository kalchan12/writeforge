# Metrics Taxonomy & Definitions

## 1. Overview

Writing metrics in RightForge are divided into distinct tiers based on computational complexity and dependency requirements.

## 2. Metric Tiers

### Tier 1: Deterministic Surface Statistics (Phase 1)
* **Character Count**: Raw length and non-whitespace length.
* **Word Count**: Total token count matching word boundaries.
* **Sentence Count**: Sentence boundary segment count.
* **Paragraph Count**: Block-separated textual segments.
* **Length Statistics**: Mean, median, minimum, maximum, and standard deviation of sentence/word lengths.

### Tier 2: Lexical & Punctuation Metrics (Phase 2)
* **Type-Token Ratio (TTR)**: Ratio of unique words ($V$) to total words ($N$): $TTR = V / N$.
* **Root TTR (Guiraud's Index)**: $R = V / \sqrt{N}$ (reduces document length sensitivity).
* **Punctuation Frequencies**: Per-token and per-character frequencies of standard punctuation marks.
* **Long-Word Ratio**: Proportion of tokens exceeding a threshold (e.g., $\ge 7$ characters).

### Tier 3: Readability & Syntactic Indices (Phase 3)
* **Flesch Reading Ease**: $206.835 - 1.015 \cdot (\text{total words} / \text{total sentences}) - 84.6 \cdot (\text{total syllables} / \text{total words})$.
* **Flesch-Kincaid Grade Level**: $0.39 \cdot (\text{total words} / \text{total sentences}) + 11.8 \cdot (\text{total syllables} / \text{total words}) - 15.59$.
* **Syntactic Depth**: Parse tree depth and subordination ratios (deferred).

### Tier 4: Stylometric Fingerprints (Phase 4+)
* **Yule's K**: Characteristic measure of vocabulary richness independent of text length.
* **Function Word Distribution Vector**: Normalized vector across standard function word lists.
