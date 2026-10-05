"use client";

import React, { useEffect, useState } from "react";
import {
  AnalysisResult,
  AuthorProfile,
  PerplexityReport,
  SemanticCoherenceReport,
} from "../types/api";
import {
  analyzeBasic,
  analyzeCoherence,
  analyzeLinguistic,
  analyzePerplexity,
  analyzeStylometry,
  fetchHealth,
} from "../lib/api";
import { MetricCard } from "../components/MetricCard";
import { PerplexityGraph } from "../components/PerplexityGraph";
import { ProfilePanel } from "../components/ProfilePanel";
import { RevisionPanel } from "../components/RevisionPanel";

const PRESET_TEXTS = {
  uniform_synthetic: {
    label: "Uniform Synthetic (LLM-style)",
    text:
      "Artificial intelligence is transforming many industries across the world. " +
      "Modern algorithms process large volumes of data with high precision. " +
      "These automated systems provide significant efficiencies for business operations. " +
      "Machine learning models continue to improve through extensive training datasets. " +
      "Organizations adopt advanced technologies to enhance operational productivity.",
  },
  human_cadence: {
    label: "Varied Human Prose (High Cadence)",
    text:
      "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, " +
      "and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. " +
      "It is a way I have of driving off the spleen and regulating the circulation. " +
      "Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; " +
      "then, I account it high time to get to sea as soon as I can. Quiet.",
  },
  academic_formal: {
    label: "Academic / Formal Expository",
    text:
      "The analytical engine weaves algebraical patterns just as the Jacquard loom weaves flowers and leaves. " +
      "A formal demonstration proceeds rigorously from indisputable axioms to valid conclusions. " +
      "Science is the systematic enterprise that builds and organizes testable explanations about reality. " +
      "Empirical observation remains paramount.",
  },
};

type ActiveTab = "analysis" | "perplexity" | "profiles" | "revision";

export default function DashboardPage() {
  const [text, setText] = useState(PRESET_TEXTS.human_cadence.text);
  const [activeTab, setActiveTab] = useState<ActiveTab>("analysis");
  const [apiHealth, setApiHealth] = useState<{ status: string; service: string; version: string } | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  // Analysis states
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [basicResult, setBasicResult] = useState<AnalysisResult | null>(null);
  const [linguisticResult, setLinguisticResult] = useState<AnalysisResult | null>(null);
  const [stylometryResult, setStylometryResult] = useState<AnalysisResult | null>(null);
  const [coherenceReport, setCoherenceReport] = useState<SemanticCoherenceReport | null>(null);
  const [perplexityReport, setPerplexityReport] = useState<PerplexityReport | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  // Active AuthorProfile state
  const [activeProfile, setActiveProfile] = useState<AuthorProfile | null>(null);

  useEffect(() => {
    fetchHealth()
      .then((h) => setApiHealth(h))
      .catch((err: unknown) => {
        setApiError(err instanceof Error ? err.message : "API server unreachable");
      });
  }, []);

  const runAllAnalyses = async (contentToAnalyze?: string) => {
    const targetText = contentToAnalyze ?? text;
    if (!targetText.trim()) return;

    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      const [basic, linguistic, stylometry, coherence, ppl] = await Promise.all([
        analyzeBasic(targetText),
        analyzeLinguistic(targetText),
        analyzeStylometry(targetText),
        analyzeCoherence(targetText),
        analyzePerplexity(targetText),
      ]);

      setBasicResult(basic);
      setLinguisticResult(linguistic);
      setStylometryResult(stylometry);
      setCoherenceReport(coherence);
      setPerplexityReport(ppl);
    } catch (err: unknown) {
      setAnalysisError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Run initial analysis once on mount
  useEffect(() => {
    runAllAnalyses(PRESET_TEXTS.human_cadence.text);
  }, []);

  const handlePresetSelect = (presetKey: keyof typeof PRESET_TEXTS) => {
    const selected = PRESET_TEXTS[presetKey].text;
    setText(selected);
    runAllAnalyses(selected);
  };

  const getMetric = (result: AnalysisResult | null, name: string): number => {
    if (!result || !result.metrics[name]) return 0;
    return result.metrics[name].value;
  };

  return (
    <div
      style={{
        maxWidth: "1140px",
        margin: "0 auto",
        padding: "2rem 1.5rem 5rem",
        display: "flex",
        flexDirection: "column",
        gap: "1.75rem",
      }}
    >
      {/* Top Header */}
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "1rem",
          borderBottom: "1px solid var(--border-color, #2d3345)",
          paddingBottom: "1.25rem",
        }}
      >
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
            <h1 style={{ fontSize: "1.75rem", fontWeight: 800, letterSpacing: "-0.03em" }}>
              RightForge
            </h1>
            <span
              style={{
                fontSize: "0.7rem",
                padding: "0.2rem 0.5rem",
                borderRadius: "9999px",
                backgroundColor: "#1e3a8a",
                color: "#60a5fa",
                fontWeight: 600,
              }}
            >
              RESEARCH SUITE v0.1.0
            </span>
          </div>
          <p style={{ color: "var(--text-muted, #9aa0a6)", fontSize: "0.9rem", marginTop: "0.2rem" }}>
            Local-first writing analysis, stylometrics, perplexity modeling, and controlled revision
          </p>
        </div>

        {/* Backend health status pill */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
            fontSize: "0.8rem",
            padding: "0.4rem 0.85rem",
            borderRadius: "9999px",
            backgroundColor: "#12151f",
            border: "1px solid var(--border-color, #2d3345)",
          }}
        >
          <span
            style={{
              width: "8px",
              height: "8px",
              borderRadius: "50%",
              backgroundColor: apiHealth ? "#34d399" : "#f87171",
              display: "inline-block",
            }}
          />
          {apiHealth ? (
            <span style={{ color: "#34d399" }}>
              FastAPI Online ({apiHealth.service})
            </span>
          ) : (
            <span style={{ color: "#f87171" }}>
              API Offline ({apiError || "Port 8000"})
            </span>
          )}
        </div>
      </header>

      {/* Editor & Control Section */}
      <section
        style={{
          backgroundColor: "var(--card-bg, #1a1d27)",
          border: "1px solid var(--border-color, #2d3345)",
          borderRadius: "8px",
          padding: "1.25rem",
          display: "flex",
          flexDirection: "column",
          gap: "1rem",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "0.5rem",
          }}
        >
          <label style={{ fontSize: "0.85rem", fontWeight: 600, color: "var(--text-muted, #9aa0a6)" }}>
            SOURCE DOCUMENT TEXT:
          </label>

          {/* Preset Buttons */}
          <div style={{ display: "flex", alignItems: "center", gap: "0.4rem", flexWrap: "wrap" }}>
            <span style={{ fontSize: "0.75rem", color: "var(--text-muted, #9aa0a6)" }}>Presets:</span>
            {Object.entries(PRESET_TEXTS).map(([key, item]) => (
              <button
                key={key}
                onClick={() => handlePresetSelect(key as keyof typeof PRESET_TEXTS)}
                style={{
                  backgroundColor: "#12151f",
                  border: "1px solid var(--border-color, #2d3345)",
                  color: "#e2e8f0",
                  borderRadius: "4px",
                  padding: "0.25rem 0.6rem",
                  fontSize: "0.75rem",
                  cursor: "pointer",
                }}
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>

        <textarea
          rows={5}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter or paste text to analyze..."
          style={{
            width: "100%",
            backgroundColor: "#12151f",
            border: "1px solid var(--border-color, #2d3345)",
            borderRadius: "6px",
            padding: "0.85rem",
            color: "var(--text-main, #f0f2f5)",
            fontSize: "0.95rem",
            lineHeight: 1.6,
            fontFamily: "inherit",
            resize: "vertical",
          }}
        />

        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "0.5rem" }}>
          <div style={{ fontSize: "0.8rem", color: "var(--text-muted, #9aa0a6)" }}>
            {getMetric(basicResult, "word_count")} words &bull;{" "}
            {getMetric(basicResult, "sentence_count")} sentences &bull;{" "}
            {getMetric(basicResult, "paragraph_count")} paragraphs
          </div>

          <div style={{ display: "flex", gap: "0.5rem" }}>
            <button
              onClick={() => {
                setText("");
                setBasicResult(null);
                setLinguisticResult(null);
                setStylometryResult(null);
                setCoherenceReport(null);
                setPerplexityReport(null);
              }}
              style={{
                backgroundColor: "transparent",
                border: "1px solid var(--border-color, #2d3345)",
                color: "var(--text-muted, #9aa0a6)",
                borderRadius: "6px",
                padding: "0.5rem 0.85rem",
                fontSize: "0.85rem",
                cursor: "pointer",
              }}
            >
              Clear Text
            </button>

            <button
              onClick={() => runAllAnalyses()}
              disabled={isAnalyzing || !text.trim()}
              style={{
                backgroundColor: "#4f80ff",
                color: "#ffffff",
                border: "none",
                borderRadius: "6px",
                padding: "0.5rem 1.25rem",
                fontWeight: 600,
                fontSize: "0.85rem",
                cursor: isAnalyzing || !text.trim() ? "not-allowed" : "pointer",
              }}
            >
              {isAnalyzing ? "Computing Metrics..." : "Run Full Analysis"}
            </button>
          </div>
        </div>

        {analysisError && (
          <div
            style={{
              padding: "0.6rem 0.85rem",
              borderRadius: "4px",
              backgroundColor: "#7f1d1d33",
              border: "1px solid #f87171",
              color: "#f87171",
              fontSize: "0.85rem",
            }}
          >
            {analysisError}
          </div>
        )}
      </section>

      {/* Navigation Tabs */}
      <nav
        style={{
          display: "flex",
          borderBottom: "1px solid var(--border-color, #2d3345)",
          gap: "0.5rem",
        }}
      >
        {[
          { key: "analysis", label: "1. Document Metrics" },
          { key: "perplexity", label: "2. Cadence & Perplexity" },
          { key: "profiles", label: "3. Writing Profiles" },
          { key: "revision", label: "4. Controlled Revision" },
        ].map((tab) => {
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as ActiveTab)}
              style={{
                background: "none",
                border: "none",
                borderBottom: isActive ? "2px solid #4f80ff" : "2px solid transparent",
                padding: "0.6rem 1rem",
                fontWeight: isActive ? 600 : 500,
                color: isActive ? "#ffffff" : "var(--text-muted, #9aa0a6)",
                cursor: "pointer",
                fontSize: "0.9rem",
              }}
            >
              {tab.label}
            </button>
          );
        })}
      </nav>

      {/* TAB 1: Document Metrics & Stylometry */}
      {activeTab === "analysis" && (
        <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
          {/* Surface & Cadence Metrics */}
          <div>
            <h3 style={{ fontSize: "1rem", fontWeight: 600, marginBottom: "0.75rem", color: "#60a5fa" }}>
              Surface & Sentence Cadence
            </h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: "0.85rem" }}>
              <MetricCard
                label="Word Count"
                value={getMetric(basicResult, "word_count")}
                description="Total extracted tokens"
              />
              <MetricCard
                label="Sentence Count"
                value={getMetric(basicResult, "sentence_count")}
                description="Total segmented sentences"
              />
              <MetricCard
                label="Avg Words / Sent"
                value={getMetric(basicResult, "avg_words_per_sentence")}
                description="Mean sentence length"
                badge={{
                  text: getMetric(basicResult, "avg_words_per_sentence") > 25 ? "Elevated" : "Standard",
                  variant: getMetric(basicResult, "avg_words_per_sentence") > 25 ? "warning" : "success",
                }}
              />
              <MetricCard
                label="Length Std Dev"
                value={getMetric(linguisticResult, "sentence_length_std_dev")}
                description="Sentence length dispersion"
                badge={{
                  text: getMetric(linguisticResult, "sentence_length_std_dev") < 3 ? "Low Variance" : "Dynamic",
                  variant: getMetric(linguisticResult, "sentence_length_std_dev") < 3 ? "warning" : "accent",
                }}
              />
            </div>
          </div>

          {/* Lexical & Stylometric Richness */}
          <div>
            <h3 style={{ fontSize: "1rem", fontWeight: 600, marginBottom: "0.75rem", color: "#34d399" }}>
              Vocabulary Richness & Readability
            </h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))", gap: "0.85rem" }}>
              <MetricCard
                label="Type-Token Ratio"
                value={getMetric(linguisticResult, "type_token_ratio")}
                description="Unique words / total words"
              />
              <MetricCard
                label="Flesch Reading Ease"
                value={getMetric(stylometryResult, "flesch_reading_ease")}
                description="Higher scores = easier readability (0-100)"
              />
              <MetricCard
                label="Flesch-Kincaid Grade"
                value={getMetric(stylometryResult, "flesch_kincaid_grade")}
                unit="Grade"
                description="Approximate US education level"
              />
              <MetricCard
                label="Yule's K Characteristic"
                value={getMetric(stylometryResult, "yules_k")}
                description="Length-invariant vocabulary richness"
              />
            </div>
          </div>

          {/* Semantic Coherence Summary */}
          {coherenceReport && (
            <div
              style={{
                backgroundColor: "var(--card-bg, #1a1d27)",
                border: "1px solid var(--border-color, #2d3345)",
                borderRadius: "8px",
                padding: "1.25rem",
                display: "flex",
                flexDirection: "column",
                gap: "0.75rem",
              }}
            >
              <h3 style={{ fontSize: "1rem", fontWeight: 600, color: "#fbbf24" }}>
                Semantic Coherence & Lexical Continuity
              </h3>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "0.75rem" }}>
                <MetricCard
                  label="Paragraph Flow"
                  value={coherenceReport.mean_paragraph_coherence}
                  description="Adjacent paragraph Jaccard continuity"
                />
                <MetricCard
                  label="Sentence Flow"
                  value={coherenceReport.mean_sentence_coherence}
                  description="Adjacent sentence Jaccard continuity"
                />
                <MetricCard
                  label="Content Word Repetition"
                  value={coherenceReport.lexical_repetition_rate}
                  description="Proportion of reused content words"
                />
                <MetricCard
                  label="Abrupt Shifts"
                  value={coherenceReport.abrupt_transitions_count}
                  description="Transitions with near-zero continuity"
                  badge={{
                    text: coherenceReport.abrupt_transitions_count === 0 ? "Smooth" : "Disjunct",
                    variant: coherenceReport.abrupt_transitions_count === 0 ? "success" : "danger",
                  }}
                />
              </div>
              <p style={{ fontSize: "0.85rem", color: "var(--text-muted, #9aa0a6)", marginTop: "0.25rem" }}>
                {coherenceReport.summary}
              </p>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: Perplexity & Cadence Visualizer */}
      {activeTab === "perplexity" && (
        <PerplexityGraph report={perplexityReport} />
      )}

      {/* TAB 3: Author Writing Profiles */}
      {activeTab === "profiles" && (
        <ProfilePanel
          currentText={text}
          activeProfile={activeProfile}
          onProfileSelect={(p) => setActiveProfile(p)}
        />
      )}

      {/* TAB 4: Controlled Revision Workbench */}
      {activeTab === "revision" && (
        <RevisionPanel
          currentText={text}
          activeProfile={activeProfile}
          onApplyRevisedText={(revised) => {
            setText(revised);
            runAllAnalyses(revised);
            setActiveTab("analysis");
          }}
        />
      )}
    </div>
  );
}
