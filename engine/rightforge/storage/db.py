"""Local SQLite persistence manager for RightForge."""

from datetime import datetime, timezone
import json
import os
import sqlite3
from typing import Any
from uuid import uuid4

from rightforge.models.document import Document
from rightforge.models.execution import RevisionExecutionResult
from rightforge.models.profile import AuthorProfile, MetricBaseline
from rightforge.models.revision import RevisionPlan


class DatabaseManager:
    """Manages local SQLite database connections, schema migrations, and transactions."""

    def __init__(self, db_path: str = "data/writeforge.db") -> None:
        self.db_path = db_path
        if db_path != ":memory:":
            os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._initialize_pragmas()
        self._initialize_schema()

    def _initialize_pragmas(self) -> None:
        cursor = self._conn.cursor()
        if self.db_path != ":memory:":
            cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        self._conn.commit()

    def _initialize_schema(self) -> None:
        cursor = self._conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS author_profiles (
                id TEXT PRIMARY KEY,
                author_name TEXT NOT NULL,
                document_count INTEGER NOT NULL DEFAULT 0,
                baselines_json TEXT NOT NULL DEFAULT '{}',
                metadata_json TEXT NOT NULL DEFAULT '{}',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS revision_logs (
                id TEXT PRIMARY KEY,
                document_id TEXT,
                author_name TEXT,
                original_text TEXT NOT NULL,
                revised_text TEXT NOT NULL,
                plan_json TEXT NOT NULL DEFAULT '{}',
                consistency_before REAL,
                consistency_after REAL,
                metrics_before_json TEXT NOT NULL DEFAULT '{}',
                metrics_after_json TEXT NOT NULL DEFAULT '{}',
                success INTEGER NOT NULL DEFAULT 1,
                error_message TEXT,
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_author_profiles_name ON author_profiles(author_name);
            CREATE INDEX IF NOT EXISTS idx_revision_logs_created ON revision_logs(created_at);
            """
        )
        self._conn.commit()

    def close(self) -> None:
        """Close database connection."""
        self._conn.close()

    # --- Document Repository Methods ---

    def save_document(self, document: Document) -> Document:
        """Persist a Document entity to SQLite."""
        cursor = self._conn.cursor()
        created_str = (
            document.created_at.isoformat()
            if hasattr(document, "created_at") and document.created_at
            else datetime.now(timezone.utc).isoformat()
        )
        cursor.execute(
            """
            INSERT OR REPLACE INTO documents (id, text, metadata_json, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                document.id,
                document.text,
                json.dumps(document.metadata),
                created_str,
            ),
        )
        self._conn.commit()
        return document

    def get_document(self, doc_id: str) -> Document | None:
        """Retrieve a Document by ID."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return Document(
            id=row["id"],
            text=row["text"],
            metadata=json.loads(row["metadata_json"]),
        )

    def list_documents(self, limit: int = 50) -> list[Document]:
        """List recently saved documents."""
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT * FROM documents ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        return [
            Document(
                id=r["id"],
                text=r["text"],
                metadata=json.loads(r["metadata_json"]),
            )
            for r in rows
        ]

    # --- AuthorProfile Repository Methods ---

    def save_profile(self, profile: AuthorProfile) -> AuthorProfile:
        """Persist an AuthorProfile entity with baselines JSON."""
        cursor = self._conn.cursor()
        baselines_dict = {
            k: v.model_dump() for k, v in profile.baselines.items()
        }
        created_str = profile.created_at.isoformat()
        updated_str = profile.updated_at.isoformat()

        cursor.execute(
            """
            INSERT OR REPLACE INTO author_profiles (
                id, author_name, document_count, baselines_json, metadata_json, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile.id,
                profile.author_name,
                profile.document_count,
                json.dumps(baselines_dict),
                json.dumps(profile.metadata),
                created_str,
                updated_str,
            ),
        )
        self._conn.commit()
        return profile

    def get_profile(self, profile_id: str) -> AuthorProfile | None:
        """Retrieve an AuthorProfile by unique ID."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM author_profiles WHERE id = ?", (profile_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_profile(row)

    def get_profile_by_name(self, author_name: str) -> AuthorProfile | None:
        """Retrieve the most recent AuthorProfile for a specific author name."""
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT * FROM author_profiles WHERE author_name = ? ORDER BY updated_at DESC LIMIT 1",
            (author_name,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_profile(row)

    def list_profiles(self, limit: int = 50) -> list[AuthorProfile]:
        """List all saved AuthorProfiles."""
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT * FROM author_profiles ORDER BY updated_at DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        return [self._row_to_profile(r) for r in rows]

    def _row_to_profile(self, row: sqlite3.Row) -> AuthorProfile:
        raw_baselines = json.loads(row["baselines_json"])
        baselines = {
            k: MetricBaseline(**v) for k, v in raw_baselines.items()
        }
        return AuthorProfile(
            id=row["id"],
            author_name=row["author_name"],
            document_count=row["document_count"],
            baselines=baselines,
            metadata=json.loads(row["metadata_json"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    # --- Revision Logs Repository Methods ---

    def log_revision(self, result: RevisionExecutionResult) -> str:
        """Store a revision execution audit record."""
        log_id = str(uuid4())
        cursor = self._conn.cursor()
        created_str = datetime.now(timezone.utc).isoformat()
        author_name = result.plan.target_author if result.plan else None

        cursor.execute(
            """
            INSERT INTO revision_logs (
                id, document_id, author_name, original_text, revised_text, plan_json,
                consistency_before, consistency_after, metrics_before_json, metrics_after_json,
                success, error_message, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                log_id,
                result.document_id,
                author_name,
                result.original_text,
                result.revised_text,
                json.dumps(result.plan.model_dump()),
                result.consistency_before,
                result.consistency_after,
                json.dumps(result.metrics_before),
                json.dumps(result.metrics_after),
                1 if result.success else 0,
                result.error_message,
                created_str,
            ),
        )
        self._conn.commit()
        return log_id

    def list_revision_logs(self, limit: int = 50) -> list[dict[str, Any]]:
        """Retrieve recent revision execution logs."""
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT * FROM revision_logs ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = cursor.fetchall()
        return [
            {
                "id": r["id"],
                "document_id": r["document_id"],
                "author_name": r["author_name"],
                "original_text": r["original_text"],
                "revised_text": r["revised_text"],
                "plan": json.loads(r["plan_json"]),
                "consistency_before": r["consistency_before"],
                "consistency_after": r["consistency_after"],
                "metrics_before": json.loads(r["metrics_before_json"]),
                "metrics_after": json.loads(r["metrics_after_json"]),
                "success": bool(r["success"]),
                "error_message": r["error_message"],
                "created_at": r["created_at"],
            }
            for r in rows
        ]
