from __future__ import annotations

import hashlib
import re
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

from linkedin_alert_agent.models import JobRecord, ParsedAlert
from linkedin_alert_agent.normalize import collapse_whitespace, infer_work_mode, normalize_job_record


GENERIC_LINK_TEXT = {
    "apply now",
    "learn more",
    "linkedin",
    "open role",
    "see all jobs",
    "see more jobs",
    "show more",
    "view all jobs",
    "view job",
}

POSTED_PATTERNS = re.compile(r"\b(today|just now|\d+\s+(minute|hour|day|week|month)s?\s+ago|reposted)\b", re.IGNORECASE)
SALARY_PATTERNS = re.compile(r"\$\s?\d")
LOCATION_HINTS = ("remote", "hybrid", "on-site", "onsite", "metropolitan area", "united states")
JOB_URL_PATTERNS = ("/jobs/view/", "/jobs/collections/", "/jobs/search/")
BLOCK_BREAK_TAGS = {"br", "div", "li", "p", "section", "table", "td", "tr"}


class LinkedInHTMLTokenParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tokens: list[dict[str, str]] = []
        self._text_parts: list[str] = []
        self._current_link: dict[str, str] | None = None
        self._current_link_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in BLOCK_BREAK_TAGS:
            self._flush_text()
        if tag == "a":
            self._flush_text()
            attributes = dict(attrs)
            self._current_link = {"type": "link", "href": attributes.get("href", "") or ""}
            self._current_link_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._current_link is not None:
            text = collapse_whitespace(" ".join(self._current_link_parts))
            if text:
                self._current_link["text"] = text
                self.tokens.append(self._current_link)
            self._current_link = None
            self._current_link_parts = []
        if tag in BLOCK_BREAK_TAGS:
            self._flush_text()

    def handle_data(self, data: str) -> None:
        cleaned = collapse_whitespace(data)
        if not cleaned:
            return
        if self._current_link is not None:
            self._current_link_parts.append(cleaned)
        else:
            self._text_parts.append(cleaned)

    def _flush_text(self) -> None:
        if not self._text_parts:
            return
        text = collapse_whitespace(" ".join(self._text_parts))
        if text:
            self.tokens.append({"type": "text", "text": text})
        self._text_parts = []


def _extract_message_body(message, content_type: str) -> str:
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() != content_type:
                continue
            if part.get_content_disposition() == "attachment":
                continue
            try:
                content = part.get_content()
            except LookupError:
                payload = part.get_payload(decode=True) or b""
                charset = part.get_content_charset() or "utf-8"
                content = payload.decode(charset, errors="replace")
            return content if isinstance(content, str) else content.decode("utf-8", errors="replace")
        return ""
    if message.get_content_type() != content_type:
        return ""
    content = message.get_content()
    return content if isinstance(content, str) else content.decode("utf-8", errors="replace")


def _is_job_link(href: str, text: str) -> bool:
    if not href:
        return False
    lowered_href = href.lower()
    lowered_text = collapse_whitespace(text).lower()
    if lowered_text in GENERIC_LINK_TEXT:
        return False
    return "linkedin.com" in lowered_href and any(pattern in lowered_href for pattern in JOB_URL_PATTERNS)


def _is_probable_job_title(title: str) -> bool:
    cleaned = collapse_whitespace(title)
    if len(cleaned) < 4 or len(cleaned) > 120:
        return False
    if cleaned.lower() in GENERIC_LINK_TEXT:
        return False
    return bool(re.search(r"[A-Za-z]", cleaned))


def _split_block_text(values: list[str]) -> list[str]:
    parts: list[str] = []
    for value in values:
        for chunk in re.split(r"\s+[|·•]\s+|\s{2,}", value):
            cleaned = collapse_whitespace(chunk)
            if cleaned:
                parts.append(cleaned)
    deduped: list[str] = []
    seen: set[str] = set()
    for part in parts:
        lowered = part.lower()
        if lowered not in seen:
            seen.add(lowered)
            deduped.append(part)
    return deduped


def _looks_like_location(value: str) -> bool:
    lowered = value.lower()
    if any(hint in lowered for hint in LOCATION_HINTS):
        return True
    if re.search(r",\s*[A-Z]{2}\b", value):
        return True
    if "," in value and any(word in lowered for word in ("massachusetts", "new york", "california", "texas")):
        return True
    return False


def _build_job_from_block(title: str, job_url: str, block_values: list[str]) -> JobRecord:
    company = ""
    location = ""
    snippet_parts: list[str] = []
    posted_text = ""
    salary_text = ""

    for value in _split_block_text(block_values)[:10]:
        lowered = value.lower()
        if lowered in GENERIC_LINK_TEXT:
            continue
        if not company and not _looks_like_location(value) and not POSTED_PATTERNS.search(value) and not SALARY_PATTERNS.search(value):
            company = value
            continue
        if not location and _looks_like_location(value):
            location = value
            continue
        if not salary_text and SALARY_PATTERNS.search(value):
            salary_text = value
            continue
        if not posted_text and POSTED_PATTERNS.search(value):
            posted_text = value
            continue
        if len(value) > 18:
            snippet_parts.append(value)

    snippet = " ".join(snippet_parts[:2])
    job = JobRecord(
        title_raw=title,
        company_raw=company,
        location_raw=location,
        job_url=job_url,
        snippet=snippet,
        salary_text=salary_text,
        posted_text=posted_text,
        work_mode=infer_work_mode(location, snippet, " ".join(block_values)),
    )
    extracted_fields = [job.title_raw, job.company_raw, job.location_raw, job.snippet, job.posted_text, job.salary_text]
    job.parse_confidence = round(sum(1 for value in extracted_fields if value) / len(extracted_fields), 2)
    return normalize_job_record(job)


def extract_jobs_from_html(html: str) -> list[JobRecord]:
    parser = LinkedInHTMLTokenParser()
    parser.feed(html)
    parser.close()
    parser._flush_text()

    jobs: list[JobRecord] = []
    for index, token in enumerate(parser.tokens):
        if token.get("type") != "link":
            continue
        href = token.get("href", "")
        title = token.get("text", "")
        if not _is_job_link(href, title) or not _is_probable_job_title(title):
            continue
        block_values: list[str] = []
        scan_index = index + 1
        while scan_index < len(parser.tokens):
            next_token = parser.tokens[scan_index]
            if next_token.get("type") == "link" and _is_job_link(next_token.get("href", ""), next_token.get("text", "")):
                break
            text = next_token.get("text", "")
            if text:
                block_values.append(text)
            scan_index += 1
        jobs.append(_build_job_from_block(title, href, block_values))
    return jobs


def extract_jobs_from_text(text: str) -> list[JobRecord]:
    jobs: list[JobRecord] = []
    for block in re.split(r"\n\s*\n", text):
        url_match = re.search(r"(https?://[^\s>]+linkedin\.com[^\s>]+/jobs/[^\s>]+)", block)
        if not url_match:
            continue
        lines = [collapse_whitespace(line) for line in block.splitlines() if collapse_whitespace(line)]
        title = lines[0] if lines else "Unknown role"
        jobs.append(_build_job_from_block(title, url_match.group(1), lines[1:]))
    return jobs


def _derive_alert_name(subject: str) -> str:
    cleaned = collapse_whitespace(subject)
    prefixes = [
        "Jobs alert for",
        "Job alert for",
        "LinkedIn Job Alerts:",
        "LinkedIn Jobs:",
        "LinkedIn",
    ]
    for prefix in prefixes:
        if cleaned.lower().startswith(prefix.lower()):
            return cleaned[len(prefix) :].strip(" :-")
    return cleaned or "LinkedIn Alert"


def parse_alert_email(raw_bytes: bytes, source_message_id: str | None = None, received_at: datetime | None = None) -> ParsedAlert:
    message = BytesParser(policy=policy.default).parsebytes(raw_bytes)
    subject = collapse_whitespace(str(message.get("Subject", "LinkedIn Job Alert")))
    header_message_id = collapse_whitespace(str(message.get("Message-ID", ""))).strip("<>")
    parsed_date = None
    if message.get("Date"):
        try:
            parsed_date = parsedate_to_datetime(str(message.get("Date")))
        except (TypeError, ValueError):
            parsed_date = None
    resolved_received_at = received_at or parsed_date or datetime.now(timezone.utc)
    if resolved_received_at.tzinfo is None:
        resolved_received_at = resolved_received_at.replace(tzinfo=timezone.utc)

    html_body = _extract_message_body(message, "text/html")
    text_body = _extract_message_body(message, "text/plain")
    extracted_jobs = extract_jobs_from_html(html_body) if html_body else extract_jobs_from_text(text_body)

    deduped_jobs: list[JobRecord] = []
    seen_keys: set[str] = set()
    for job in extracted_jobs:
        if not job.duplicate_key or job.duplicate_key in seen_keys:
            continue
        seen_keys.add(job.duplicate_key)
        job.source_alert_name = _derive_alert_name(subject)
        job.source_email_timestamp = resolved_received_at.astimezone(timezone.utc).isoformat()
        deduped_jobs.append(job)

    derived_message_id = source_message_id or header_message_id
    if not derived_message_id:
        derived_message_id = hashlib.sha1(raw_bytes).hexdigest()

    return ParsedAlert(
        message_id=derived_message_id,
        alert_name=_derive_alert_name(subject),
        received_at=resolved_received_at,
        jobs=deduped_jobs,
        subject=subject,
    )
