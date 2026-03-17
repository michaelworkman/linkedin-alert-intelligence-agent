from __future__ import annotations

from datetime import date
from html import escape
import re

from linkedin_alert_agent.models import JobRecord, ScoreBreakdown


SNIPPET_NOISE_PATTERNS = (
    r"\bActively recruiting\b",
    r"\bGet the new LinkedIn desktop app\b",
)


def build_subject(run_date: date, total_new_jobs: int, top_matches: int) -> str:
    return f"Daily LinkedIn Digest - {total_new_jobs} new roles, {top_matches} strong matches ({run_date.isoformat()})"


def _job_facts(job: JobRecord) -> str:
    facts: list[str] = []
    if job.salary_text:
        facts.append(f"Salary: {escape(job.salary_text)}")
    if job.posted_text:
        facts.append(f"Posted: {escape(job.posted_text)}")
    if not facts:
        return ""
    items = "".join(f"<span class='job-fact'>{fact}</span>" for fact in facts)
    return f"<div class='job-facts'>{items}</div>"


def _display_location(job: JobRecord) -> str:
    location = job.location_normalized or ""
    work_mode = job.work_mode or ""
    if location and work_mode and work_mode.lower() not in location.lower():
        return f"{location} ({work_mode})"
    if location:
        return location
    if work_mode:
        return work_mode
    return "Location not listed"


def _clean_snippet(snippet: str) -> str:
    cleaned = snippet
    for pattern in SNIPPET_NOISE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" -;,.")
    return cleaned


def _job_why(score: ScoreBreakdown) -> str:
    rationale = score.rationale or "Matched your saved profile."
    items = [part.strip() for part in rationale.split(";") if part.strip()]
    if not items:
        items = ["Matched your saved profile."]
    rendered_items = "".join(f"<li>{escape(item)}</li>" for item in items)
    return f"<ul class='job-why'>{rendered_items}</ul>"


def _job_card(job_id: int, job: JobRecord, score: ScoreBreakdown, compact: bool = False) -> str:
    location = _display_location(job)
    cleaned_snippet = _clean_snippet(job.snippet) if job.snippet else ""
    snippet = escape(cleaned_snippet) if cleaned_snippet else ""
    base = (
        f"<div class='job-card'>"
        f"<div class='job-title'><a href='{escape(job.job_url)}'>{escape(job.title_normalized or job.title_raw)}</a></div>"
        f"<div class='job-meta'><strong>{escape(job.company_normalized or job.company_raw or 'Unknown company')}</strong></div>"
        f"<div class='job-location'>{escape(location)}</div>"
        f"{_job_facts(job)}"
        f"{_job_why(score)}"
    )
    if snippet and not compact:
        base += f"<div class='job-snippet'>{snippet}</div>"
    base += "</div>"
    return base


def _render_section(title: str, entries: list[tuple[int, JobRecord, ScoreBreakdown]], compact: bool = False) -> str:
    if not entries:
        return ""
    cards = "".join(_job_card(job_id, job, score, compact=compact) for job_id, job, score in entries)
    return f"<section><h2>{escape(title)}</h2>{cards}</section>"


def render_digest_html(
    run_date: date,
    entries: list[tuple[int, JobRecord, ScoreBreakdown]],
    duplicates_removed: int,
) -> tuple[str, str]:
    visible_entries = [entry for entry in entries if entry[2].classification != "Filtered out"]
    top_matches = [entry for entry in visible_entries if entry[2].classification == "Top matches"]
    worth_a_look = [entry for entry in visible_entries if entry[2].classification == "Worth a look"]
    low_priority = [entry for entry in visible_entries if entry[2].classification == "Low priority"]

    subject = build_subject(run_date, len(visible_entries), len(top_matches))
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{escape(subject)}</title>
  <style>
    body {{
      font-family: Georgia, "Times New Roman", serif;
      background: linear-gradient(180deg, #f7f2ea 0%, #fcfbf8 100%);
      color: #1e1d1a;
      margin: 0;
      padding: 32px 18px;
    }}
    .wrap {{
      max-width: 880px;
      margin: 0 auto;
      background: rgba(255, 255, 255, 0.92);
      border: 1px solid #ded5c8;
      border-radius: 18px;
      padding: 28px;
      box-shadow: 0 18px 50px rgba(52, 42, 31, 0.08);
    }}
    h1, h2 {{
      font-family: "Avenir Next", "Trebuchet MS", sans-serif;
      letter-spacing: 0.02em;
    }}
    h1 {{
      margin-top: 0;
      font-size: 30px;
    }}
    h2 {{
      margin-top: 28px;
      font-size: 20px;
      border-bottom: 1px solid #eee1cf;
      padding-bottom: 8px;
    }}
    .summary {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 12px;
      margin: 18px 0 24px;
    }}
    .summary-card {{
      background: #f5eee1;
      border-radius: 14px;
      padding: 14px 16px;
    }}
    .summary-label {{
      font-size: 12px;
      text-transform: uppercase;
      color: #6a5c49;
      margin-bottom: 4px;
    }}
    .summary-value {{
      font-size: 26px;
      font-weight: 700;
    }}
    .job-card {{
      border: 1px solid #eadfce;
      background: #fffdfa;
      border-radius: 14px;
      padding: 14px 16px;
      margin-bottom: 12px;
    }}
    .job-title {{
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 4px;
    }}
    .job-title a {{
      color: #8a3b12;
      text-decoration: none;
    }}
    .job-meta {{
      color: #5f594f;
      font-size: 14px;
      margin-bottom: 2px;
    }}
    .job-location {{
      color: #7d6c57;
      font-size: 14px;
      margin-bottom: 8px;
    }}
    .job-why {{
      color: #1e1d1a;
      font-size: 15px;
      margin: 0 0 8px 18px;
      padding: 0;
    }}
    .job-why li {{
      margin-bottom: 8px;
    }}
    .job-facts {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 8px;
    }}
    .job-fact {{
      background: #f5eee1;
      border-radius: 999px;
      color: #5f594f;
      font-size: 12px;
      padding: 5px 10px;
    }}
    .job-snippet {{
      font-size: 14px;
      color: #4b463f;
      margin-bottom: 8px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>LinkedIn Alert Intelligence Agent</h1>
    <p>{escape(run_date.strftime('%A, %B %d, %Y'))}</p>
    <div class="summary">
      <div class="summary-card"><div class="summary-label">New jobs</div><div class="summary-value">{len(visible_entries)}</div></div>
      <div class="summary-card"><div class="summary-label">Top matches</div><div class="summary-value">{len(top_matches)}</div></div>
    </div>
    {_render_section("Top matches", top_matches)}
    {_render_section("Worth a look", worth_a_look)}
    {_render_section("Low priority", low_priority, compact=True)}
  </div>
</body>
</html>
"""
    return subject, html
