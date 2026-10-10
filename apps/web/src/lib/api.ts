/**
 * Typed API client for the RightForge FastAPI backend.
 */

import {
  AnalysisResult,
  AuthorProfile,
  ConsistencyReport,
  PerplexityReport,
  RevisionExecutionResult,
  RevisionPlan,
  SemanticCoherenceReport,
} from "../types/api";

export interface AISignal {
  name: string;
  raw_value: number;
  sub_score: number;
  weight: number;
  description: string;
}

export interface AIDetectionReport {
  ai_score: number;
  ai_score_percent: number;
  verdict: string;
  confidence: string;
  signals: AISignal[];
  summary: string;
}

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function postJson<T>(endpoint: string, body: unknown): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    let errorDetail = `HTTP ${res.status}`;
    try {
      const errJson = await res.json();
      if (errJson.detail) {
        errorDetail = typeof errJson.detail === "string"
          ? errJson.detail
          : JSON.stringify(errJson.detail);
      }
    } catch {
      // Ignore JSON parse error on non-JSON response
    }
    throw new Error(errorDetail);
  }

  return res.json() as Promise<T>;
}

export async function fetchHealth(): Promise<{ status: string; service: string; version: string }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) {
    throw new Error(`Health check failed: HTTP ${res.status}`);
  }
  return res.json();
}

export async function analyzeBasic(
  text: string,
  metadata: Record<string, unknown> = {}
): Promise<AnalysisResult> {
  return postJson<AnalysisResult>("/analysis/basic", { text, metadata });
}

export async function analyzeLinguistic(
  text: string,
  metadata: Record<string, unknown> = {}
): Promise<AnalysisResult> {
  return postJson<AnalysisResult>("/analysis/linguistic", { text, metadata });
}

export async function analyzeStylometry(
  text: string,
  metadata: Record<string, unknown> = {}
): Promise<AnalysisResult> {
  return postJson<AnalysisResult>("/analysis/stylometry", { text, metadata });
}

export async function analyzeCoherence(
  text: string,
  metadata: Record<string, unknown> = {}
): Promise<SemanticCoherenceReport> {
  return postJson<SemanticCoherenceReport>("/analysis/coherence", { text, metadata });
}

export async function analyzePerplexity(
  text: string,
  metadata: Record<string, unknown> = {}
): Promise<PerplexityReport> {
  return postJson<PerplexityReport>("/analysis/perplexity", { text, metadata });
}

export async function createProfile(
  authorName: string,
  documents: Array<{ text: string; metadata?: Record<string, unknown> }>,
  metadata: Record<string, unknown> = {}
): Promise<AuthorProfile> {
  return postJson<AuthorProfile>("/profiles/create", {
    author_name: authorName,
    documents,
    metadata,
  });
}

export async function compareProfile(
  text: string,
  profile: AuthorProfile,
  outlierThreshold: number = 2.0
): Promise<ConsistencyReport> {
  return postJson<ConsistencyReport>("/profiles/compare", {
    text,
    profile,
    outlier_threshold: outlierThreshold,
  });
}

export async function planRevision(
  text: string,
  profile?: AuthorProfile | null,
  outlierThreshold: number = 2.0
): Promise<RevisionPlan> {
  return postJson<RevisionPlan>("/revision/plan", {
    text,
    profile: profile || null,
    outlier_threshold: outlierThreshold,
  });
}

export async function executeRevision(
  text: string,
  options: {
    profile?: AuthorProfile | null;
    model?: string;
    endpointUrl?: string;
    useMock?: boolean;
    outlierThreshold?: number;
  } = {}
): Promise<RevisionExecutionResult> {
  return postJson<RevisionExecutionResult>("/revision/execute", {
    text,
    profile: options.profile || null,
    model: options.model || "llama3",
    endpoint_url: options.endpointUrl || "http://localhost:11434",
    use_mock: options.useMock ?? false,
    outlier_threshold: options.outlierThreshold ?? 2.0,
  });
}

export async function detectAI(
  text: string,
  metadata: Record<string, unknown> = {}
): Promise<AIDetectionReport> {
  return postJson<AIDetectionReport>("/analysis/ai-detect", { text, metadata });
}
