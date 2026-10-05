/**
 * TypeScript domain type definitions mirroring RightForge FastAPI backend models.
 */

export interface MetricResult {
  name: string;
  value: number;
  description?: string | null;
  unit?: string | null;
}

export interface AnalysisResult {
  document_id?: string | null;
  metrics: Record<string, MetricResult>;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface MetricBaseline {
  name: string;
  mean: number;
  variance: number;
  std_dev: number;
  min_value: number;
  max_value: number;
  sample_count: number;
  description?: string | null;
}

export interface AuthorProfile {
  id: string;
  author_name: string;
  document_count: number;
  baselines: Record<string, MetricBaseline>;
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface MetricDeviation {
  metric_name: string;
  observed_value: number;
  baseline_mean: number;
  baseline_std_dev: number;
  z_score: number;
  absolute_z_score: number;
  is_outlier: boolean;
  description?: string | null;
}

export interface ConsistencyReport {
  author_profile_id: string;
  author_name: string;
  document_id?: string | null;
  consistency_score: number;
  evaluated_metrics_count: number;
  outlier_count: number;
  outliers: string[];
  deviations: Record<string, MetricDeviation>;
  summary: string;
}

export interface TransitionScore {
  from_index: number;
  to_index: number;
  jaccard_similarity: number;
  overlap_coefficient: number;
  shared_content_words: string[];
  is_abrupt_shift: boolean;
}

export interface SemanticCoherenceReport {
  document_id?: string | null;
  paragraph_count: number;
  sentence_count: number;
  mean_paragraph_coherence: number;
  mean_sentence_coherence: number;
  lexical_repetition_rate: number;
  abrupt_transitions_count: number;
  paragraph_transitions: TransitionScore[];
  summary: string;
}

export interface SentencePerplexity {
  sentence_index: number;
  text: string;
  token_count: number;
  perplexity: number;
  mean_logprob: number;
}

export interface PerplexityReport {
  document_id?: string | null;
  overall_perplexity: number;
  mean_sentence_perplexity: number;
  burstiness: number;
  min_sentence_perplexity: number;
  max_sentence_perplexity: number;
  sentence_count: number;
  sentence_perplexities: SentencePerplexity[];
  summary: string;
}

export interface RevisionGoal {
  metric_name: string;
  description: string;
  current_value: number;
  target_value: number;
  direction: "increase" | "decrease" | "maintain";
  severity: "low" | "medium" | "high";
}

export interface SentenceRevisionTarget {
  sentence_index: number;
  original_text: string;
  issue_type: string;
  suggestion: string;
  priority: number;
}

export interface RevisionPlan {
  document_id?: string | null;
  target_author?: string | null;
  goals: RevisionGoal[];
  sentence_targets: SentenceRevisionTarget[];
  total_suggestions: number;
  summary: string;
}

export interface RevisionExecutionResult {
  document_id?: string | null;
  original_text: string;
  revised_text: string;
  plan: RevisionPlan;
  consistency_before?: number | null;
  consistency_after?: number | null;
  metrics_before: Record<string, number>;
  metrics_after: Record<string, number>;
  success: boolean;
  error_message?: string | null;
}
