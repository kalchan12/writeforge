"use client";

import { useEffect, useState } from "react";

interface ServiceHealth {
  status: string;
  service: string;
  version: string;
}

export default function HomePage() {
  const [health, setHealth] = useState<ServiceHealth | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/health`);
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        const data: ServiceHealth = await res.json();
        setHealth(data);
      } catch (err: unknown) {
        setError(
          err instanceof Error
            ? err.message
            : "Could not connect to RightForge API"
        );
      } finally {
        setLoading(false);
      }
    };

    checkBackend();
  }, []);

  return (
    <main
      style={{
        maxWidth: "760px",
        margin: "0 auto",
        padding: "4rem 1.5rem",
        display: "flex",
        flexDirection: "column",
        gap: "2rem",
      }}
    >
      <header>
        <h1 style={{ fontSize: "2.25rem", fontWeight: 700, letterSpacing: "-0.03em" }}>
          RightForge
        </h1>
        <p style={{ color: "var(--text-muted)", marginTop: "0.5rem", fontSize: "1.1rem" }}>
          Local-first writing analysis and author-style research platform
        </p>
      </header>

      <section
        style={{
          border: "1px solid var(--border-color)",
          borderRadius: "8px",
          backgroundColor: "var(--card-bg)",
          padding: "1.5rem",
        }}
      >
        <h2 style={{ fontSize: "1.2rem", marginBottom: "0.75rem" }}>
          Phase 0 Foundation Status
        </h2>
        <p style={{ color: "var(--text-muted)", fontSize: "0.95rem", marginBottom: "1rem" }}>
          Minimal application shell established. Core analysis engine, domain models, and API boundary initialized.
        </p>

        <div
          style={{
            padding: "0.75rem 1rem",
            borderRadius: "6px",
            background: "#12151f",
            border: "1px solid var(--border-color)",
            fontSize: "0.9rem",
            fontFamily: "monospace",
          }}
        >
          <strong>API Status: </strong>
          {loading && <span>Checking API connection (http://localhost:8000/health)...</span>}
          {!loading && health && (
            <span style={{ color: "var(--success-color)" }}>
              Connected ({health.service} v{health.version} - {health.status})
            </span>
          )}
          {!loading && error && (
            <span style={{ color: "#f87171" }}>
              Offline ({error}) - Ensure API server is running on port 8000.
            </span>
          )}
        </div>
      </section>

      <section style={{ color: "var(--text-muted)", fontSize: "0.9rem" }}>
        <p>
          Next development phase: Deterministic document statistics and linguistic metrics pipeline.
        </p>
      </section>
    </main>
  );
}
