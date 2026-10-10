"use client";

import React, { useState, useEffect } from "react";
import AIScoreGauge from "../components/AIScoreGauge";
import DiffViewer from "../components/DiffViewer";
import { detectAI, executeRevision, fetchHealth, AIDetectionReport } from "../lib/api";
import { RevisionExecutionResult } from "../types/api";

export default function Page() {
  const [text, setText] = useState("");
  const [healthStatus, setHealthStatus] = useState("checking");
  const [detecting, setDetecting] = useState(false);
  const [humanizing, setHumanizing] = useState(false);
  const [copied, setCopied] = useState(false);
  
  const [aiReport, setAiReport] = useState<AIDetectionReport | null>(null);
  const [revisionResult, setRevisionResult] = useState<RevisionExecutionResult | null>(null);
  const [revisedAiReport, setRevisedAiReport] = useState<AIDetectionReport | null>(null);
  const [diffViewMode, setDiffViewMode] = useState<"side-by-side" | "raw">("side-by-side");
  
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHealth()
      .then(() => setHealthStatus("ok"))
      .catch(() => setHealthStatus("error"));
  }, []);

  const handleDetectAI = async () => {
    if (!text.trim()) return;
    setDetecting(true);
    setError(null);
    try {
      const report = await detectAI(text);
      setAiReport(report);
    } catch (err: any) {
      setError(err.message || "Failed to detect AI.");
    } finally {
      setDetecting(false);
    }
  };

  const handleHumanize = async () => {
    if (!text.trim()) return;
    setHumanizing(true);
    setError(null);
    try {
      const [result, origReport] = await Promise.all([
        executeRevision(text, { provider: "antigravity", model: "gemini-3.8-flash-low", useMock: false }),
        aiReport ? Promise.resolve(aiReport) : detectAI(text).catch(() => null),
      ]);
      setRevisionResult(result);
      if (origReport) {
        setAiReport(origReport);
      }

      if (result.revised_text) {
        detectAI(result.revised_text)
          .then((revReport) => setRevisedAiReport(revReport))
          .catch(() => setRevisedAiReport(null));
      }
    } catch (err: any) {
      setError(err.message || "Failed to humanize text.");
    } finally {
      setHumanizing(false);
    }
  };

  const handleCopy = () => {
    if (revisionResult?.revised_text) {
      navigator.clipboard.writeText(revisionResult.revised_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleUseRevised = () => {
    if (revisionResult?.revised_text) {
      setText(revisionResult.revised_text);
      setRevisionResult(null);
      setRevisedAiReport(null);
      if (revisedAiReport) {
        setAiReport(revisedAiReport);
      }
    }
  };

  const charCount = text.length;
  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;

  return (
    <div style={{
      minHeight: "100vh",
      backgroundColor: "var(--bg-color)",
      color: "var(--text-main)",
      fontFamily: "system-ui, -apple-system, sans-serif",
      display: "flex",
      flexDirection: "column",
    }}>
      {/* Header */}
      <header style={{
        padding: "1rem 2rem",
        borderBottom: "1px solid var(--border-color)",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        backgroundColor: "var(--card-bg)"
      }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: "1rem" }}>
          <h1 style={{ margin: 0, fontSize: "1.5rem", fontWeight: "bold", color: "var(--text-main)" }}>
            WriteForge
          </h1>
          <span style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>
            AI Content Detector & Humanizer
          </span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
          <div style={{
            width: "8px", height: "8px", borderRadius: "50%",
            backgroundColor: healthStatus === "ok" ? "var(--success-color)" : 
                             healthStatus === "checking" ? "#eab308" : "#ef4444"
          }} />
          <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
            {healthStatus === "ok" ? "System Online" : 
             healthStatus === "checking" ? "Checking..." : "System Offline"}
          </span>
        </div>
      </header>

      {/* Main Layout */}
      <main style={{
        display: "flex",
        flexDirection: "row",
        flex: 1,
        padding: "2rem",
        gap: "2rem",
        maxWidth: "1400px",
        margin: "0 auto",
        width: "100%",
        boxSizing: "border-box",
        flexWrap: "wrap"
      }}>
        {/* Left Panel */}
        <section style={{
          flex: "1 1 500px",
          display: "flex",
          flexDirection: "column",
          gap: "1rem"
        }}>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your text here to analyze or humanize..."
            rows={12}
            style={{
              width: "100%",
              backgroundColor: "var(--card-bg)",
              border: "1px solid var(--border-color)",
              borderRadius: "8px",
              padding: "1rem",
              color: "var(--text-main)",
              fontSize: "1rem",
              lineHeight: "1.5",
              resize: "vertical",
              outline: "none",
              boxSizing: "border-box"
            }}
          />
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", color: "var(--text-muted)", fontSize: "0.875rem" }}>
            <span>{wordCount} words | {charCount} characters</span>
            <button 
              onClick={() => { setText(""); setAiReport(null); setRevisionResult(null); setRevisedAiReport(null); }}
              style={{
                background: "none",
                border: "none",
                color: "var(--text-muted)",
                cursor: "pointer",
                textDecoration: "underline"
              }}
            >
              Clear
            </button>
          </div>

          <div style={{ display: "flex", gap: "1rem", marginTop: "0.5rem" }}>
            <button
              onClick={handleDetectAI}
              disabled={detecting || !text.trim()}
              style={{
                flex: 1,
                padding: "0.75rem 1.5rem",
                backgroundColor: "var(--accent-color)",
                color: "#fff",
                border: "none",
                borderRadius: "6px",
                fontSize: "1rem",
                fontWeight: "bold",
                cursor: (detecting || !text.trim()) ? "not-allowed" : "pointer",
                opacity: (detecting || !text.trim()) ? 0.7 : 1,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                gap: "0.5rem",
                transition: "opacity 0.2s"
              }}
            >
              {detecting ? "Analyzing..." : "🔍 Detect AI"}
            </button>
            <button
              onClick={handleHumanize}
              disabled={humanizing || !text.trim()}
              style={{
                flex: 1,
                padding: "0.75rem 1.5rem",
                backgroundColor: "var(--success-color)",
                color: "#111827",
                border: "none",
                borderRadius: "6px",
                fontSize: "1rem",
                fontWeight: "bold",
                cursor: (humanizing || !text.trim()) ? "not-allowed" : "pointer",
                opacity: (humanizing || !text.trim()) ? 0.7 : 1,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                gap: "0.5rem",
                transition: "opacity 0.2s"
              }}
            >
              {humanizing ? "Humanizing..." : "✨ Humanize"}
            </button>
          </div>

          {error && (
            <div style={{
              backgroundColor: "rgba(239, 68, 68, 0.1)",
              border: "1px solid #ef4444",
              color: "#f87171",
              padding: "1rem",
              borderRadius: "6px",
              marginTop: "1rem"
            }}>
              {error}
            </div>
          )}
        </section>

        {/* Right Panel */}
        <section style={{
          flex: "1 1 500px",
          display: "flex",
          flexDirection: "column",
          gap: "2rem"
        }}>
          {!aiReport && !revisionResult && !detecting && !humanizing && (
            <div style={{
              flex: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              border: "2px dashed var(--border-color)",
              borderRadius: "8px",
              color: "var(--text-muted)"
            }}>
              <p>Paste text and select an action to see results.</p>
            </div>
          )}

          {aiReport && (
            <div style={{
              backgroundColor: "var(--card-bg)",
              border: "1px solid var(--border-color)",
              borderRadius: "8px",
              padding: "1.5rem",
              display: "flex",
              flexDirection: "column",
              gap: "1.5rem"
            }}>
              <AIScoreGauge 
                score={aiReport.ai_score_percent} 
                verdict={aiReport.verdict} 
                confidence={aiReport.confidence} 
              />

              <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
                <h4 style={{ margin: 0, borderBottom: "1px solid var(--border-color)", paddingBottom: "0.5rem" }}>
                  Signal Breakdown
                </h4>
                {aiReport.signals.map((sig, idx) => (
                  <div key={idx} style={{ display: "flex", flexDirection: "column", gap: "0.25rem" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.875rem" }}>
                      <span>{sig.name} <span style={{ color: "var(--text-muted)" }}>(Weight: {sig.weight})</span></span>
                      <span>{Math.round(sig.sub_score * 100)}%</span>
                    </div>
                    <div style={{
                      height: "8px",
                      backgroundColor: "var(--bg-color)",
                      borderRadius: "4px",
                      overflow: "hidden"
                    }}>
                      <div style={{
                        height: "100%",
                        width: `${sig.sub_score * 100}%`,
                        backgroundColor: sig.sub_score > 0.6 ? "#ef4444" : sig.sub_score > 0.3 ? "#eab308" : "var(--success-color)",
                        transition: "width 0.5s ease-out"
                      }} />
                    </div>
                    <span style={{ fontSize: "0.75rem", color: "var(--text-muted)" }}>{sig.description}</span>
                  </div>
                ))}
              </div>

              <div style={{
                backgroundColor: "rgba(79, 128, 255, 0.1)",
                padding: "1rem",
                borderRadius: "6px",
                fontSize: "0.9rem",
                color: "var(--text-main)",
                borderLeft: "3px solid var(--accent-color)"
              }}>
                {aiReport.summary}
              </div>
            </div>
          )}

          {revisionResult && (
            <div style={{
              backgroundColor: "var(--card-bg)",
              border: "1px solid var(--border-color)",
              borderRadius: "8px",
              padding: "1.5rem",
              display: "flex",
              flexDirection: "column",
              gap: "1.25rem"
            }}>
              {/* Header with Title and Mode Toggle */}
              <div style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                flexWrap: "wrap",
                gap: "0.75rem",
                borderBottom: "1px solid var(--border-color)",
                paddingBottom: "0.75rem"
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
                  <h3 style={{ margin: 0, fontSize: "1.2rem", display: "flex", alignItems: "center", gap: "0.5rem" }}>
                    ✨ Humanized Comparison
                  </h3>
                  <span style={{
                    fontSize: "0.75rem",
                    padding: "0.2rem 0.6rem",
                    borderRadius: "9999px",
                    backgroundColor: "rgba(52, 211, 153, 0.15)",
                    color: "var(--success-color)",
                    fontWeight: 600,
                    border: "1px solid rgba(52, 211, 153, 0.3)"
                  }}>
                    Side-by-Side Live
                  </span>
                </div>

                <div style={{ display: "flex", gap: "0.4rem", backgroundColor: "#12151f", padding: "0.25rem", borderRadius: "6px", border: "1px solid var(--border-color)" }}>
                  <button
                    onClick={() => setDiffViewMode("side-by-side")}
                    style={{
                      padding: "0.3rem 0.65rem",
                      fontSize: "0.8rem",
                      borderRadius: "4px",
                      border: "none",
                      backgroundColor: diffViewMode === "side-by-side" ? "var(--accent-color)" : "transparent",
                      color: diffViewMode === "side-by-side" ? "#fff" : "var(--text-muted)",
                      cursor: "pointer",
                      fontWeight: diffViewMode === "side-by-side" ? 600 : 400,
                    }}
                  >
                    Side-by-Side Diff
                  </button>
                  <button
                    onClick={() => setDiffViewMode("raw")}
                    style={{
                      padding: "0.3rem 0.65rem",
                      fontSize: "0.8rem",
                      borderRadius: "4px",
                      border: "none",
                      backgroundColor: diffViewMode === "raw" ? "var(--accent-color)" : "transparent",
                      color: diffViewMode === "raw" ? "#fff" : "var(--text-muted)",
                      cursor: "pointer",
                      fontWeight: diffViewMode === "raw" ? 600 : 400,
                    }}
                  >
                    Clean View
                  </button>
                </div>
              </div>

              {/* AI Score Shift Impact Pill (if available) */}
              {(aiReport || revisedAiReport) && (
                <div style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "0.75rem 1rem",
                  borderRadius: "6px",
                  backgroundColor: "rgba(52, 211, 153, 0.08)",
                  border: "1px solid rgba(52, 211, 153, 0.25)",
                  fontSize: "0.85rem",
                  flexWrap: "wrap",
                  gap: "0.5rem"
                }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
                    <span style={{ color: "var(--text-muted)" }}>AI Probability:</span>
                    {aiReport && (
                      <span style={{ fontWeight: 600, color: aiReport.ai_score_percent > 60 ? "#ef4444" : "#eab308" }}>
                        {aiReport.ai_score_percent}% (Original)
                      </span>
                    )}
                    <span>&rarr;</span>
                    {revisedAiReport ? (
                      <span style={{ fontWeight: 700, color: "var(--success-color)", fontSize: "0.95rem" }}>
                        {revisedAiReport.ai_score_percent}% ({revisedAiReport.verdict})
                      </span>
                    ) : (
                      <span style={{ color: "var(--text-muted)", fontStyle: "italic" }}>Calculating...</span>
                    )}
                  </div>
                  {aiReport && revisedAiReport && aiReport.ai_score_percent > revisedAiReport.ai_score_percent && (
                    <span style={{
                      fontSize: "0.75rem",
                      color: "var(--success-color)",
                      fontWeight: 600,
                    }}>
                      &darr; {aiReport.ai_score_percent - revisedAiReport.ai_score_percent}% reduction in AI predictability
                    </span>
                  )}
                </div>
              )}

              {/* Content Comparison View */}
              {diffViewMode === "side-by-side" ? (
                <DiffViewer
                  originalText={revisionResult.original_text}
                  revisedText={revisionResult.revised_text}
                />
              ) : (
                <div style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
                  gap: "1rem"
                }}>
                  <div style={{
                    backgroundColor: "var(--bg-color)",
                    padding: "1rem",
                    borderRadius: "6px",
                    border: "1px solid var(--border-color)",
                    fontSize: "0.95rem",
                    lineHeight: "1.6",
                    color: "var(--text-muted)",
                    maxHeight: "360px",
                    overflowY: "auto",
                  }}>
                    <div style={{ marginBottom: "0.5rem", fontWeight: 700, fontSize: "0.75rem", textTransform: "uppercase", color: "var(--text-muted)" }}>
                      Original Text
                    </div>
                    {revisionResult.original_text}
                  </div>

                  <div style={{
                    backgroundColor: "rgba(52, 211, 153, 0.05)",
                    padding: "1rem",
                    borderRadius: "6px",
                    border: "1px solid var(--success-color)",
                    fontSize: "0.95rem",
                    lineHeight: "1.6",
                    color: "var(--text-main)",
                    maxHeight: "360px",
                    overflowY: "auto",
                  }}>
                    <div style={{ marginBottom: "0.5rem", fontWeight: 700, fontSize: "0.75rem", textTransform: "uppercase", color: "var(--success-color)" }}>
                      Humanized Text
                    </div>
                    {revisionResult.revised_text}
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div style={{ display: "flex", gap: "1rem", marginTop: "0.25rem" }}>
                <button
                  onClick={handleCopy}
                  style={{
                    flex: 1,
                    padding: "0.6rem",
                    backgroundColor: copied ? "rgba(52, 211, 153, 0.2)" : "transparent",
                    color: copied ? "var(--success-color)" : "var(--text-main)",
                    border: copied ? "1px solid var(--success-color)" : "1px solid var(--border-color)",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontSize: "0.9rem",
                    fontWeight: 600,
                    transition: "all 0.2s"
                  }}
                >
                  {copied ? "✓ Copied to Clipboard!" : "📋 Copy Humanized Text"}
                </button>
                <button
                  onClick={handleUseRevised}
                  style={{
                    flex: 1,
                    padding: "0.6rem",
                    backgroundColor: "var(--accent-color)",
                    color: "#fff",
                    border: "none",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontSize: "0.9rem",
                    fontWeight: 600,
                  }}
                >
                  ↖️ Use as Main Input
                </button>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
