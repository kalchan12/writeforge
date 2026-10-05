"""Unit tests for local SQLite persistence layer."""

from rightforge.models.document import Document
from rightforge.models.execution import RevisionExecutionResult
from rightforge.models.profile import AuthorProfile, MetricBaseline
from rightforge.models.revision import RevisionPlan
from rightforge.storage.db import DatabaseManager


def test_database_manager_initialization():
    """Verify in-memory database initializes with operational schema and WAL pragmas."""
    db = DatabaseManager(db_path=":memory:")
    assert db._conn is not None
    db.close()


def test_document_save_and_retrieval():
    """Verify documents can be saved, listed, and queried by ID."""
    db = DatabaseManager(db_path=":memory:")
    doc = Document(id="doc-test-1", text="Sample prose for persistence.", metadata={"genre": "fiction"})

    saved = db.save_document(doc)
    assert saved.id == "doc-test-1"

    retrieved = db.get_document("doc-test-1")
    assert retrieved is not None
    assert retrieved.id == "doc-test-1"
    assert retrieved.text == "Sample prose for persistence."
    assert retrieved.metadata["genre"] == "fiction"

    non_existent = db.get_document("non-existent-id")
    assert non_existent is None

    docs = db.list_documents()
    assert len(docs) == 1
    assert docs[0].id == "doc-test-1"
    db.close()


def test_profile_save_and_retrieval():
    """Verify AuthorProfile entities and baseline distributions are persisted faithfully."""
    db = DatabaseManager(db_path=":memory:")
    profile = AuthorProfile(
        author_name="Virginia Woolf",
        document_count=3,
        baselines={
            "avg_words_per_sentence": MetricBaseline(
                name="avg_words_per_sentence",
                mean=24.5,
                variance=4.2,
                std_dev=2.05,
                min_value=18.0,
                max_value=30.0,
                sample_count=3,
            )
        },
        metadata={"era": "modernism"},
    )

    saved = db.save_profile(profile)
    assert saved.author_name == "Virginia Woolf"

    retrieved = db.get_profile(profile.id)
    assert retrieved is not None
    assert retrieved.author_name == "Virginia Woolf"
    assert "avg_words_per_sentence" in retrieved.baselines
    assert retrieved.baselines["avg_words_per_sentence"].mean == 24.5

    by_name = db.get_profile_by_name("Virginia Woolf")
    assert by_name is not None
    assert by_name.id == profile.id

    profiles = db.list_profiles()
    assert len(profiles) == 1
    db.close()


def test_revision_logging_and_retrieval():
    """Verify revision audit logs store plans, metric snapshots, and error states."""
    db = DatabaseManager(db_path=":memory:")
    plan = RevisionPlan(
        document_id="doc-rev-1",
        target_author="Hemingway",
        goals=[],
        sentence_targets=[],
        total_suggestions=0,
        summary="Clear prose",
    )
    result = RevisionExecutionResult(
        document_id="doc-rev-1",
        original_text="Long text needing revision.",
        revised_text="Short clean text.",
        plan=plan,
        consistency_before=0.45,
        consistency_after=0.88,
        metrics_before={"word_count": 4.0},
        metrics_after={"word_count": 3.0},
        success=True,
    )

    log_id = db.log_revision(result)
    assert isinstance(log_id, str)
    assert len(log_id) > 0

    logs = db.list_revision_logs()
    assert len(logs) == 1
    log = logs[0]
    assert log["document_id"] == "doc-rev-1"
    assert log["author_name"] == "Hemingway"
    assert log["consistency_before"] == 0.45
    assert log["consistency_after"] == 0.88
    assert log["success"] is True
    db.close()
