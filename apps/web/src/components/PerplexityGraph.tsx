"use client";

import React, { useState } from "react";
import { PerplexityReport, SentencePerplexity } from "../types/api";

interface PerplexityGraphProps {
  report: PerplexityReport | null;
}

export function PerplexityGraph({ report }: PerplexityGraphProps) {
  const [selectedSentence, setSelectedSentence] =
    useState<SentencePerplexity | null>(null);

  if (!report || report.sentence_perplexities.length === 0) {
    return (
      <div
        style={{
          padding: "2rem",
          textAlign: "center",
          color: "var(--text-muted, #9aa0a6)",
          border: "1px dashed var(--border-color, #2d3345)",
          borderRadius: "8px",
        }}
      >
        No perplexity data available. Analyze a document with multiple sentences to view cadence.
      </div>
    );
  }

  const sentences = report.sentence_perplexities;
  const maxPpl = Math.max(...sentences.map((s) => s.perplexity), 10);
  const minPpl = Math.min(...sentences.map((s) => s.perplexity), 0);

  // SVG dimensions
  const svgWidth = 680;
  const svgHeight = 160;
  const paddingX = 35;
  const paddingY = 25;
  const plotWidth = svgWidth - paddingX * 2;
  const plotHeight = svgHeight - paddingY * 2;

  const points = sentences.map((s, idx) => {
    const x =
      sentences.length === 1
        ? paddingX + plotWidth / 2
        : paddingX + (idx / (sentences.length - 1)) * plotWidth;
    const normalizedY = (s.perplexity - minPpl) / (maxPpl - minPpl || 1);
    const y = svgHeight - paddingY - normalizedY * plotHeight;
    return { x, y, sentence: s };
  });

  const polylineStr = points.map((p) => `${p.x},${p.y}`).join(" ");

  // Burstiness classification badge
  const isHighBurstiness = report.burstiness >= 0.35;
  const isLowBurstiness = report.burstiness < 0.20;

  return (
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
          <h3 style={{ fontSize: "1.05rem", fontWeight: 600 }}>
            Sentence Perplexity & Cadence Trajectory
          </h3>
          <p style={{ fontSize: "0.85rem", color: "var(--text-muted, #9aa0a6)" }}>
            Information-theoretic token probability variation across sentences
          </p>
        </div>

        <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
          <div style={{ textAlign: "right" }}>
            <span style={{ fontSize: "0.75rem", color: "var(--text-muted, #9aa0a6)" }}>
              Burstiness (CV)
            </span>
            <div style={{ fontWeight: 700, fontSize: "1.1rem" }}>
              {report.burstiness.toFixed(3)}
            </div>
          </div>

          <span
            style={{
              padding: "0.25rem 0.65rem",
              borderRadius: "9999px",
              fontSize: "0.75rem",
              fontWeight: 600,
              backgroundColor: isHighBurstiness
                ? "#064e3b"
                : isLowBurstiness
                ? "#7f1d1d"
                : "#1e3a8a",
              color: isHighBurstiness
                ? "#34d399"
                : isLowBurstiness
                ? "#f87171"
                : "#60a5fa",
            }}
          >
            {isHighBurstiness
              ? "High Cadence (Human)"
              : isLowBurstiness
              ? "Uniform (Synthetic)"
              : "Moderate Cadence"}
          </span>
        </div>
      </div>

      {/* SVG Trajectory Chart */}
      <div
        style={{
          width: "100%",
          overflowX: "auto",
          backgroundColor: "#12151f",
          borderRadius: "6px",
          padding: "0.5rem 0",
        }}
      >
        <svg
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          style={{ width: "100%", height: "auto", display: "block" }}
        >
          {/* Grid lines */}
          <line
            x1={paddingX}
            y1={paddingY}
            x2={svgWidth - paddingX}
            y2={paddingY}
            stroke="#2d3345"
            strokeDasharray="4 4"
          />
          <line
            x1={paddingX}
            y1={svgHeight - paddingY}
            x2={svgWidth - paddingX}
            y2={svgHeight - paddingY}
            stroke="#2d3345"
          />

          {/* Polyline curve */}
          {sentences.length > 1 && (
            <polyline
              fill="none"
              stroke="#4f80ff"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={polylineStr}
            />
          )}

          {/* Data Points */}
          {points.map((p, idx) => {
            const isSelected =
              selectedSentence?.sentence_index === p.sentence.sentence_index;
            return (
              <g
                key={idx}
                style={{ cursor: "pointer" }}
                onClick={() => setSelectedSentence(p.sentence)}
              >
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={isSelected ? 6 : 4}
                  fill={isSelected ? "#34d399" : "#4f80ff"}
                  stroke="#ffffff"
                  strokeWidth="1.5"
                />
                <text
                  x={p.x}
                  y={svgHeight - 8}
                  textAnchor="middle"
                  fill="#9aa0a6"
                  fontSize="9"
                >
                  S{idx + 1}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Selected sentence detail card */}
      {selectedSentence ? (
        <div
          style={{
            backgroundColor: "#12151f",
            border: "1px solid var(--border-color, #2d3345)",
            borderRadius: "6px",
            padding: "0.75rem 1rem",
            fontSize: "0.85rem",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginBottom: "0.25rem",
              fontWeight: 600,
            }}
          >
            <span>Sentence {selectedSentence.sentence_index + 1}</span>
            <span style={{ color: "#60a5fa" }}>
              PPL: {selectedSentence.perplexity.toFixed(1)} ({selectedSentence.token_count} words)
            </span>
          </div>
          <p style={{ color: "var(--text-main, #f0f2f5)", fontStyle: "italic" }}>
            &ldquo;{selectedSentence.text}&rdquo;
          </p>
        </div>
      ) : (
        <div style={{ fontSize: "0.8rem", color: "var(--text-muted, #9aa0a6)" }}>
          Click on any point along the curve to inspect sentence-level perplexity and token count.
        </div>
      )}

      {/* Qualitative Summary */}
      <div
        style={{
          fontSize: "0.85rem",
          color: "var(--text-muted, #9aa0a6)",
          borderTop: "1px solid var(--border-color, #2d3345)",
          paddingTop: "0.75rem",
        }}
      >
        <strong>Summary: </strong>
        {report.summary}
      </div>
    </div>
  );
}
