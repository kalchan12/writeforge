"use client";

import React, { useState } from "react";
import {
  AuthorProfile,
  RevisionExecutionResult,
  RevisionPlan,
} from "../types/api";
import { planRevision, executeRevision } from "../lib/api";

interface RevisionPanelProps {
  currentText: string;
  activeProfile: AuthorProfile | null;
  onApplyRevisedText: (text: string) => void;
}

export function RevisionPanel({
  currentText,
  activeProfile,
  onApplyRevisedText,
}: RevisionPanelProps) {
  const [plan, setPlan] = useState<RevisionPlan | null>(null);
  const [executionResult, setExecutionResult] =
    useState<RevisionExecutionResult | null>(null);
  const [isPlanning, setIsPlanning] = useState(false);
  const [isExecuting, setIsExecuting] = useState(false);
  const [useMock, setUseMock] = useState(true);
  const [model, setModel] = useState("llama3");
  const [endpointUrl, setEndpointUrl] = useState("http://localhost:11434");
  const [error, setError] = useState<string | null>(null);

  const handleGeneratePlan = async () => {
    if (!currentText.trim()) {
      setError("Document text is empty. Enter text in the editor to formulate revision plan.");
      return;
    }
    setError(null);
    setIsPlanning(true);
    try {
      const generatedPlan = await planRevision(currentText, activeProfile);
      setPlan(generatedPlan);
      setExecutionResult(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to generate revision plan");
    } finally {
      setIsPlanning(false);
    }
  };

  const handleExecuteRevision = async () => {
    if (!currentText.trim()) {
      setError("Document text is empty.");
      return;
    }
    setError(null);
    setIsExecuting(true);
    try {
      const result = await executeRevision(currentText, {
        profile: activeProfile,
        model,
        endpointUrl,
        useMock,
        outlierThreshold: 2.0,
      });
      setExecutionResult(result);
      if (result.plan) {
        setPlan(result.plan);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Revision execution failed");
    } finally {
      setIsExecuting(false);
    }
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: "1.5rem",
      }}
    >
      {/* 1. Header & Actions */}
      <div
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
          <div>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 600 }}>
              Controlled Stylistic Revision Workbench
            </h3>
            <p style={{ fontSize: "0.85rem", color: "var(--text-muted, #9aa0a6)" }}>
              {activeProfile
                ? `Conditioned against target author "${activeProfile.author_name}"`
                : "Rule-governed diagnostic targets and cadence adjustments"}
            </p>
          </div>

          <div style={{ display: "flex", gap: "0.5rem" }}>
            <button
              onClick={handleGeneratePlan}
              disabled={isPlanning}
              style={{
                backgroundColor: "#2d3345",
                color: "#e2e8f0",
                border: "1px solid #4a5568",
                borderRadius: "6px",
                padding: "0.5rem 1rem",
                fontWeight: 600,
                fontSize: "0.85rem",
                cursor: isPlanning ? "not-allowed" : "pointer",
              }}
            >
              {isPlanning ? "Analyzing..." : "Diagnose Revision Plan"}
            </button>

            <button
              onClick={handleExecuteRevision}
              disabled={isExecuting}
              style={{
                backgroundColor: "#4f80ff",
                color: "#ffffff",
                border: "none",
                borderRadius: "6px",
                padding: "0.5rem 1.25rem",
                fontWeight: 600,
                fontSize: "0.85rem",
                cursor: isExecuting ? "not-allowed" : "pointer",
              }}
            >
              {isExecuting ? "Executing Revision..." : "Execute Controlled Revision"}
            </button>
          </div>
        </div>

        {/* Inference Options Bar */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "1rem",
            backgroundColor: "#12151f",
            borderRadius: "6px",
            padding: "0.6rem 0.85rem",
            fontSize: "0.8rem",
            color: "var(--text-muted, #9aa0a6)",
          }}
        >
          <label style={{ display: "flex", alignItems: "center", gap: "0.4rem", cursor: "pointer" }}>
            <input
              type="checkbox"
              checked={useMock}
              onChange={(e) => setUseMock(e.target.checked)}
            />
            <span style={{ color: "#f0f2f5" }}>Deterministic Mock Mode</span> (Offline / CI)
          </label>

          {!useMock && (
            <>
              <div style={{ display: "flex", alignItems: "center", gap: "0.35rem" }}>
                <span>Model:</span>
                <input
                  type="text"
                  value={model}
                  onChange={(e) => setModel(e.target.value)}
                  style={{
                    backgroundColor: "#1a1d27",
                    border: "1px solid #2d3345",
                    borderRadius: "4px",
                    padding: "0.2rem 0.5rem",
                    color: "#f0f2f5",
                    fontSize: "0.8rem",
                    width: "90px",
                  }}
                />
              </div>

              <div style={{ display: "flex", alignItems: "center", gap: "0.35rem" }}>
                <span>Host:</span>
                <input
                  type="text"
                  value={endpointUrl}
                  onChange={(e) => setEndpointUrl(e.target.value)}
                  style={{
                    backgroundColor: "#1a1d27",
                    border: "1px solid #2d3345",
                    borderRadius: "4px",
                    padding: "0.2rem 0.5rem",
                    color: "#f0f2f5",
                    fontSize: "0.8rem",
                    width: "160px",
                  }}
                />
              </div>
            </>
          )}
        </div>

        {error && (
          <div
            style={{
              padding: "0.5rem 0.75rem",
              borderRadius: "4px",
              backgroundColor: "#7f1d1d33",
              border: "1px solid #f87171",
              color: "#f87171",
              fontSize: "0.85rem",
            }}
          >
            {error}
          </div>
        )}
      </div>

      {/* 2. Revision Execution Results (Diff & Verification) */}
      {executionResult && (
        <div
          style={{
            backgroundColor: "var(--card-bg, #1a1d27)",
            border: "1px solid var(--border-color, #2d3345)",
            borderRadius: "8px",
            padding: "1.25rem",
            display: "flex",
            flexDirection: "column",
            gap: "1.25rem",
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
            <div style={{ display: "flex", alignItems: "center", gap: "0.6rem" }}>
              <span
                style={{
                  fontSize: "0.75rem",
                  padding: "0.2rem 0.6rem",
                  borderRadius: "9999px",
                  backgroundColor: executionResult.success ? "#064e3b" : "#7f1d1d",
                  color: executionResult.success ? "#34d399" : "#f87171",
                  fontWeight: 600,
                }}
              >
                {executionResult.success ? "REVISION COMPLETE" : "EXECUTION FAILED"}
              </span>
              <h4 style={{ fontSize: "1rem", fontWeight: 600 }}>
                Controlled Transformation Output
              </h4>
            </div>

            {executionResult.success && (
              <button
                onClick={() => onApplyRevisedText(executionResult.revised_text)}
                style={{
                  backgroundColor: "#34d399",
                  color: "#0f1117",
                  border: "none",
                  borderRadius: "4px",
                  padding: "0.4rem 0.85rem",
                  fontWeight: 600,
                  fontSize: "0.8rem",
                  cursor: "pointer",
                }}
              >
                Apply Revised Text to Editor
              </button>
            )}
          </div>

          {executionResult.error_message && (
            <div
              style={{
                padding: "0.6rem",
                borderRadius: "4px",
                backgroundColor: "#7f1d1d33",
                color: "#f87171",
                fontSize: "0.85rem",
              }}
            >
              {executionResult.error_message}
            </div>
          )}

          {/* Side-by-Side Comparison */}
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
            <div
              style={{
                backgroundColor: "#12151f",
                border: "1px solid var(--border-color, #2d3345)",
                borderRadius: "6px",
                padding: "0.85rem",
              }}
            >
              <div
                style={{
                  fontSize: "0.75rem",
                  fontWeight: 600,
                  color: "var(--text-muted, #9aa0a6)",
                  marginBottom: "0.5rem",
                  textTransform: "uppercase",
                }}
              >
                Original Text
              </div>
              <p style={{ fontSize: "0.85rem", lineHeight: 1.5, color: "#f0f2f5" }}>
                {executionResult.original_text}
              </p>
            </div>

            <div
              style={{
                backgroundColor: "#12151f",
                border: "1px solid #34d39944",
                borderRadius: "6px",
                padding: "0.85rem",
              }}
            >
              <div
                style={{
                  fontSize: "0.75rem",
                  fontWeight: 600,
                  color: "#34d399",
                  marginBottom: "0.5rem",
                  textTransform: "uppercase",
                }}
              >
                Revised Candidate
              </div>
              <p style={{ fontSize: "0.85rem", lineHeight: 1.5, color: "#f0f2f5" }}>
                {executionResult.revised_text}
              </p>
            </div>
          </div>

          {/* Metric Shifts Comparison */}
          <div
            style={{
              backgroundColor: "#12151f",
              borderRadius: "6px",
              padding: "0.75rem",
              fontSize: "0.8rem",
            }}
          >
            <div
              style={{
                fontWeight: 600,
                color: "var(--text-muted, #9aa0a6)",
                marginBottom: "0.5rem",
              }}
            >
              Metric Shifts & Fidelity Verification:
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                gap: "0.75rem",
              }}
            >
              {Object.keys(executionResult.metrics_before).map((k) => (
                <div key={k} style={{ borderLeft: "2px solid #2d3345", paddingLeft: "0.5rem" }}>
                  <span style={{ fontSize: "0.7rem", color: "var(--text-muted, #9aa0a6)" }}>
                    {k.replace(/_/g, " ")}
                  </span>
                  <div style={{ fontWeight: 600 }}>
                    {executionResult.metrics_before[k]?.toFixed(1)} &rarr;{" "}
                    <span style={{ color: "#60a5fa" }}>
                      {executionResult.metrics_after[k]?.toFixed(1) ?? "—"}
                    </span>
                  </div>
                </div>
              ))}

              {executionResult.consistency_before !== null &&
                executionResult.consistency_before !== undefined && (
                  <div style={{ borderLeft: "2px solid #34d399", paddingLeft: "0.5rem" }}>
                    <span style={{ fontSize: "0.7rem", color: "var(--text-muted, #9aa0a6)" }}>
                      Consistency Score
                    </span>
                    <div style={{ fontWeight: 600, color: "#34d399" }}>
                      {(executionResult.consistency_before * 100).toFixed(1)}% &rarr;{" "}
                      {((executionResult.consistency_after ?? 0) * 100).toFixed(1)}%
                    </div>
                  </div>
                )}
            </div>
          </div>
        </div>
      )}

      {/* 3. Diagnostic Plan Details (Goals & Sentence Targets) */}
      {plan && (
        <div
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
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h4 style={{ fontSize: "1rem", fontWeight: 600 }}>
              Diagnostic Strategy Summary
            </h4>
            <span style={{ fontSize: "0.8rem", color: "var(--text-muted, #9aa0a6)" }}>
              {plan.total_suggestions} target intervention(s)
            </span>
          </div>

          <p style={{ fontSize: "0.85rem", color: "var(--text-muted, #9aa0a6)" }}>
            {plan.summary}
          </p>

          {/* Goals */}
          {plan.goals.length > 0 && (
            <div>
              <span
                style={{
                  fontSize: "0.75rem",
                  fontWeight: 600,
                  color: "var(--text-muted, #9aa0a6)",
                  textTransform: "uppercase",
                  letterSpacing: "0.04em",
                }}
              >
                Global Directional Goals
              </span>
              <div
                style={{
                  marginTop: "0.5rem",
                  display: "flex",
                  flexDirection: "column",
                  gap: "0.4rem",
                }}
              >
                {plan.goals.map((g, idx) => (
                  <div
                    key={idx}
                    style={{
                      backgroundColor: "#12151f",
                      borderRadius: "4px",
                      padding: "0.5rem 0.75rem",
                      fontSize: "0.8rem",
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                    }}
                  >
                    <div>
                      <strong>{g.metric_name}</strong>: {g.description}
                    </div>
                    <span
                      style={{
                        padding: "0.15rem 0.5rem",
                        borderRadius: "4px",
                        fontSize: "0.7rem",
                        fontWeight: 600,
                        backgroundColor:
                          g.direction === "increase"
                            ? "#064e3b"
                            : g.direction === "decrease"
                            ? "#78350f"
                            : "#1e3a8a",
                        color:
                          g.direction === "increase"
                            ? "#34d399"
                            : g.direction === "decrease"
                            ? "#fbbf24"
                            : "#60a5fa",
                      }}
                    >
                      {g.direction.toUpperCase()} TO ~{g.target_value}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Sentence-Level Targets */}
          {plan.sentence_targets.length > 0 && (
            <div>
              <span
                style={{
                  fontSize: "0.75rem",
                  fontWeight: 600,
                  color: "var(--text-muted, #9aa0a6)",
                  textTransform: "uppercase",
                  letterSpacing: "0.04em",
                }}
              >
                Granular Sentence Diagnoses
              </span>
              <div
                style={{
                  marginTop: "0.5rem",
                  display: "flex",
                  flexDirection: "column",
                  gap: "0.5rem",
                }}
              >
                {plan.sentence_targets.map((t, idx) => (
                  <div
                    key={idx}
                    style={{
                      backgroundColor: "#12151f",
                      border: "1px solid var(--border-color, #2d3345)",
                      borderRadius: "6px",
                      padding: "0.75rem",
                      fontSize: "0.8rem",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        marginBottom: "0.3rem",
                      }}
                    >
                      <span style={{ fontWeight: 600, color: "#60a5fa" }}>
                        Sentence {t.sentence_index + 1} &bull;{" "}
                        {t.issue_type.replace(/_/g, " ").toUpperCase()}
                      </span>
                      <span
                        style={{
                          fontSize: "0.7rem",
                          color:
                            t.priority === 1
                              ? "#f87171"
                              : t.priority === 2
                              ? "#fbbf24"
                              : "var(--text-muted, #9aa0a6)",
                        }}
                      >
                        Priority {t.priority}
                      </span>
                    </div>

                    <div
                      style={{
                        color: "var(--text-muted, #9aa0a6)",
                        fontStyle: "italic",
                        marginBottom: "0.35rem",
                      }}
                    >
                      &ldquo;{t.original_text}&rdquo;
                    </div>

                    <div style={{ color: "#34d399", fontWeight: 500 }}>
                      &rarr; {t.suggestion}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
