"use client";

import React, { useState } from "react";
import { AuthorProfile, ConsistencyReport } from "../types/api";
import { createProfile, compareProfile } from "../lib/api";

interface ProfilePanelProps {
  currentText: string;
  activeProfile: AuthorProfile | null;
  onProfileSelect: (profile: AuthorProfile | null) => void;
}

export function ProfilePanel({
  currentText,
  activeProfile,
  onProfileSelect,
}: ProfilePanelProps) {
  const [authorName, setAuthorName] = useState("Ernest Hemingway");
  const [doc1, setDoc1] = useState(
    "The sun rose over the hills. The water was cold and clear in the morning."
  );
  const [doc2, setDoc2] = useState(
    "He walked down the dusty road alone. The wind came hard from the north."
  );
  const [isCreating, setIsCreating] = useState(false);
  const [isComparing, setIsComparing] = useState(false);
  const [comparisonReport, setComparisonReport] =
    useState<ConsistencyReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCreateProfile = async () => {
    if (!authorName.trim() || !doc1.trim()) {
      setError("Please provide an author name and at least one sample document.");
      return;
    }
    setError(null);
    setIsCreating(true);
    try {
      const docs = [{ text: doc1.trim() }];
      if (doc2.trim()) {
        docs.push({ text: doc2.trim() });
      }
      const profile = await createProfile(authorName.trim(), docs);
      onProfileSelect(profile);
      setComparisonReport(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to create profile");
    } finally {
      setIsCreating(false);
    }
  };

  const handleCompare = async () => {
    if (!activeProfile) {
      setError("No active profile to compare against. Create or select a profile first.");
      return;
    }
    if (!currentText.trim()) {
      setError("Current document text is empty. Enter text in the editor to compare.");
      return;
    }
    setError(null);
    setIsComparing(true);
    try {
      const report = await compareProfile(currentText, activeProfile, 2.0);
      setComparisonReport(report);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to evaluate profile consistency");
    } finally {
      setIsComparing(false);
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
      {/* 1. Profile Manager Header */}
      <div
        style={{
          backgroundColor: "var(--card-bg, #1a1d27)",
          border: "1px solid var(--border-color, #2d3345)",
          borderRadius: "8px",
          padding: "1.25rem",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 600 }}>
              Author Profile Signature
            </h3>
            <p style={{ fontSize: "0.85rem", color: "var(--text-muted, #9aa0a6)" }}>
              Aggregates stylometric baselines across author documents for consistency scoring
            </p>
          </div>
          {activeProfile && (
            <button
              onClick={() => onProfileSelect(null)}
              style={{
                background: "none",
                border: "1px solid var(--border-color, #2d3345)",
                color: "var(--text-muted, #9aa0a6)",
                borderRadius: "4px",
                padding: "0.3rem 0.65rem",
                fontSize: "0.75rem",
                cursor: "pointer",
              }}
            >
              Clear Active Profile
            </button>
          )}
        </div>

        {activeProfile ? (
          <div
            style={{
              marginTop: "1rem",
              padding: "0.75rem 1rem",
              borderRadius: "6px",
              backgroundColor: "#12151f",
              border: "1px solid #34d39944",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: "0.5rem",
            }}
          >
            <div>
              <span style={{ fontSize: "0.75rem", color: "var(--text-muted, #9aa0a6)" }}>
                Active Profile Target
              </span>
              <div style={{ fontSize: "1.1rem", fontWeight: 700, color: "#34d399" }}>
                {activeProfile.author_name}
              </div>
              <span style={{ fontSize: "0.8rem", color: "var(--text-muted, #9aa0a6)" }}>
                {activeProfile.document_count} document(s) &bull;{" "}
                {Object.keys(activeProfile.baselines).length} baselines established
              </span>
            </div>

            <button
              onClick={handleCompare}
              disabled={isComparing}
              style={{
                backgroundColor: "#4f80ff",
                color: "#ffffff",
                border: "none",
                borderRadius: "6px",
                padding: "0.6rem 1.25rem",
                fontWeight: 600,
                fontSize: "0.9rem",
                cursor: isComparing ? "not-allowed" : "pointer",
              }}
            >
              {isComparing ? "Evaluating..." : "Compare Current Text Against Profile"}
            </button>
          </div>
        ) : (
          <div
            style={{
              marginTop: "1rem",
              display: "flex",
              flexDirection: "column",
              gap: "0.75rem",
            }}
          >
            <div style={{ display: "flex", flexDirection: "column", gap: "0.3rem" }}>
              <label style={{ fontSize: "0.8rem", color: "var(--text-muted, #9aa0a6)" }}>
                Author Identifier / Name:
              </label>
              <input
                type="text"
                value={authorName}
                onChange={(e) => setAuthorName(e.target.value)}
                style={{
                  backgroundColor: "#12151f",
                  border: "1px solid var(--border-color, #2d3345)",
                  borderRadius: "6px",
                  padding: "0.5rem 0.75rem",
                  color: "#f0f2f5",
                  fontSize: "0.9rem",
                }}
              />
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "0.75rem" }}>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.3rem" }}>
                <label style={{ fontSize: "0.75rem", color: "var(--text-muted, #9aa0a6)" }}>
                  Sample Document 1:
                </label>
                <textarea
                  rows={3}
                  value={doc1}
                  onChange={(e) => setDoc1(e.target.value)}
                  style={{
                    backgroundColor: "#12151f",
                    border: "1px solid var(--border-color, #2d3345)",
                    borderRadius: "6px",
                    padding: "0.5rem",
                    color: "#f0f2f5",
                    fontSize: "0.85rem",
                    fontFamily: "inherit",
                  }}
                />
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: "0.3rem" }}>
                <label style={{ fontSize: "0.75rem", color: "var(--text-muted, #9aa0a6)" }}>
                  Sample Document 2 (optional):
                </label>
                <textarea
                  rows={3}
                  value={doc2}
                  onChange={(e) => setDoc2(e.target.value)}
                  style={{
                    backgroundColor: "#12151f",
                    border: "1px solid var(--border-color, #2d3345)",
                    borderRadius: "6px",
                    padding: "0.5rem",
                    color: "#f0f2f5",
                    fontSize: "0.85rem",
                    fontFamily: "inherit",
                  }}
                />
              </div>
            </div>

            <button
              onClick={handleCreateProfile}
              disabled={isCreating}
              style={{
                alignSelf: "flex-start",
                backgroundColor: "#34d399",
                color: "#0f1117",
                border: "none",
                borderRadius: "6px",
                padding: "0.5rem 1rem",
                fontWeight: 600,
                fontSize: "0.85rem",
                cursor: isCreating ? "not-allowed" : "pointer",
              }}
            >
              {isCreating ? "Constructing Profile..." : "Create & Activate Profile"}
            </button>
          </div>
        )}

        {error && (
          <div
            style={{
              marginTop: "0.75rem",
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

      {/* 2. Comparison Report Display */}
      {comparisonReport && (
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
              <h4 style={{ fontSize: "1rem", fontWeight: 600 }}>
                Stylistic Consistency Assessment
              </h4>
              <p style={{ fontSize: "0.8rem", color: "var(--text-muted, #9aa0a6)" }}>
                Evaluated against &ldquo;{comparisonReport.author_name}&rdquo;
              </p>
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
              <div style={{ textAlign: "right" }}>
                <span style={{ fontSize: "0.75rem", color: "var(--text-muted, #9aa0a6)" }}>
                  Consistency Score
                </span>
                <div
                  style={{
                    fontSize: "1.4rem",
                    fontWeight: 700,
                    color:
                      comparisonReport.consistency_score >= 0.75
                        ? "#34d399"
                        : comparisonReport.consistency_score >= 0.5
                        ? "#fbbf24"
                        : "#f87171",
                  }}
                >
                  {(comparisonReport.consistency_score * 100).toFixed(1)}%
                </div>
              </div>

              <span
                style={{
                  fontSize: "0.75rem",
                  padding: "0.2rem 0.6rem",
                  borderRadius: "9999px",
                  backgroundColor:
                    comparisonReport.outlier_count === 0 ? "#064e3b" : "#7f1d1d",
                  color: comparisonReport.outlier_count === 0 ? "#34d399" : "#f87171",
                  fontWeight: 600,
                }}
              >
                {comparisonReport.outlier_count} Outlier(s)
              </span>
            </div>
          </div>

          <p style={{ fontSize: "0.85rem", color: "var(--text-muted, #9aa0a6)" }}>
            {comparisonReport.summary}
          </p>

          {/* Deviations Table */}
          <div style={{ overflowX: "auto" }}>
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                fontSize: "0.8rem",
                textAlign: "left",
              }}
            >
              <thead>
                <tr
                  style={{
                    borderBottom: "1px solid var(--border-color, #2d3345)",
                    color: "var(--text-muted, #9aa0a6)",
                  }}
                >
                  <th style={{ padding: "0.5rem" }}>Metric</th>
                  <th style={{ padding: "0.5rem" }}>Observed</th>
                  <th style={{ padding: "0.5rem" }}>Expected (Mean &plusmn; &sigma;)</th>
                  <th style={{ padding: "0.5rem" }}>Z-Score</th>
                  <th style={{ padding: "0.5rem" }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {Object.values(comparisonReport.deviations).map((dev) => (
                  <tr
                    key={dev.metric_name}
                    style={{
                      borderBottom: "1px solid #222634",
                      backgroundColor: dev.is_outlier ? "#7f1d1d18" : "transparent",
                    }}
                  >
                    <td style={{ padding: "0.5rem", fontWeight: 500 }}>
                      {dev.metric_name}
                    </td>
                    <td style={{ padding: "0.5rem", fontFeatureSettings: '"tnum"' }}>
                      {dev.observed_value.toFixed(2)}
                    </td>
                    <td style={{ padding: "0.5rem", color: "var(--text-muted, #9aa0a6)" }}>
                      {dev.baseline_mean.toFixed(2)} &plusmn; {dev.baseline_std_dev.toFixed(2)}
                    </td>
                    <td
                      style={{
                        padding: "0.5rem",
                        fontWeight: 600,
                        color:
                          dev.z_score > 0
                            ? "#fbbf24"
                            : dev.z_score < 0
                            ? "#60a5fa"
                            : "inherit",
                      }}
                    >
                      {dev.z_score > 0 ? `+${dev.z_score.toFixed(2)}` : dev.z_score.toFixed(2)}
                    </td>
                    <td style={{ padding: "0.5rem" }}>
                      <span
                        style={{
                          fontSize: "0.7rem",
                          padding: "0.1rem 0.4rem",
                          borderRadius: "4px",
                          backgroundColor: dev.is_outlier ? "#7f1d1d" : "#064e3b",
                          color: dev.is_outlier ? "#f87171" : "#34d399",
                          fontWeight: 500,
                        }}
                      >
                        {dev.is_outlier ? "OUTLIER" : "ALIGNED"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
