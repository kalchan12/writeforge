"use client";

import React from "react";

interface MetricCardProps {
  label: string;
  value: number | string;
  unit?: string;
  description?: string | null;
  badge?: {
    text: string;
    variant: "neutral" | "success" | "warning" | "danger" | "accent";
  };
}

export function MetricCard({
  label,
  value,
  unit,
  description,
  badge,
}: MetricCardProps) {
  const badgeColors: Record<string, { bg: string; text: string }> = {
    neutral: { bg: "#2d3345", text: "#e2e8f0" },
    success: { bg: "#064e3b", text: "#34d399" },
    warning: { bg: "#78350f", text: "#fbbf24" },
    danger: { bg: "#7f1d1d", text: "#f87171" },
    accent: { bg: "#1e3a8a", text: "#60a5fa" },
  };

  const badgeStyle = badge ? badgeColors[badge.variant] || badgeColors.neutral : null;

  return (
    <div
      style={{
        backgroundColor: "var(--card-bg, #1a1d27)",
        border: "1px solid var(--border-color, #2d3345)",
        borderRadius: "8px",
        padding: "1rem 1.25rem",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        gap: "0.5rem",
        boxShadow: "0 2px 4px rgba(0,0,0,0.15)",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "flex-start",
          gap: "0.5rem",
        }}
      >
        <span
          style={{
            fontSize: "0.85rem",
            fontWeight: 600,
            color: "var(--text-muted, #9aa0a6)",
            textTransform: "uppercase",
            letterSpacing: "0.04em",
          }}
        >
          {label}
        </span>
        {badge && badgeStyle && (
          <span
            style={{
              fontSize: "0.75rem",
              padding: "0.15rem 0.5rem",
              borderRadius: "9999px",
              backgroundColor: badgeStyle.bg,
              color: badgeStyle.text,
              fontWeight: 500,
            }}
          >
            {badge.text}
          </span>
        )}
      </div>

      <div style={{ display: "flex", alignItems: "baseline", gap: "0.35rem" }}>
        <span
          style={{
            fontSize: "1.75rem",
            fontWeight: 700,
            color: "var(--text-main, #f0f2f5)",
            fontFeatureSettings: '"tnum"',
          }}
        >
          {typeof value === "number"
            ? Number.isInteger(value)
              ? value
              : value.toFixed(2)
            : value}
        </span>
        {unit && (
          <span style={{ fontSize: "0.85rem", color: "var(--text-muted, #9aa0a6)" }}>
            {unit}
          </span>
        )}
      </div>

      {description && (
        <span
          style={{
            fontSize: "0.8rem",
            color: "var(--text-muted, #9aa0a6)",
            lineHeight: 1.3,
          }}
        >
          {description}
        </span>
      )}
    </div>
  );
}
