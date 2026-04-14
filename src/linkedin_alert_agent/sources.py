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
        processed_label_name: str = "",
        create_processed_label: bool = True,
        max_results: int = 25,
        mark_read: bool = False,
    ) -> None:
        self.client = client
        self.query = query
        self.label_names = label_names or []
        self.label_ids = label_ids or []
        self.processed_label_name = processed_label_name.strip()
        self.create_processed_label = create_processed_label
        self.max_results = max_results
        self.mark_read = mark_read
        self._processed_label_id: str | None = None

    def iter_messages(self) -> list[SourceMessage]:
        resolved_label_ids = self.client.resolve_label_ids(self.label_names, self.label_ids)
        query = self._with_processed_label_exclusion(self.query)
        listing = self.client.request_json(
            "GET",
            "/messages",
            params={
                "q": query,
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
        add_label_ids: list[str] = []
        remove_label_ids: list[str] = []

        if self.processed_label_name:
            add_label_ids.append(self._resolve_processed_label_id())
        if self.mark_read:
            remove_label_ids.append("UNREAD")

        if not add_label_ids and not remove_label_ids:
            return
        self.client.modify_message_labels(
            message_id,
            add_label_ids=add_label_ids,
            remove_label_ids=remove_label_ids,
        )

    def _resolve_processed_label_id(self) -> str:
        if self._processed_label_id:
            return self._processed_label_id
        if self.create_processed_label:
            self._processed_label_id = self.client.ensure_label_id(self.processed_label_name)
        else:
            resolved = self.client.resolve_label_ids([self.processed_label_name], [])
            if not resolved:
                raise ValueError(f"Could not resolve Gmail processed label {self.processed_label_name!r}.")
            self._processed_label_id = resolved[0]
        return self._processed_label_id

    def _with_processed_label_exclusion(self, query: str) -> str:
        if not self.processed_label_name:
            return query
        escaped_label = self.processed_label_name.replace('"', '\\"')
        exclusion = f'-label:"{escaped_label}"'
        return f"{query} {exclusion}".strip()
