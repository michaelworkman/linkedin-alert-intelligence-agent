from __future__ import annotations

import hashlib
import html
import re
from typing import TYPE_CHECKING
from urllib.parse import parse_qs, unquote, urlparse, urlunparse

if TYPE_CHECKING:
    from linkedin_alert_agent.models import JobRecord


STATE_ABBREVIATIONS = {
    "alabama": "AL",
    "alaska": "AK",
    "arizona": "AZ",
    "arkansas": "AR",
    "california": "CA",
    "colorado": "CO",
    "connecticut": "CT",
    "delaware": "DE",
    "district of columbia": "DC",
    "florida": "FL",
    "georgia": "GA",
    "hawaii": "HI",
    "idaho": "ID",
    "illinois": "IL",
    "indiana": "IN",
    "iowa": "IA",
    "kansas": "KS",
    "kentucky": "KY",
    "louisiana": "LA",
    "maine": "ME",
    "maryland": "MD",
    "massachusetts": "MA",
    "michigan": "MI",
    "minnesota": "MN",
    "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT",
    "nebraska": "NE",
    "nevada": "NV",
    "new hampshire": "NH",
    "new jersey": "NJ",
    "new mexico": "NM",
    "new york": "NY",
    "north carolina": "NC",
    "north dakota": "ND",
    "ohio": "OH",
    "oklahoma": "OK",
    "oregon": "OR",
    "pennsylvania": "PA",
    "rhode island": "RI",
    "south carolina": "SC",
    "south dakota": "SD",
    "tennessee": "TN",
    "texas": "TX",
    "utah": "UT",
    "vermont": "VT",
    "virginia": "VA",
    "washington": "WA",
    "west virginia": "WV",
    "wisconsin": "WI",
    "wyoming": "WY",
}

ACRONYMS = {"AI", "API", "B2B", "B2C", "CRM", "CX", "HR", "IC", "SEO", "UI", "UX", "VP"}
SMALL_WORDS = {"a", "an", "and", "at", "for", "in", "of", "on", "or", "the", "to", "with"}
WORK_MODE_PATTERNS = {
    "remote": "Remote",
    "hybrid": "Hybrid",
    "on-site": "On-site",
    "onsite": "On-site",
    "in office": "On-site",
}


def collapse_whitespace(value: str) -> str:
    cleaned = value or ""
    for _ in range(4):
        unescaped = html.unescape(cleaned)
        unescaped = re.sub(r"&amp;", "&", unescaped, flags=re.IGNORECASE)
        if unescaped == cleaned:
            break
        cleaned = unescaped
    return re.sub(r"\s+", " ", cleaned).strip()


def _smart_title_case(text: str) -> str:
    words: list[str] = []
    for index, raw_word in enumerate(text.split()):
        prefix_match = re.match(r"^([^A-Za-z0-9]*)(.*?)([^A-Za-z0-9]*)$", raw_word)
        if not prefix_match:
            words.append(raw_word)
            continue
        prefix, core, suffix = prefix_match.groups()
        if not core:
            words.append(raw_word)
            continue
        upper = core.upper()
        if upper in ACRONYMS:
            normalized = upper
        elif index > 0 and core.lower() in SMALL_WORDS:
            normalized = core.lower()
        else:
            normalized = core[:1].upper() + core[1:].lower()
        words.append(f"{prefix}{normalized}{suffix}")
    return " ".join(words)


def normalize_title(title: str) -> str:
    cleaned = collapse_whitespace(title)
    replacements = {
        r"\bsr\.?(?=\s|$)": "senior",
        r"\bjr\.?(?=\s|$)": "junior",
        r"\bsvp(?=\s|$)": "senior vice president",
        r"\bvp(?=\s|$)": "vice president",
        r"\bdir\.?(?=\s|$)": "director",
        r"\bux/ui\b": "ux ui",
        r"\bui/ux\b": "ui ux",
    }
    lowered = cleaned.lower()
    for pattern, replacement in replacements.items():
        lowered = re.sub(pattern, replacement, lowered, flags=re.IGNORECASE)
    return _smart_title_case(lowered)


def normalize_company(company: str) -> str:
    cleaned = collapse_whitespace(company)
    suffix_pattern = re.compile(
        r"(,?\s+(inc|inc\.|llc|l\.l\.c\.|corp|corp\.|corporation|co|co\.|company|ltd|ltd\.))+$",
        flags=re.IGNORECASE,
    )
    return suffix_pattern.sub("", cleaned).strip(" ,")


def infer_work_mode(*values: str) -> str:
    joined = " ".join(collapse_whitespace(value).lower() for value in values if value)
    for pattern, label in WORK_MODE_PATTERNS.items():
        if pattern in joined:
            return label
    return ""


def normalize_location(location: str) -> str:
    cleaned = collapse_whitespace(location)
    if not cleaned:
        return ""
    work_mode = infer_work_mode(cleaned)
    trimmed = re.sub(r",?\s*(united states|usa)$", "", cleaned, flags=re.IGNORECASE).strip(" ,-")
    if work_mode and trimmed.lower() == work_mode.lower():
        return work_mode
    parts = [collapse_whitespace(part) for part in trimmed.split(",") if collapse_whitespace(part)]
    if len(parts) >= 2:
        city = parts[0]
        region = parts[1]
        abbreviation = STATE_ABBREVIATIONS.get(region.lower(), region.upper() if len(region) == 2 else region)
        return f"{city}, {abbreviation}"
    return trimmed


def canonicalize_job_url(url: str) -> str:
    cleaned = collapse_whitespace(url)
    if not cleaned:
        return ""
    parsed = urlparse(cleaned)
    if "url" in parse_qs(parsed.query):
        nested = parse_qs(parsed.query).get("url", [""])[0]
        if nested:
            parsed = urlparse(unquote(nested))
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc.lower()
    path = re.sub(r"/+$", "", parsed.path)
    return urlunparse((scheme, netloc, path, "", "", ""))


def build_duplicate_key(job_url_canonical: str, title: str, company: str, location: str) -> str:
    if job_url_canonical:
        return hashlib.sha1(job_url_canonical.encode("utf-8")).hexdigest()
    fallback = "|".join(
        [
            collapse_whitespace(title).lower(),
            collapse_whitespace(company).lower(),
            collapse_whitespace(location).lower(),
        ]
    )
    return hashlib.sha1(fallback.encode("utf-8")).hexdigest()


def normalize_job_record(job: "JobRecord") -> "JobRecord":
    job.title_normalized = normalize_title(job.title_raw)
    job.company_normalized = normalize_company(job.company_raw)
    job.location_normalized = normalize_location(job.location_raw)
    job.job_url_canonical = canonicalize_job_url(job.job_url)
    if not job.work_mode:
        job.work_mode = infer_work_mode(job.location_raw, job.snippet, job.posted_text)
    job.duplicate_key = build_duplicate_key(
        job.job_url_canonical,
        job.title_normalized,
        job.company_normalized,
        job.location_normalized,
    )
    return job
