"""Unit tests for the AIDetector engine."""

import pytest
from rightforge.analysis.ai_detector import AIDetector
from rightforge.text.ai_markers import detect_ai_lexical_markers


def test_ai_lexical_markers_detects_chatgpt_tropes():
    ai_text = (
        "In the ever-evolving landscape of artificial intelligence, it is paramount to delve into the rich tapestry "
        "of technology. Furthermore, this serves as a testament to human innovation, which plays a pivotal role. "
        "Moreover, we must foster collaborative solutions to seamlessly leverage these capabilities. In conclusion, it is multifaceted."
    )
    result = detect_ai_lexical_markers(ai_text)
    assert result["total_matches"] > 0
    assert result["density_per_100_words"] > 5.0
    assert "delve" in result["matched_hallmarks"]
    assert "tapestry" in result["matched_hallmarks"]
    assert len(result["matched_phrases"]) > 0


def test_ai_lexical_markers_clean_human_text():
    human_text = "Call me Ishmael. Some years ago, never mind how long precisely, having little or no money in my purse."
    result = detect_ai_lexical_markers(human_text)
    assert result["total_matches"] == 0
    assert result["density_per_100_words"] == 0.0


def test_ai_detector_empty_text():
    detector = AIDetector()
    report = detector.detect("")
    assert report.ai_score == 0.0
    assert report.ai_score_percent == 0.0
    assert report.verdict == "No Content"
    assert report.confidence == "low"
    assert len(report.signals) == 0


def test_ai_detector_hallmark_synthetic_text():
    detector = AIDetector()
    ai_text = (
        "In the ever-evolving landscape of technology, it is paramount that we delve deep into the rich tapestry "
        "of innovation. Furthermore, artificial intelligence serves as a testament to modern human ingenuity. "
        "Moreover, these models play a pivotal role in shaping how organizations foster collaborative synergy. "
        "Additionally, leaders must leverage dynamic frameworks to seamlessly transform contemporary workflows. "
        "In conclusion, the multifaceted potential of this domain underscores our commitment to sustainable progress."
    )
    report = detector.detect(ai_text)
    assert report.ai_score_percent >= 60.0
    assert report.verdict == "Likely AI"
    assert report.confidence in ["medium", "high"]
    signal_names = [s.name for s in report.signals]
    assert "AI Vocabulary Fingerprint" in signal_names


def test_ai_detector_human_prose():
    detector = AIDetector()
    human_text = (
        "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, "
        "and nothing particular to interest me on shore, I thought I would sail about a little and see the watery "
        "part of the world. It is a way I have of driving off the spleen and regulating the circulation. "
        "Whenever I find myself growing grim about the mouth, I quietly take to the ship."
    )
    report = detector.detect(human_text)
    assert report.ai_score_percent <= 35.0
    assert report.verdict == "Likely Human"
