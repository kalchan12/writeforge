"""Unit tests for the controlled revision planning engine."""

from rightforge.models.document import Document
from rightforge.models.profile import AuthorProfile, MetricBaseline
from rightforge.models.revision import RevisionPlan, SentenceRevisionTarget
from rightforge.revision.planner import RevisionPlanner


def test_revision_planner_empty_text():
    """Verify revision planner returns clean empty plan for empty input."""
    planner = RevisionPlanner()
    plan = planner.generate_plan("")

    assert isinstance(plan, RevisionPlan)
    assert plan.total_suggestions == 0
    assert len(plan.goals) == 0
    assert len(plan.sentence_targets) == 0
    assert "no readable text" in plan.summary.lower()


def test_revision_planner_detects_excessive_length():
    """Verify that run-on sentences exceeding 35 words trigger high-priority length warnings."""
    planner = RevisionPlanner()
    long_sentence = (
        "Although the initial preliminary findings suggested that the algorithmic methodology "
        "might exhibit superior classification accuracy across diverse observational corpora, "
        "subsequent rigorous evaluations conducted under strictly controlled laboratory protocols "
        "revealed several critical architectural discrepancies that fundamentally undermined "
        "the statistical validity of the empirical baseline measurements."
    )
    plan = planner.generate_plan(long_sentence)

    assert plan.total_suggestions >= 1
    length_issues = [t for t in plan.sentence_targets if t.issue_type == "excessive_length"]
    assert len(length_issues) == 1
    target = length_issues[0]
    assert target.sentence_index == 0
    assert target.priority == 1
    assert "words" in target.suggestion


def test_revision_planner_detects_cadence_monotony():
    """Verify that 3 consecutive sentences of identical word lengths trigger cadence monotony targets."""
    planner = RevisionPlanner()
    text = (
        "The red fox ran quickly into the woods today. "
        "The old man sat quietly near the river banks. "
        "The cold wind blew sharply across the dark hills."
    )
    plan = planner.generate_plan(text)

    monotony_issues = [t for t in plan.sentence_targets if t.issue_type == "cadence_monotony"]
    assert len(monotony_issues) >= 1
    target = monotony_issues[0]
    assert target.priority == 2
    assert "burstiness" in target.suggestion.lower() or "cadence" in target.suggestion.lower()


def test_revision_planner_detects_repetitive_openers():
    """Verify that consecutive sentences starting with the same word are flagged."""
    planner = RevisionPlanner()
    text = (
        "Furthermore, empirical analysis requires rigorous observation. "
        "Furthermore, experimental reproducibility guarantees reliable scientific conclusions."
    )
    plan = planner.generate_plan(text)

    opener_issues = [t for t in plan.sentence_targets if t.issue_type == "repetitive_opener"]
    assert len(opener_issues) == 1
    target = opener_issues[0]
    assert target.sentence_index == 1
    assert "Furthermore" in target.suggestion


def test_revision_planner_detects_lexical_redundancy():
    """Verify that repeating a content word 3+ times in one sentence triggers redundancy suggestion."""
    planner = RevisionPlanner()
    text = (
        "The experiment proved that this experiment was the definitive experiment of the decade."
    )
    plan = planner.generate_plan(text)

    redundancy_issues = [t for t in plan.sentence_targets if t.issue_type == "lexical_redundancy"]
    assert len(redundancy_issues) >= 1
    target = redundancy_issues[0]
    assert "experiment" in target.suggestion


def test_revision_planner_profile_guided_goals():
    """Verify that profile deviations generate aligned revision goals."""
    profile = AuthorProfile(
        author_name="Hemingway",
        document_count=5,
        baselines={
            "sentence_length_mean": MetricBaseline(
                name="sentence_length_mean",
                mean=10.0,
                variance=1.0,
                std_dev=1.0,
                min_value=8.0,
                max_value=12.0,
                sample_count=5,
            ),
        },
    )

    doc = Document(
        text=(
            "The extremely sophisticated technological paradigm shifts necessitate comprehensive reevaluations "
            "across all computational and theoretical frameworks in modern enterprise domains. "
            "Such unprecedented transformational dynamics inevitably precipitate systemic operational restructuring "
            "throughout distributed organizations and academic institutions globally."
        )
    )

    planner = RevisionPlanner()
    plan = planner.generate_plan(target=doc, profile=profile, outlier_threshold=1.5)

    assert plan.target_author == "Hemingway"
    assert len(plan.goals) >= 1
    len_goal = next((g for g in plan.goals if g.metric_name == "sentence_length_mean"), None)
    assert len_goal is not None
    assert len_goal.direction == "decrease"
    assert len_goal.target_value == 10.0


def test_revision_planner_document_id_preservation():
    """Verify document identifier is preserved in revision plan output."""
    planner = RevisionPlanner()
    doc = Document(id="doc-special-99", text="Short prose.")
    plan = planner.generate_plan(doc)

    assert plan.document_id == "doc-special-99"
