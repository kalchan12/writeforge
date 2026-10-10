"use client";

import React, { useMemo } from "react";

interface DiffViewerProps {
  originalText: string;
  revisedText: string;
}

interface DiffToken {
  type: "same" | "added" | "removed";
  value: string;
}

// LCS-based word-level diff implementation without external dependencies
function computeWordDiff(orig: string, rev: string): { originalTokens: DiffToken[]; revisedTokens: DiffToken[] } {
  // Tokenize preserving whitespaces and punctuation
  const tokenRegex = /(\s+|[^\s\w]+|\w+)/g;
  const origTokens = orig.match(tokenRegex) || [];
  const revTokens = rev.match(tokenRegex) || [];

  const m = origTokens.length;
  const n = revTokens.length;

  // Build LCS table (capped size safeguard for very large texts)
  if (m * n > 400000) {
    return {
      originalTokens: origTokens.map((t) => ({ type: "same", value: t })),
      revisedTokens: revTokens.map((t) => ({ type: "same", value: t })),
    };
  }

  const dp: number[][] = Array.from({ length: m + 1 }, () => new Uint16Array(n + 1) as unknown as number[]);

  for (let i = 0; i < m; i++) {
    for (let j = 0; j < n; j++) {
      if (origTokens[i] === revTokens[j]) {
        dp[i + 1][j + 1] = dp[i][j] + 1;
      } else {
        dp[i + 1][j + 1] = Math.max(dp[i + 1][j], dp[i][j + 1]);
      }
    }
  }

  let i = m;
  let j = n;
  const origDiff: DiffToken[] = [];
  const revDiff: DiffToken[] = [];

  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && origTokens[i - 1] === revTokens[j - 1]) {
      origDiff.push({ type: "same", value: origTokens[i - 1] });
      revDiff.push({ type: "same", value: revTokens[j - 1] });
      i--;
      j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      revDiff.push({ type: "added", value: revTokens[j - 1] });
      j--;
    } else if (i > 0 && (j === 0 || dp[i][j - 1] < dp[i - 1][j])) {
      origDiff.push({ type: "removed", value: origTokens[i - 1] });
      i--;
    }
  }

  return {
    originalTokens: origDiff.reverse(),
    revisedTokens: revDiff.reverse(),
  };
}

export default function DiffViewer({ originalText, revisedText }: DiffViewerProps) {
  const { originalTokens, revisedTokens } = useMemo(
    () => computeWordDiff(originalText, revisedText),
    [originalText, revisedText]
  );

  const stats = useMemo(() => {
    const origWords = originalText.trim() ? originalText.trim().split(/\s+/).length : 0;
    const revWords = revisedText.trim() ? revisedText.trim().split(/\s+/).length : 0;
    const addedCount = revisedTokens.filter((t) => t.type === "added" && /\w+/.test(t.value)).length;
    const removedCount = originalTokens.filter((t) => t.type === "removed" && /\w+/.test(t.value)).length;
    return { origWords, revWords, addedCount, removedCount };
  }, [originalText, revisedText, originalTokens, revisedTokens]);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
      {/* Legend & Stats Banner */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "0.5rem",
          padding: "0.5rem 0.75rem",
          backgroundColor: "#12151f",
          border: "1px solid var(--border-color)",
          borderRadius: "6px",
          fontSize: "0.8rem",
          color: "var(--text-muted)",
        }}
      >
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "2px",
                backgroundColor: "rgba(239, 68, 68, 0.4)",
                border: "1px solid #ef4444",
                display: "inline-block",
              }}
            />
            Removed ({stats.removedCount} words)
          </span>
          <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "2px",
                backgroundColor: "rgba(52, 211, 153, 0.4)",
                border: "1px solid var(--success-color)",
                display: "inline-block",
              }}
            />
            Added / Enhanced ({stats.addedCount} words)
          </span>
        </div>
        <div>
          Word count: {stats.origWords} &rarr;{" "}
          <span style={{ color: "var(--text-main)", fontWeight: 600 }}>{stats.revWords}</span>
        </div>
      </div>

      {/* Side-by-side comparison columns */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
          gap: "1rem",
        }}
      >
        {/* Left: Original with deletions highlighted */}
        <div
          style={{
            backgroundColor: "#12151f",
            border: "1px solid var(--border-color)",
            borderRadius: "6px",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              padding: "0.5rem 0.75rem",
              backgroundColor: "rgba(255, 255, 255, 0.02)",
              borderBottom: "1px solid var(--border-color)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              fontSize: "0.75rem",
              fontWeight: 600,
              color: "var(--text-muted)",
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            <span>Original Draft</span>
            <span>{stats.origWords} words</span>
          </div>
          <div
            style={{
              padding: "1rem",
              fontSize: "0.95rem",
              lineHeight: "1.7",
              color: "var(--text-main)",
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              maxHeight: "360px",
              overflowY: "auto",
            }}
          >
            {originalTokens.map((tok, idx) => {
              if (tok.type === "removed") {
                return (
                  <mark
                    key={idx}
                    style={{
                      backgroundColor: "rgba(239, 68, 68, 0.25)",
                      color: "#fca5a5",
                      textDecoration: "line-through",
                      borderRadius: "3px",
                      padding: "0 2px",
                    }}
                  >
                    {tok.value}
                  </mark>
                );
              }
              return <span key={idx}>{tok.value}</span>;
            })}
          </div>
        </div>

        {/* Right: Revised with additions highlighted */}
        <div
          style={{
            backgroundColor: "#12151f",
            border: "1px solid rgba(52, 211, 153, 0.4)",
            borderRadius: "6px",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
          }}
        >
          <div
            style={{
              padding: "0.5rem 0.75rem",
              backgroundColor: "rgba(52, 211, 153, 0.08)",
              borderBottom: "1px solid rgba(52, 211, 153, 0.2)",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              fontSize: "0.75rem",
              fontWeight: 600,
              color: "var(--success-color)",
              textTransform: "uppercase",
              letterSpacing: "0.05em",
            }}
          >
            <span>✨ Humanized Candidate</span>
            <span>{stats.revWords} words</span>
          </div>
          <div
            style={{
              padding: "1rem",
              fontSize: "0.95rem",
              lineHeight: "1.7",
              color: "var(--text-main)",
              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
              maxHeight: "360px",
              overflowY: "auto",
            }}
          >
            {revisedTokens.map((tok, idx) => {
              if (tok.type === "added") {
                return (
                  <mark
                    key={idx}
                    style={{
                      backgroundColor: "rgba(52, 211, 153, 0.25)",
                      color: "#6ee7b7",
                      fontWeight: 600,
                      borderRadius: "3px",
                      padding: "0 2px",
                    }}
                  >
                    {tok.value}
                  </mark>
                );
              }
              return <span key={idx}>{tok.value}</span>;
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
