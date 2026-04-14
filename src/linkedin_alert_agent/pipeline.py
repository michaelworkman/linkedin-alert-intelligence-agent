from __future__ import annotations

import json
import traceback
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from linkedin_alert_agent.ai import OpenAIReasoner
from linkedin_alert_agent.config import Config
from linkedin_alert_agent.digest import render_digest_html
from linkedin_alert_agent.emailer import send_html_email
from linkedin_alert_agent.gmail import GmailApiClient, GoogleOAuthManager, load_google_client_config
from linkedin_alert_agent.models import JobRecord, ScoreBreakdown
from linkedin_alert_agent.parsers import parse_alert_email
from linkedin_alert_agent.scoring import JobScorer, load_profile
from linkedin_alert_agent.sources import FilesystemMessageSource, GmailApiMessageSource
from linkedin_alert_agent.storage import Storage


@dataclass(slots=True)
class RunSummary:
    run_date: str
    processed_messages: int
    parsed_jobs: int
    new_jobs: int
    duplicates_removed: int
    digest_path: Path
    email_sent_at: str | None
    subject: str


def _build_source(config: Config):
    if config.source_mode == "gmail":
        if config.gmail_access_token:
            client = GmailApiClient(access_token_supplier=lambda: config.gmail_access_token)
        else:
            oauth_manager = GoogleOAuthManager(
                client_config=load_google_client_config(
                    client_id=config.gmail_client_id,
                    client_secret=config.gmail_client_secret,
                    redirect_uri=config.gmail_redirect_uri,
                    client_secrets_path=config.gmail_client_secrets_path,
                ),
                token_path=config.gmail_token_path,
            )
            client = GmailApiClient(
                access_token_supplier=lambda: oauth_manager.get_token(config.gmail_scopes).access_token
            )
        return GmailApiMessageSource(
            client=client,
            query=config.gmail_query,
            label_names=config.gmail_label_names,
            label_ids=config.gmail_label_ids,
            processed_label_name=config.gmail_processed_label_name,
            create_processed_label=config.gmail_create_processed_label,
            max_results=config.gmail_max_results,
            mark_read=config.gmail_mark_read,
        )
    if config.source_mode != "filesystem":
        raise ValueError(f"Unsupported SOURCE_MODE: {config.source_mode}")
    return FilesystemMessageSource(config.filesystem_input_dir)


def _maybe_refine_with_ai(
    reasoner: OpenAIReasoner | None,
    job: JobRecord,
    score: ScoreBreakdown,
    profile: dict,
    scorer: JobScorer,
) -> ScoreBreakdown:
    if reasoner is None:
        return score
    try:
        refinement = reasoner.refine(job, score, profile)
    except Exception:
        return score
    if not refinement:
        return score

    adjustment = int(refinement.get("score_adjustment", 0))
    score.ai_adjustment = max(-10, min(10, adjustment))
    score.total = max(0, min(100, score.total + score.ai_adjustment))
    combined_notes = score.notes + list(refinement.get("matching_signals", [])) + list(refinement.get("caution_signals", []))
    deduped_notes: list[str] = []
    seen: set[str] = set()
    for note in combined_notes:
        cleaned = note.strip()
        lowered = cleaned.lower()
        if cleaned and lowered not in seen:
            seen.add(lowered)
            deduped_notes.append(cleaned)
    score.notes = deduped_notes
    rationale = str(refinement.get("rationale", "")).strip()
    if rationale:
        score.rationale = rationale
    score.classification = scorer.classify(score.total)
    return score


def run_pipeline(config: Config, dry_run: bool = False) -> RunSummary:
    config.ensure_directories()
    profile = load_profile(config.profile_path)
    scorer = JobScorer(profile)
    reasoner = OpenAIReasoner(config.openai_api_key, config.openai_model, config.openai_base_url) if config.openai_ready else None
    source = _build_source(config)
    storage = Storage(config.database_path)
    run_day = date.today()

    processed_messages = 0
    parsed_jobs = 0
    duplicates_removed = 0
    new_entries: list[tuple[int, JobRecord, ScoreBreakdown]] = []
    completed_message_ids: list[str] = []

    try:
        with storage.transaction():
            for message in source.iter_messages():
                if storage.has_processed_alert(message.message_id):
                    continue
                processed_messages += 1
                try:
                    alert = parse_alert_email(
                        message.raw_bytes,
                        source_message_id=message.message_id,
                        received_at=message.received_at,
                    )
                except Exception:
                    failed_path = config.failed_dir / f"{message.message_id}.eml"
                    failed_path.write_bytes(message.raw_bytes)
                    (config.failed_dir / f"{message.message_id}.log").write_text(traceback.format_exc(), encoding="utf-8")
                    continue

                alert_id = storage.create_alert(alert.message_id, alert.alert_name, alert.received_at)
                parsed_jobs += len(alert.jobs)
                for job in alert.jobs:
                    job_id, is_new = storage.upsert_job(job, alert.received_at)
                    storage.link_job_to_alert(job_id, alert_id)
                    if is_new:
                        score = scorer.score(job)
                        score = _maybe_refine_with_ai(reasoner, job, score, profile, scorer)
                        storage.save_score(job_id, score)
                        new_entries.append((job_id, job, score))
                    else:
                        duplicates_removed += 1
                completed_message_ids.append(message.message_id)

            new_entries.sort(key=lambda item: item[2].total, reverse=True)
            subject, html = render_digest_html(run_day, new_entries, duplicates_removed)
            digest_path = config.output_dir / f"linkedin-digest-{run_day.isoformat()}.html"
            digest_path.write_text(html, encoding="utf-8")
            email_sent_at = None if dry_run else send_html_email(config, subject, html)
            storage.save_digest(
                run_date=run_day.isoformat(),
                job_ids=[job_id for job_id, _, _ in new_entries],
                email_subject=subject,
                html_path=str(digest_path),
                email_sent_at=email_sent_at,
            )

        if not dry_run:
            for message_id in completed_message_ids:
                source.mark_processed(message_id)
        return RunSummary(
            run_date=run_day.isoformat(),
            processed_messages=processed_messages,
            parsed_jobs=parsed_jobs,
            new_jobs=len(new_entries),
            duplicates_removed=duplicates_removed,
            digest_path=digest_path,
            email_sent_at=email_sent_at,
            subject=subject,
        )
    finally:
        storage.close()


def rebuild_latest_digest(config: Config, send_email: bool = False) -> RunSummary:
    config.ensure_directories()
    profile = load_profile(config.profile_path)
    scorer = JobScorer(profile)
    reasoner = OpenAIReasoner(config.openai_api_key, config.openai_model, config.openai_base_url) if config.openai_ready else None
    storage = Storage(config.database_path)

    try:
        latest = storage.latest_digest()
        if latest is None:
            raise ValueError("No saved digest exists yet, so there is nothing to rebuild.")
        job_ids = json.loads(latest["jobs_included"])
        entries: list[tuple[int, JobRecord, ScoreBreakdown]] = []
        for job_id, job in storage.fetch_jobs(job_ids):
            score = scorer.score(job)
            score = _maybe_refine_with_ai(reasoner, job, score, profile, scorer)
            storage.save_score(job_id, score)
            entries.append((job_id, job, score))
        entries.sort(key=lambda item: item[2].total, reverse=True)
        run_day = date.fromisoformat(str(latest["run_date"]))
        subject, html = render_digest_html(run_day, entries, duplicates_removed=0)
        digest_path = config.output_dir / f"linkedin-digest-{run_day.isoformat()}.html"
        digest_path.write_text(html, encoding="utf-8")
        email_sent_at = send_html_email(config, subject, html) if send_email else latest["email_sent_at"]
        storage.save_digest(
            run_date=run_day.isoformat(),
            job_ids=[job_id for job_id, _, _ in entries],
            email_subject=subject,
            html_path=str(digest_path),
            email_sent_at=email_sent_at,
        )
        return RunSummary(
            run_date=run_day.isoformat(),
            processed_messages=0,
            parsed_jobs=len(entries),
            new_jobs=len(entries),
            duplicates_removed=0,
            digest_path=digest_path,
            email_sent_at=email_sent_at,
            subject=subject,
        )
    finally:
        storage.close()
