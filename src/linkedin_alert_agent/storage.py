from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from linkedin_alert_agent.models import JobRecord, ScoreBreakdown
from linkedin_alert_agent.normalize import normalize_job_record


class Storage:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path
        self.connection = sqlite3.connect(database_path)
        self.connection.row_factory = sqlite3.Row
        self.initialize()

    def close(self) -> None:
        self.connection.close()

    def initialize(self) -> None:
        cursor = self.connection.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_message_id TEXT NOT NULL UNIQUE,
                alert_name TEXT NOT NULL,
                received_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_url TEXT,
                job_url_canonical TEXT,
                title_raw TEXT NOT NULL,
                title_normalized TEXT NOT NULL,
                company_raw TEXT,
                company_normalized TEXT,
                location_raw TEXT,
                location_normalized TEXT,
                work_mode TEXT,
                snippet TEXT,
                salary_text TEXT,
                posted_text TEXT,
                first_seen_at TEXT NOT NULL,
                last_seen_at TEXT NOT NULL,
                duplicate_key TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS job_alerts (
                alert_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                PRIMARY KEY (alert_id, job_id),
                FOREIGN KEY(alert_id) REFERENCES alerts(id),
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            );

            CREATE TABLE IF NOT EXISTS scores (
                job_id INTEGER PRIMARY KEY,
                score_total INTEGER NOT NULL,
                title_score INTEGER NOT NULL,
                location_score INTEGER NOT NULL,
                seniority_score INTEGER NOT NULL,
                alignment_score INTEGER NOT NULL,
                company_quality_score INTEGER NOT NULL,
                compensation_score INTEGER NOT NULL,
                penalty_score INTEGER NOT NULL,
                ai_adjustment INTEGER NOT NULL DEFAULT 0,
                notes TEXT NOT NULL,
                rationale TEXT NOT NULL,
                classification TEXT NOT NULL,
                scored_at TEXT NOT NULL,
                FOREIGN KEY(job_id) REFERENCES jobs(id)
            );

            CREATE TABLE IF NOT EXISTS digests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_date TEXT NOT NULL UNIQUE,
                jobs_included TEXT NOT NULL,
                email_subject TEXT NOT NULL,
                html_path TEXT NOT NULL,
                email_sent_at TEXT
            );
            """
        )
        self.connection.commit()

    def has_processed_alert(self, source_message_id: str) -> bool:
        cursor = self.connection.execute(
            "SELECT 1 FROM alerts WHERE source_message_id = ? LIMIT 1",
            (source_message_id,),
        )
        return cursor.fetchone() is not None

    def create_alert(self, source_message_id: str, alert_name: str, received_at: datetime) -> int:
        self.connection.execute(
            """
            INSERT OR IGNORE INTO alerts (source_message_id, alert_name, received_at)
            VALUES (?, ?, ?)
            """,
            (source_message_id, alert_name, received_at.astimezone(timezone.utc).isoformat()),
        )
        row = self.connection.execute(
            "SELECT id FROM alerts WHERE source_message_id = ?",
            (source_message_id,),
        ).fetchone()
        self.connection.commit()
        if row is None:
            raise RuntimeError(f"Unable to create alert row for {source_message_id}")
        return int(row["id"])

    def upsert_job(self, job: JobRecord, seen_at: datetime) -> tuple[int, bool]:
        iso_seen_at = seen_at.astimezone(timezone.utc).isoformat()
        existing = self.connection.execute(
            "SELECT id FROM jobs WHERE duplicate_key = ?",
            (job.duplicate_key,),
        ).fetchone()
        if existing:
            self.connection.execute(
                """
                UPDATE jobs
                SET
                    job_url = COALESCE(NULLIF(?, ''), job_url),
                    job_url_canonical = COALESCE(NULLIF(?, ''), job_url_canonical),
                    title_raw = COALESCE(NULLIF(?, ''), title_raw),
                    title_normalized = COALESCE(NULLIF(?, ''), title_normalized),
                    company_raw = COALESCE(NULLIF(?, ''), company_raw),
                    company_normalized = COALESCE(NULLIF(?, ''), company_normalized),
                    location_raw = COALESCE(NULLIF(?, ''), location_raw),
                    location_normalized = COALESCE(NULLIF(?, ''), location_normalized),
                    work_mode = COALESCE(NULLIF(?, ''), work_mode),
                    snippet = COALESCE(NULLIF(?, ''), snippet),
                    salary_text = COALESCE(NULLIF(?, ''), salary_text),
                    posted_text = COALESCE(NULLIF(?, ''), posted_text),
                    last_seen_at = ?
                WHERE id = ?
                """,
                (
                    job.job_url,
                    job.job_url_canonical,
                    job.title_raw,
                    job.title_normalized,
                    job.company_raw,
                    job.company_normalized,
                    job.location_raw,
                    job.location_normalized,
                    job.work_mode,
                    job.snippet,
                    job.salary_text,
                    job.posted_text,
                    iso_seen_at,
                    int(existing["id"]),
                ),
            )
            self.connection.commit()
            return int(existing["id"]), False

        cursor = self.connection.execute(
            """
            INSERT INTO jobs (
                job_url,
                job_url_canonical,
                title_raw,
                title_normalized,
                company_raw,
                company_normalized,
                location_raw,
                location_normalized,
                work_mode,
                snippet,
                salary_text,
                posted_text,
                first_seen_at,
                last_seen_at,
                duplicate_key
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job.job_url,
                job.job_url_canonical,
                job.title_raw,
                job.title_normalized,
                job.company_raw,
                job.company_normalized,
                job.location_raw,
                job.location_normalized,
                job.work_mode,
                job.snippet,
                job.salary_text,
                job.posted_text,
                iso_seen_at,
                iso_seen_at,
                job.duplicate_key,
            ),
        )
        self.connection.commit()
        return int(cursor.lastrowid), True

    def link_job_to_alert(self, job_id: int, alert_id: int) -> None:
        self.connection.execute(
            """
            INSERT OR IGNORE INTO job_alerts (alert_id, job_id)
            VALUES (?, ?)
            """,
            (alert_id, job_id),
        )
        self.connection.commit()

    def save_score(self, job_id: int, score: ScoreBreakdown) -> None:
        self.connection.execute(
            """
            INSERT INTO scores (
                job_id,
                score_total,
                title_score,
                location_score,
                seniority_score,
                alignment_score,
                company_quality_score,
                compensation_score,
                penalty_score,
                ai_adjustment,
                notes,
                rationale,
                classification,
                scored_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(job_id) DO UPDATE SET
                score_total = excluded.score_total,
                title_score = excluded.title_score,
                location_score = excluded.location_score,
                seniority_score = excluded.seniority_score,
                alignment_score = excluded.alignment_score,
                company_quality_score = excluded.company_quality_score,
                compensation_score = excluded.compensation_score,
                penalty_score = excluded.penalty_score,
                ai_adjustment = excluded.ai_adjustment,
                notes = excluded.notes,
                rationale = excluded.rationale,
                classification = excluded.classification,
                scored_at = excluded.scored_at
            """,
            (
                job_id,
                score.total,
                score.title_score,
                score.location_score,
                score.seniority_score,
                score.alignment_score,
                score.company_quality_score,
                score.compensation_score,
                score.penalty_score,
                score.ai_adjustment,
                json.dumps(score.notes),
                score.rationale,
                score.classification,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        self.connection.commit()

    def save_digest(
        self,
        run_date: str,
        job_ids: list[int],
        email_subject: str,
        html_path: str,
        email_sent_at: str | None,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO digests (run_date, jobs_included, email_subject, html_path, email_sent_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(run_date) DO UPDATE SET
                jobs_included = excluded.jobs_included,
                email_subject = excluded.email_subject,
                html_path = excluded.html_path,
                email_sent_at = excluded.email_sent_at
            """,
            (run_date, json.dumps(job_ids), email_subject, html_path, email_sent_at),
        )
        self.connection.commit()

    def latest_digest(self) -> sqlite3.Row | None:
        return self.connection.execute(
            """
            SELECT run_date, jobs_included, email_subject, html_path, email_sent_at
            FROM digests
            ORDER BY run_date DESC
            LIMIT 1
            """
        ).fetchone()

    def fetch_jobs(self, job_ids: list[int]) -> list[tuple[int, JobRecord]]:
        if not job_ids:
            return []
        placeholders = ", ".join("?" for _ in job_ids)
        rows = self.connection.execute(
            f"""
            SELECT id, job_url, job_url_canonical, title_raw, title_normalized,
                   company_raw, company_normalized, location_raw, location_normalized,
                   work_mode, snippet, salary_text, posted_text, duplicate_key,
                   first_seen_at, last_seen_at
            FROM jobs
            WHERE id IN ({placeholders})
            """,
            tuple(job_ids),
        ).fetchall()
        row_map = {
            int(row["id"]): normalize_job_record(
                JobRecord(
                    title_raw=row["title_raw"],
                    company_raw=row["company_raw"] or "",
                    location_raw=row["location_raw"] or "",
                    job_url=row["job_url"] or "",
                    snippet=row["snippet"] or "",
                    salary_text=row["salary_text"] or "",
                    posted_text=row["posted_text"] or "",
                    work_mode=row["work_mode"] or "",
                    title_normalized=row["title_normalized"] or "",
                    company_normalized=row["company_normalized"] or "",
                    location_normalized=row["location_normalized"] or "",
                    job_url_canonical=row["job_url_canonical"] or "",
                    duplicate_key=row["duplicate_key"] or "",
                    first_seen_at=row["first_seen_at"],
                    last_seen_at=row["last_seen_at"],
                )
            )
            for row in rows
        }
        return [(job_id, row_map[job_id]) for job_id in job_ids if job_id in row_map]
