from __future__ import annotations

import json
from urllib.request import Request, urlopen

from linkedin_alert_agent.models import JobRecord, ScoreBreakdown


class OpenAIReasoner:
    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        self.api_key = api_key
        self.model = model
        self.base_url = base_url

    def refine(self, job: JobRecord, score: ScoreBreakdown, profile: dict) -> dict | None:
        schema = {
            "type": "object",
            "properties": {
                "score_adjustment": {"type": "integer", "minimum": -10, "maximum": 10},
                "matching_signals": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "caution_signals": {
                    "type": "array",
                    "items": {"type": "string"},
                },
                "rationale": {"type": "string"},
            },
            "required": ["score_adjustment", "matching_signals", "caution_signals", "rationale"],
            "additionalProperties": False,
        }
        payload = {
            "model": self.model,
            "input": [
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "You are a precise job-ranking assistant. Use the profile strictly. Keep the adjustment small and explain it briefly.",
                        }
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": json.dumps(
                                {
                                    "profile": profile,
                                    "job": {
                                        "title": job.title_normalized,
                                        "company": job.company_normalized,
                                        "location": job.location_normalized,
                                        "work_mode": job.work_mode,
                                        "snippet": job.snippet,
                                        "posted_text": job.posted_text,
                                        "salary_text": job.salary_text,
                                    },
                                    "deterministic_score": {
                                        "total": score.total,
                                        "classification": score.classification,
                                        "notes": score.notes,
                                    },
                                }
                            ),
                        }
                    ],
                },
            ],
            "text": {
                "format": {
                    "type": "json_schema",
                    "name": "job_rank_adjustment",
                    "strict": True,
                    "schema": schema,
                }
            },
        }
        request = Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        with urlopen(request, timeout=45) as response:
            raw = json.loads(response.read().decode("utf-8"))
        text = self._extract_text(raw)
        if not text:
            return None
        return json.loads(text)

    def _extract_text(self, payload: dict) -> str:
        output_text = payload.get("output_text")
        if isinstance(output_text, str) and output_text.strip():
            return output_text
        for item in payload.get("output", []):
            for content in item.get("content", []):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    return str(content["text"])
        return ""
