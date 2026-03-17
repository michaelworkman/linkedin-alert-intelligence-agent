from __future__ import annotations

import base64
from datetime import datetime, timezone
from pathlib import Path

from linkedin_alert_agent.gmail import GmailApiClient
from linkedin_alert_agent.models import SourceMessage


class FilesystemMessageSource:
    def __init__(self, input_dir: Path) -> None:
        self.input_dir = input_dir

    def iter_messages(self) -> list[SourceMessage]:
        if not self.input_dir.exists():
            return []
        messages: list[SourceMessage] = []
        for path in sorted(self.input_dir.glob("*.eml")):
            messages.append(
                SourceMessage(
                    message_id=path.stem,
                    raw_bytes=path.read_bytes(),
                    received_at=datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc),
                    origin="filesystem",
                )
            )
        return messages

    def mark_processed(self, message_id: str) -> None:
        _ = message_id


class GmailApiMessageSource:
    def __init__(
        self,
        client: GmailApiClient,
        query: str,
        label_names: list[str] | None = None,
        label_ids: list[str] | None = None,
        max_results: int = 25,
        mark_read: bool = False,
    ) -> None:
        self.client = client
        self.query = query
        self.label_names = label_names or []
        self.label_ids = label_ids or []
        self.max_results = max_results
        self.mark_read = mark_read

    def iter_messages(self) -> list[SourceMessage]:
        resolved_label_ids = self.client.resolve_label_ids(self.label_names, self.label_ids)
        listing = self.client.request_json(
            "GET",
            "/messages",
            params={
                "q": self.query,
                "labelIds": resolved_label_ids,
                "maxResults": self.max_results,
            },
        )
        results: list[SourceMessage] = []
        for item in listing.get("messages", []):
            message_id = item["id"]
            message = self.client.request_json("GET", f"/messages/{message_id}", params={"format": "raw"})
            raw_message = message.get("raw", "")
            padding = "=" * (-len(raw_message) % 4)
            raw_bytes = base64.urlsafe_b64decode(raw_message + padding)
            internal_date = message.get("internalDate")
            received_at = None
            if internal_date:
                received_at = datetime.fromtimestamp(int(internal_date) / 1000, tz=timezone.utc)
            results.append(
                SourceMessage(
                    message_id=message_id,
                    raw_bytes=raw_bytes,
                    received_at=received_at,
                    origin="gmail",
                )
            )
        return results

    def mark_processed(self, message_id: str) -> None:
        if not self.mark_read:
            return
        self.client.request_json(
            "POST",
            f"/messages/{message_id}/modify",
            payload={"removeLabelIds": ["UNREAD"]},
        )
