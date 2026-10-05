#!/usr/bin/env python3
"""Evaluation harness for Perplexity and Burstiness modeling across diverse text categories."""

from rightforge.analysis.perplexity import PerplexityAnalyzer

SAMPLE_TEXTS = {
    "Synthetic / Uniform LLM-style": (
        "Artificial intelligence is transforming many industries across the world. "
        "Modern algorithms process large volumes of data with high precision. "
        "These automated systems provide significant efficiencies for business operations. "
        "Machine learning models continue to improve through extensive training datasets. "
        "Organizations adopt advanced technologies to enhance operational productivity."
    ),
    "Varied Human Prose (High Cadence)": (
        "Call me Ishmael. "
        "Some years ago—never mind how long precisely—having little or no money in my purse, "
        "and nothing particular to interest me on shore, I thought I would sail about a little "
        "and see the watery part of the world. "
        "It is a way I have of driving off the spleen and regulating the circulation. "
        "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly "
        "November in my soul; then, I account it high time to get to sea as soon as I can. "
        "Quiet."
    ),
    "Academic / Formal Expository": (
        "The analytical engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves. "
        "A formal demonstration proceeds rigorously from indisputable axioms to valid conclusions. "
        "Science is the systematic enterprise that builds and organizes testable explanations about reality. "
        "Empirical observation remains paramount."
    ),
}


def run_evaluation() -> None:
    print("=================================================================")
    print(" RightForge: Perplexity & Burstiness Research Evaluation (EXP-002)")
    print("=================================================================")

    analyzer = PerplexityAnalyzer()

    print(
        f"{'Text Category':<35} | {'Sentences':<9} | {'Overall PPL':<11} | {'Mean Sent PPL':<13} | {'Burstiness':<10}"
    )
    print("-" * 90)

    for category, text in SAMPLE_TEXTS.items():
        report = analyzer.analyze_perplexity(text)
        print(
            f"{category:<35} | "
            f"{report.sentence_count:<9} | "
            f"{report.overall_perplexity:<11.2f} | "
            f"{report.mean_sentence_perplexity:<13.2f} | "
            f"{report.burstiness:<10.4f}"
        )

    print("-" * 90)
    print("\nDetailed Per-Sentence Perplexity Trajectories:")
    for category, text in SAMPLE_TEXTS.items():
        report = analyzer.analyze_perplexity(text)
        print(f"\n[{category}] - Burstiness: {report.burstiness:.4f}")
        for s in report.sentence_perplexities:
            preview = s.text if len(s.text) <= 55 else s.text[:52] + "..."
            print(f"  Sentence {s.sentence_index + 1} ({s.token_count:2d} tokens): PPL={s.perplexity:7.2f} | \"{preview}\"")
        print(f"  Summary: {report.summary}")


if __name__ == "__main__":
    run_evaluation()
