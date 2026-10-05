# Stylometry & Authorship Research

## 1. Foundations of Stylometry

Stylometry is the quantitative study of literary style through computational linguistics. It operates on the foundational hypothesis that individual writers possess subconscious, consistent stylistic habits ("stylistic invariants") that can be extracted and measured.

## 2. Stylometric Feature Dimensions

1. **Lexical**:
   * Word frequency distributions, vocabulary richness, Type-Token Ratio (TTR), Simpson's D index, Yule's K characteristic.
   * Distribution of hapax legomena (words appearing once) and dis legomena (words appearing twice).
2. **Structural & Syntactic**:
   * Sentence length distributions, clause density, subordination indices.
   * Part-of-speech (POS) tag sequence frequencies and transition matrices.
3. **Punctuation & Orthography**:
   * Punctuation mark densities and idiosyncratic usage patterns (semicolons, em dashes, parentheses).
   * Contraction usage rates and hyphenation behaviors.
4. **Function Words**:
   * Relative frequencies of topic-neutral function words (prepositions, conjunctions, articles, pronouns).
   * Highly resistant to intentional masking and topic bias.

## 3. Application in RightForge

In RightForge, stylometry provides the mathematical foundation for:
* Building multi-document author writing profiles.
* Measuring authorial consistency across drafts.
* Preserving author voice during revision workflows.
