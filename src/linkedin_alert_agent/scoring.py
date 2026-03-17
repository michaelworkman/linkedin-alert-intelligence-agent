from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from linkedin_alert_agent.models import JobRecord, ScoreBreakdown


DEFAULT_PROFILE: dict[str, Any] = {
    "target_titles": [],
    "target_locations": [],
    "remote_ok": True,
    "preferred_seniority_keywords": [
        "director",
        "head",
        "lead",
        "manager",
        "principal",
    ],
    "must_have_keywords": [],
    "emphasis_keywords": [],
    "positive_keywords": [],
    "avoid_keywords": [],
    "hard_exclude_keywords": [],
    "company_quality_signals": [],
    "core_function_keywords": [
        "design",
        "brand",
        "ux",
        "ui",
        "experience",
        "editorial",
        "storytelling",
        "visual",
        "content strategy",
        "art direction",
        "digital",
    ],
    "classification_thresholds": {
        "top_match": 75,
        "worth_a_look": 55,
        "low_priority": 35,
    },
}

LEADERSHIP_KEYWORDS = {
    "leadership",
    "lead",
    "director",
    "head",
    "vp",
    "vice president",
    "manages",
    "manage",
    "team",
    "strategy",
    "roadmap",
    "cross-functional",
}

SENIORITY_TITLE_KEYWORDS = ("director", "head", "lead", "principal", "manager", "vice president", "vp")

JUNIOR_PATTERNS = (
    "assistant",
    "associate",
    "coordinator",
    "junior",
    "intern",
    "designer ii",
    "designer i",
)

FUNCTION_LABELS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("product", ("product",)),
    ("marketing", ("marketing",)),
    ("brand", ("brand",)),
    ("UX", ("ux", "ui", "experience")),
    ("design", ("design", "creative", "visual", "editorial", "art direction")),
)

RATIONALE_PREFIX_ORDER = (
    "Strong title fit",
    "Relevant senior",
    "Adjacent leadership role",
    "Relevant ",
    "Priority emphasis",
    "Target location",
    "Remote role is allowed",
    "Alignment keywords",
    "Must-have signals",
    "Company or industry signal",
    "Salary information included",
    "Leadership and scope language present",
)


def load_profile(path: Path) -> dict[str, Any]:
    if not path.exists():
        return DEFAULT_PROFILE.copy()
    with path.open("r", encoding="utf-8") as handle:
        loaded = json.load(handle)
    merged = DEFAULT_PROFILE.copy()
    merged.update(loaded)
    merged["classification_thresholds"] = {
        **DEFAULT_PROFILE["classification_thresholds"],
        **loaded.get("classification_thresholds", {}),
    }
    return merged


def _contains_any(haystack: str, candidates: list[str]) -> list[str]:
    lowered = haystack.lower()
    return [candidate for candidate in candidates if candidate.lower() in lowered]


def _contains_exact_terms(haystack: str, candidates: list[str]) -> list[str]:
    lowered = haystack.lower()
    hits: list[str] = []
    for candidate in candidates:
        pattern = r"(?<!\w)" + re.escape(candidate.lower()) + r"(?!\w)"
        if re.search(pattern, lowered):
            hits.append(candidate)
    return hits


def _describe_function_focus(text: str) -> str | None:
    lowered = text.lower()
    labels = [label for label, keywords in FUNCTION_LABELS if any(keyword in lowered for keyword in keywords)]
    if not labels:
        return None
    return "/".join(labels[:2])


def _prioritize_notes(notes: list[str]) -> list[str]:
    def note_rank(note: str) -> tuple[int, int]:
        for index, prefix in enumerate(RATIONALE_PREFIX_ORDER):
            if note.startswith(prefix):
                return index, 0
        return len(RATIONALE_PREFIX_ORDER), 0

    return sorted(notes, key=note_rank)


class JobScorer:
    def __init__(self, profile: dict[str, Any]) -> None:
        self.profile = profile
        self.thresholds = profile.get("classification_thresholds", DEFAULT_PROFILE["classification_thresholds"])

    def classify(self, total: int) -> str:
        if total >= int(self.thresholds["top_match"]):
            return "Top matches"
        if total >= int(self.thresholds["worth_a_look"]):
            return "Worth a look"
        if total >= int(self.thresholds["low_priority"]):
            return "Low priority"
        return "Filtered out"

    def score(self, job: JobRecord) -> ScoreBreakdown:
        searchable = " ".join(
            part
            for part in [
                job.title_normalized,
                job.company_normalized,
                job.location_normalized,
                job.snippet,
                job.posted_text,
                job.salary_text,
                job.work_mode,
            ]
            if part
        )
        searchable_lower = searchable.lower()
        title_lower = job.title_normalized.lower()
        notes: list[str] = []
        core_keywords = self.profile.get("core_function_keywords", DEFAULT_PROFILE["core_function_keywords"])
        emphasis_keywords = self.profile.get("emphasis_keywords", DEFAULT_PROFILE["emphasis_keywords"])
        hard_exclude_keywords = self.profile.get("hard_exclude_keywords", DEFAULT_PROFILE["hard_exclude_keywords"])
        preferred_seniority_keywords = self.profile.get(
            "preferred_seniority_keywords",
            DEFAULT_PROFILE["preferred_seniority_keywords"],
        )
        has_core_function_title = any(keyword.lower() in title_lower for keyword in core_keywords)
        has_core_function_anywhere = any(keyword.lower() in searchable_lower for keyword in core_keywords)
        has_senior_title = any(keyword in title_lower for keyword in SENIORITY_TITLE_KEYWORDS)
        has_preferred_seniority_title = any(
            keyword.lower() in title_lower for keyword in preferred_seniority_keywords
        )
        hard_exclude_hits = _contains_exact_terms(searchable, hard_exclude_keywords)

        if hard_exclude_hits:
            reason = f"Filtered out because it references {hard_exclude_hits[0]}."
            return ScoreBreakdown(
                total=0,
                title_score=0,
                location_score=0,
                seniority_score=0,
                alignment_score=0,
                company_quality_score=0,
                compensation_score=0,
                penalty_score=-100,
                notes=[reason],
                rationale=reason,
                classification="Filtered out",
            )

        title_score = 0
        title_hits = _contains_any(job.title_normalized, self.profile.get("target_titles", []))
        if title_hits:
            title_score = 32
            notes.append(f"Strong title fit: {title_hits[0]}")
        elif has_core_function_title and has_preferred_seniority_title:
            title_score = 22
            function_focus = _describe_function_focus(job.title_normalized)
            if function_focus:
                notes.append(f"Relevant senior {function_focus} title")
            else:
                notes.append("Relevant senior role in a target function")
        elif has_core_function_title and has_senior_title:
            title_score = 18
            function_focus = _describe_function_focus(job.title_normalized)
            if function_focus:
                notes.append(f"Adjacent leadership role in {function_focus}")
            else:
                notes.append("Adjacent leadership role in a target function")
        elif has_core_function_title:
            title_score = 10
            function_focus = _describe_function_focus(job.title_normalized)
            if function_focus:
                notes.append(f"Relevant {function_focus} function")
            else:
                notes.append("Relevant target function")

        location_score = 0
        target_locations = self.profile.get("target_locations", [])
        if _contains_any(job.location_normalized or job.work_mode, target_locations):
            location_score = 20
            notes.append(f"Target location: {job.location_normalized or job.work_mode}")
        elif self.profile.get("remote_ok", True) and job.work_mode == "Remote":
            location_score = 15
            notes.append("Remote role is allowed")
        elif job.location_normalized:
            location_score = -15
            notes.append(f"Outside target geography: {job.location_normalized}")

        seniority_score = 0
        leadership_hits = [keyword for keyword in LEADERSHIP_KEYWORDS if keyword in searchable_lower]
        if leadership_hits:
            seniority_score = min(20, 11 + (len(leadership_hits) * 2))
            notes.append("Leadership and scope language present")
            if has_preferred_seniority_title:
                seniority_score = min(24, seniority_score + 2)

        alignment_score = 0
        emphasis_hits = _contains_any(searchable, emphasis_keywords)
        positive_hits = _contains_any(searchable, self.profile.get("positive_keywords", []))
        must_have_hits = _contains_any(searchable, self.profile.get("must_have_keywords", []))
        if emphasis_hits:
            alignment_score += min(12, 6 + (len(emphasis_hits) * 2))
            notes.append(f"Priority emphasis: {', '.join(emphasis_hits[:2])}")
        if positive_hits:
            alignment_score += min(10, 4 + (len(positive_hits) * 2))
            notes.append(f"Alignment keywords: {', '.join(positive_hits[:3])}")
        if must_have_hits:
            alignment_score += min(5, len(must_have_hits))
            notes.append(f"Must-have signals: {', '.join(must_have_hits[:2])}")

        company_quality_score = 0
        company_hits = _contains_any(searchable, self.profile.get("company_quality_signals", []))
        if company_hits:
            company_quality_score = min(10, 4 + len(company_hits) * 2)
            notes.append(f"Company or industry signal: {company_hits[0]}")

        compensation_score = 0
        if re.search(r"\$\s?\d", job.salary_text):
            compensation_score = 10
            notes.append("Salary information included")

        penalty_score = 0
        avoid_hits = _contains_any(searchable, self.profile.get("avoid_keywords", []))
        if avoid_hits:
            penalty_score -= min(30, 12 + (len(avoid_hits) * 4))
            notes.append(f"Avoid signal: {avoid_hits[0]}")
        if any(pattern in searchable_lower for pattern in JUNIOR_PATTERNS):
            penalty_score -= 20
            notes.append("Below target seniority")
        if "contract" in searchable_lower or "temporary" in searchable_lower or "temp" in searchable_lower:
            penalty_score -= 15
            notes.append("Contract or temporary language present")
        if has_senior_title and not has_core_function_anywhere and not title_hits:
            penalty_score -= 18
            notes.append("Leadership role appears outside target design or creative function")

        total = max(
            0,
            min(
                100,
                title_score
                + location_score
                + seniority_score
                + alignment_score
                + company_quality_score
                + compensation_score
                + penalty_score,
            ),
        )
        classification = self.classify(total)
        positive_notes = [note for note in notes if not note.lower().startswith("avoid signal")]
        positive_notes = _prioritize_notes(positive_notes)
        rationale_bits = positive_notes[:3] if positive_notes else notes[:2]
        rationale = "; ".join(rationale_bits) if rationale_bits else "Limited match against the current profile."

        return ScoreBreakdown(
            total=total,
            title_score=title_score,
            location_score=location_score,
            seniority_score=seniority_score,
            alignment_score=alignment_score,
            company_quality_score=company_quality_score,
            compensation_score=compensation_score,
            penalty_score=penalty_score,
            notes=notes,
            rationale=rationale,
            classification=classification,
        )
