"use client";

import React, { useState, useEffect } from "react";
import AIScoreGauge from "../components/AIScoreGauge";
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
      const result = await executeRevision(text, { useMock: true });
      setRevisionResult(result);
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
      setAiReport(null); // Optional: clear AI report since text changed
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
              onClick={() => { setText(""); setAiReport(null); setRevisionResult(null); }}
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
              gap: "1rem"
            }}>
              <h3 style={{ margin: 0, display: "flex", alignItems: "center", gap: "0.5rem" }}>
                ✨ Humanized Text
              </h3>
              
              <div style={{
                backgroundColor: "var(--bg-color)",
                padding: "1rem",
                borderRadius: "6px",
                color: "var(--text-muted)",
                fontSize: "0.9rem",
                border: "1px solid var(--border-color)",
                opacity: 0.7
              }}>
                <div style={{ marginBottom: "0.5rem", fontWeight: "bold", fontSize: "0.8rem", textTransform: "uppercase" }}>Original</div>
                {revisionResult.original_text}
              </div>

              <div style={{
                backgroundColor: "rgba(52, 211, 153, 0.05)",
                padding: "1rem",
                borderRadius: "6px",
                color: "var(--text-main)",
                fontSize: "1rem",
                lineHeight: "1.5",
                border: "1px solid var(--success-color)"
              }}>
                <div style={{ marginBottom: "0.5rem", fontWeight: "bold", fontSize: "0.8rem", color: "var(--success-color)", textTransform: "uppercase" }}>Revised</div>
                {revisionResult.revised_text}
              </div>

              <div style={{ display: "flex", gap: "1rem", marginTop: "0.5rem" }}>
                <button
                  onClick={handleCopy}
                  style={{
                    flex: 1,
                    padding: "0.5rem",
                    backgroundColor: copied ? "rgba(52, 211, 153, 0.2)" : "transparent",
                    color: copied ? "var(--success-color)" : "var(--text-main)",
                    border: copied ? "1px solid var(--success-color)" : "1px solid var(--border-color)",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontSize: "0.9rem",
                    transition: "all 0.2s"
                  }}
                >
                  {copied ? "✓ Copied!" : "📋 Copy Text"}
                </button>
                <button
                  onClick={handleUseRevised}
                  style={{
                    flex: 1,
                    padding: "0.5rem",
                    backgroundColor: "var(--accent-color)",
                    color: "#fff",
                    border: "none",
                    borderRadius: "6px",
                    cursor: "pointer",
                    fontSize: "0.9rem"
                  }}
                >
                  ↖️ Use as Input
                </button>
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
