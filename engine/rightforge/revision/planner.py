"""Controlled revision planning engine for rule-governed style adaptation."""

from collections import Counter
import math
from typing import Sequence

from rightforge.models.comparison import ConsistencyReport
from rightforge.models.document import Document
from rightforge.models.profile import AuthorProfile
from rightforge.models.revision import RevisionGoal, RevisionPlan, SentenceRevisionTarget
from rightforge.profiles.comparator import ProfileComparator
from rightforge.text.function_words import ALL_FUNCTION_WORDS
from rightforge.text.segmentation import split_sentences, tokenize_words


class RevisionPlanner:
    """Analyzes documents for stylistic anomalies and generates actionable sentence-level interventions."""

    def __init__(self, comparator: ProfileComparator | None = None) -> None:
        self.comparator = comparator if comparator is not None else ProfileComparator()

    def generate_plan(
        self,
        target: Document | str,
        profile: AuthorProfile | None = None,
        outlier_threshold: float = 2.0,
    ) -> RevisionPlan:
        """Construct a structured revision plan containing global goals and sentence targets."""
        text = target.text if isinstance(target, Document) else target
        doc_id = target.id if isinstance(target, Document) else None

        sentences = split_sentences(text)
        if not sentences or not text.strip():
            return RevisionPlan(
                document_id=doc_id,
                target_author=profile.author_name if profile else None,
                goals=[],
                sentence_targets=[],
                total_suggestions=0,
                summary="Document contains no readable text for revision planning.",
            )

        tokenized_sentences = [
            tokenize_words(s) for s in sentences
        ]
        lengths = [len(words) for words in tokenized_sentences]
        sentence_targets: list[SentenceRevisionTarget] = []

        # 1. Evaluate sentence-level interventions
        self._detect_excessive_lengths(sentences, lengths, profile, sentence_targets)
        self._detect_cadence_monotony(sentences, lengths, sentence_targets)
        self._detect_repetitive_openers(sentences, tokenized_sentences, sentence_targets)
        self._detect_lexical_redundancy(sentences, tokenized_sentences, sentence_targets)

        # Sort sentence targets by sentence index and priority
        sentence_targets.sort(key=lambda t: (t.sentence_index, t.priority))

        # 2. Formulate global revision goals
        goals: list[RevisionGoal] = []
        if profile is not None:
            goals = self._goals_from_profile(target, profile, outlier_threshold)
        else:
            goals = self._goals_from_heuristics(tokenized_sentences, lengths)

        # 3. Generate executive summary
        summary = self._build_summary(goals, sentence_targets, profile)

        return RevisionPlan(
            document_id=doc_id,
            target_author=profile.author_name if profile else None,
            goals=goals,
            sentence_targets=sentence_targets,
            total_suggestions=len(sentence_targets),
            summary=summary,
        )

    def _detect_excessive_lengths(
        self,
        sentences: list[str],
        lengths: list[int],
        profile: AuthorProfile | None,
        targets: list[SentenceRevisionTarget],
    ) -> None:
        """Flag sentences that risk reader fatigue or exceed target profile lengths."""
        max_target = 35
        if profile:
            target_mean = None
            if "sentence_length_mean" in profile.baselines:
                target_mean = profile.baselines["sentence_length_mean"].mean
            elif "avg_words_per_sentence" in profile.baselines:
                target_mean = profile.baselines["avg_words_per_sentence"].mean
            if target_mean is not None:
                max_target = max(int(target_mean * 1.75), 28)

        for idx, (sentence, length) in enumerate(zip(sentences, lengths)):
            if length > max_target:
                targets.append(
                    SentenceRevisionTarget(
                        sentence_index=idx,
                        original_text=sentence,
                        issue_type="excessive_length",
                        suggestion=(
                            f"Sentence contains {length} words (threshold is {max_target}). "
                            "Consider partitioning into two distinct clauses to enhance rhythmic cadence."
                        ),
                        priority=1,
                    )
                )

    def _detect_cadence_monotony(
        self,
        sentences: list[str],
        lengths: list[int],
        targets: list[SentenceRevisionTarget],
    ) -> None:
        """Identify runs of near-identical sentence lengths causing cadence flattening."""
        if len(lengths) < 3:
            return

        for i in range(2, len(lengths)):
            w1, w2, w3 = lengths[i - 2], lengths[i - 1], lengths[i]
            if w1 > 0 and abs(w1 - w2) <= 2 and abs(w2 - w3) <= 2:
                targets.append(
                    SentenceRevisionTarget(
                        sentence_index=i,
                        original_text=sentences[i],
                        issue_type="cadence_monotony",
                        suggestion=(
                            f"Three consecutive sentences share near-identical lengths ({w1}, {w2}, {w3} words). "
                            "Introduce a short staccato statement or an expansive compound sentence to restore cadence burstiness."
                        ),
                        priority=2,
                    )
                )

    def _detect_repetitive_openers(
        self,
        sentences: list[str],
        tokenized_sentences: list[list[str]],
        targets: list[SentenceRevisionTarget],
    ) -> None:
        """Flag consecutive sentences opening with the identical grammatical word."""
        if len(tokenized_sentences) < 2:
            return

        for i in range(1, len(tokenized_sentences)):
            words_prev = tokenized_sentences[i - 1]
            words_curr = tokenized_sentences[i]
            if words_prev and words_curr:
                opener_prev = words_prev[0].lower()
                opener_curr = words_curr[0].lower()
                if opener_prev == opener_curr and len(opener_curr) > 1:
                    targets.append(
                        SentenceRevisionTarget(
                            sentence_index=i,
                            original_text=sentences[i],
                            issue_type="repetitive_opener",
                            suggestion=(
                                f"Consecutive sentences open with '{words_curr[0]}'. "
                                "Invert the clause or introduce an adverbial phrase to diversify sentence heads."
                            ),
                            priority=2,
                        )
                    )

    def _detect_lexical_redundancy(
        self,
        sentences: list[str],
        tokenized_sentences: list[list[str]],
        targets: list[SentenceRevisionTarget],
    ) -> None:
        """Identify content words overused within an individual sentence."""
        for idx, (sentence, words) in enumerate(zip(sentences, tokenized_sentences)):
            content_words = [w.lower() for w in words if w.lower() not in ALL_FUNCTION_WORDS and len(w) > 2]
            counts = Counter(content_words)
            for word, freq in counts.items():
                if freq >= 3:
                    targets.append(
                        SentenceRevisionTarget(
                            sentence_index=idx,
                            original_text=sentence,
                            issue_type="lexical_redundancy",
                            suggestion=(
                                f"Word '{word}' appears {freq} times within a single sentence. "
                                "Substitute with contextual synonyms or rephrase to reduce redundancy."
                            ),
                            priority=3,
                        )
                    )

    def _goals_from_profile(
        self,
        target: Document | str,
        profile: AuthorProfile,
        threshold: float,
    ) -> list[RevisionGoal]:
        """Derive revision goals by identifying deviations against reference AuthorProfile."""
        doc = Document(text=target) if isinstance(target, str) else target
        comparison = self.comparator.compare(
            profile=profile, target=doc, outlier_threshold=threshold
        )

        goals: list[RevisionGoal] = []
        for metric_name in comparison.outliers:
            dev = comparison.deviations.get(metric_name)
            if not dev:
                continue
            direction = "decrease" if dev.z_score > 0 else "increase"
            severity = "high" if abs(dev.z_score) >= 3.0 else "medium"
            description = (
                f"Metric '{dev.metric_name}' deviates from author baseline "
                f"(observed {dev.observed_value:.2f} vs expected {dev.baseline_mean:.2f})."
            )
            goals.append(
                RevisionGoal(
                    metric_name=dev.metric_name,
                    description=description,
                    current_value=round(dev.observed_value, 4),
                    target_value=round(dev.baseline_mean, 4),
                    direction=direction,
                    severity=severity,
                )
            )
        return goals

    def _goals_from_heuristics(
        self,
        tokenized_sentences: list[list[str]],
        lengths: list[int],
    ) -> list[RevisionGoal]:
        """Derive baseline revision goals from intrinsic stylistic distributions."""
        goals: list[RevisionGoal] = []
        if not lengths:
            return goals

        mean_len = sum(lengths) / len(lengths)
        if mean_len > 25.0:
            goals.append(
                RevisionGoal(
                    metric_name="sentence_length_mean",
                    description="Average sentence length is elevated; reduce to prevent reader fatigue.",
                    current_value=round(mean_len, 2),
                    target_value=18.0,
                    direction="decrease",
                    severity="medium",
                )
            )
        elif mean_len < 10.0 and len(lengths) >= 3:
            goals.append(
                RevisionGoal(
                    metric_name="sentence_length_mean",
                    description="Average sentence length is truncated; elaborate ideas to avoid fragmented cadence.",
                    current_value=round(mean_len, 2),
                    target_value=16.0,
                    direction="increase",
                    severity="medium",
                )
            )

        # Check sentence length variance
        if len(lengths) >= 3:
            variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
            std_dev = math.sqrt(variance)
            if std_dev < 3.0:
                goals.append(
                    RevisionGoal(
                        metric_name="sentence_length_std_dev",
                        description="Sentence length variation is low; diversify sentence structures to enhance cadence burstiness.",
                        current_value=round(std_dev, 2),
                        target_value=6.0,
                        direction="increase",
                        severity="high",
                    )
                )

        # Check lexical richness (TTR)
        all_words = [w.lower() for s in tokenized_sentences for w in s]
        if all_words:
            ttr = len(set(all_words)) / len(all_words)
            if ttr < 0.40 and len(all_words) > 20:
                goals.append(
                    RevisionGoal(
                        metric_name="type_token_ratio",
                        description="Lexical richness is low; expand vocabulary and reduce verbatim repetitions.",
                        current_value=round(ttr, 4),
                        target_value=0.55,
                        direction="increase",
                        severity="medium",
                    )
                )

        return goals

    def _build_summary(
        self,
        goals: list[RevisionGoal],
        targets: list[SentenceRevisionTarget],
        profile: AuthorProfile | None,
    ) -> str:
        """Generate human-readable summary of the plan."""
        target_count = len(targets)
        goal_count = len(goals)

        if profile:
            context = f"against AuthorProfile '{profile.author_name}'"
        else:
            context = "based on general stylistic and cadence heuristics"

        if target_count == 0 and goal_count == 0:
            return f"Document is well-balanced {context} with no critical stylistic anomalies detected."

        high_priority = sum(1 for t in targets if t.priority == 1)
        return (
            f"Generated revision plan {context}: {goal_count} global goal(s) and "
            f"{target_count} sentence-level recommendation(s) ({high_priority} high priority)."
        )
