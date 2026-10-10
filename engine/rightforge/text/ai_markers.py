"""Catalog of distinct lexical, transition, and phrase markers characteristic of ChatGPT and other LLMs."""

import re

# High-frequency words disproportionately over-represented in LLM outputs relative to human writing
AI_SIGNATURE_WORDS: frozenset[str] = frozenset({
    "delve", "delves", "delving",
    "tapestry", "testament",
    "unwavering", "beacon",
    "multifaceted", "intertwined", "intertwine",
    "pivotal", "paramount",
    "foster", "fosters", "fostering",
    "leverage", "leverages", "leveraging",
    "underscore", "underscores", "underscoring",
    "showcase", "showcases", "showcasing",
    "meticulous", "meticulously",
    "intricate", "intricacies",
    "transformative",
    "burgeoning",
    "seamless", "seamlessly",
    "holistic",
    "vital", "crucial",
    "vibrant",
    "plethora", "myriad",
    "embark", "embarks", "embarking",
    "realm", "realms",
    "landscape", "landscapes",
    "synergy", "synergies",
    "nuanced", "nuance", "nuances",
    "poised",
    "crucible",
    "conduit",
    "bedrock",
    "cornerstone",
    "linchpin",
    "epitome",
    "imperative",
    "profound", "profoundly",
    "indispensable",
    "inextricably",
    "resonate", "resonates", "resonating",
    "harness", "harnesses", "harnessing",
    "catalyst", "catalysts",
})

# Multi-word transition phrases strongly favored by ChatGPT / Claude / Gemini
AI_SIGNATURE_PHRASES: list[tuple[re.Pattern, str, float]] = [
    # (regex pattern, name, weight/severity)
    (re.compile(r"\bdelve into\b", re.IGNORECASE), "delve into", 1.0),
    (re.compile(r"\brich tapestry\b", re.IGNORECASE), "rich tapestry", 1.0),
    (re.compile(r"\ba testament to\b", re.IGNORECASE), "a testament to", 0.9),
    (re.compile(r"\bplays a pivotal role\b", re.IGNORECASE), "plays a pivotal role", 0.9),
    (re.compile(r"\bplays a crucial role\b", re.IGNORECASE), "plays a crucial role", 0.8),
    (re.compile(r"\bplay a pivotal role\b", re.IGNORECASE), "play a pivotal role", 0.9),
    (re.compile(r"\bplay a crucial role\b", re.IGNORECASE), "play a crucial role", 0.8),
    (re.compile(r"\bit is important to note that\b", re.IGNORECASE), "it is important to note that", 0.8),
    (re.compile(r"\bit is worth noting that\b", re.IGNORECASE), "it is worth noting that", 0.8),
    (re.compile(r"\bit is crucial to\b", re.IGNORECASE), "it is crucial to", 0.7),
    (re.compile(r"\bit is essential to\b", re.IGNORECASE), "it is essential to", 0.7),
    (re.compile(r"\bin the ever-evolving landscape\b", re.IGNORECASE), "in the ever-evolving landscape", 1.0),
    (re.compile(r"\bin today's fast-paced world\b", re.IGNORECASE), "in today's fast-paced world", 0.9),
    (re.compile(r"\bat the intersection of\b", re.IGNORECASE), "at the intersection of", 0.7),
    (re.compile(r"\bnavigating the complexities\b", re.IGNORECASE), "navigating the complexities", 0.9),
    (re.compile(r"\ba beacon of\b", re.IGNORECASE), "a beacon of", 0.8),
    (re.compile(r"\bstands as a testament\b", re.IGNORECASE), "stands as a testament", 0.9),
    (re.compile(r"\bparadigm shift\b", re.IGNORECASE), "paradigm shift", 0.6),
    (re.compile(r"\bnot only\b.*?\bbut also\b", re.IGNORECASE), "not only... but also", 0.4),
]

# Rigid sentence-starter transitions typical of LLM discourse markers
AI_TRANSITION_STARTERS: list[re.Pattern] = [
    re.compile(r"^\s*Furthermore,?\s+", re.IGNORECASE),
    re.compile(r"^\s*Moreover,?\s+", re.IGNORECASE),
    re.compile(r"^\s*Additionally,?\s+", re.IGNORECASE),
    re.compile(r"^\s*Consequently,?\s+", re.IGNORECASE),
    re.compile(r"^\s*In conclusion,?\s+", re.IGNORECASE),
    re.compile(r"^\s*To summarize,?\s+", re.IGNORECASE),
    re.compile(r"^\s*Ultimately,?\s+", re.IGNORECASE),
    re.compile(r"^\s*Importantly,?\s+", re.IGNORECASE),
    re.compile(r"^\s*Significantly,?\s+", re.IGNORECASE),
    re.compile(r"^\s*Notably,?\s+", re.IGNORECASE),
]


def detect_ai_lexical_markers(text: str) -> dict:
    """Analyze text for presence and density of AI signature words, phrases, and transition starters."""
    if not text.strip():
        return {
            "total_matches": 0,
            "density_per_100_words": 0.0,
            "matched_hallmarks": [],
            "matched_phrases": [],
            "matched_starters": [],
        }

    words = re.findall(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b", text.lower())
    total_words = len(words)
    matched_words = [w for w in words if w in AI_SIGNATURE_WORDS]

    matched_phrases = []
    for pattern, phrase_name, _ in AI_SIGNATURE_PHRASES:
        if pattern.search(text):
            matched_phrases.append(phrase_name)

    sentences = [s.strip() for s in re.split(r"[.!?]+", text) if s.strip()]
    matched_starters = []
    for s in sentences:
        for starter in AI_TRANSITION_STARTERS:
            if starter.match(s):
                matched_starters.append(s[:25].strip())

    total_matches = len(matched_words) + len(matched_phrases) + len(matched_starters)
    density = (total_matches / max(total_words, 1)) * 100.0

    return {
        "total_matches": total_matches,
        "density_per_100_words": round(density, 2),
        "matched_hallmarks": matched_words,
        "matched_phrases": matched_phrases,
        "matched_starters": matched_starters,
    }

