from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class JobRecord:
    title_raw: str
    company_raw: str = ""
    location_raw: str = ""
    job_url: str = ""
    snippet: str = ""
    salary_text: str = ""
    posted_text: str = ""
    work_mode: str = ""
    source_alert_name: str = ""
    source_email_timestamp: str = ""
    parse_confidence: float = 0.0
    title_normalized: str = ""
    company_normalized: str = ""
    location_normalized: str = ""
    job_url_canonical: str = ""
    duplicate_key: str = ""
    first_seen_at: str | None = None
    last_seen_at: str | None = None


@dataclass(slots=True)
class ParsedAlert:
    message_id: str
    alert_name: str
    received_at: datetime
    jobs: list[JobRecord]
    subject: str = ""


@dataclass(slots=True)
class ScoreBreakdown:
    total: int
    title_score: int
    location_score: int
    seniority_score: int
    alignment_score: int
    company_quality_score: int
    compensation_score: int
    penalty_score: int
    notes: list[str] = field(default_factory=list)
    rationale: str = ""
    classification: str = "Low priority"
    ai_adjustment: int = 0


@dataclass(slots=True)
class SourceMessage:
    message_id: str
    raw_bytes: bytes
    received_at: datetime | None = None
    origin: str = "filesystem"
