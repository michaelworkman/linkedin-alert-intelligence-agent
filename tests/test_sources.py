from __future__ import annotations

import base64
import unittest

from linkedin_alert_agent.sources import GmailApiMessageSource


class FakeGmailClient:
    def __init__(self) -> None:
        self.messages_query: dict | None = None
        self.modified_messages: list[dict] = []
        self.ensured_label_names: list[str] = []

    def resolve_label_ids(self, label_names: list[str], fallback_label_ids: list[str]) -> list[str]:
        return ["Label_Alerts", *fallback_label_ids] if label_names else fallback_label_ids

    def request_json(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        payload: dict | None = None,
    ) -> dict:
        _ = payload
        if method == "GET" and path == "/messages":
            self.messages_query = params or {}
            return {"messages": [{"id": "msg-1"}]}
        if method == "GET" and path == "/messages/msg-1":
            return {
                "raw": base64.urlsafe_b64encode(b"Subject: Test\r\n\r\nHello").decode("utf-8").rstrip("="),
                "internalDate": "1715083200000",
            }
        raise AssertionError(f"Unexpected request: {method} {path} {params} {payload}")

    def ensure_label_id(self, label_name: str) -> str:
        self.ensured_label_names.append(label_name)
        return "Label_Processed"

    def modify_message_labels(
        self,
        message_id: str,
        add_label_ids: list[str] | None = None,
        remove_label_ids: list[str] | None = None,
    ) -> dict:
        self.modified_messages.append(
            {
                "message_id": message_id,
                "add_label_ids": add_label_ids or [],
                "remove_label_ids": remove_label_ids or [],
            }
        )
        return {}


class SourceTests(unittest.TestCase):
    def test_iter_messages_excludes_already_processed_label(self) -> None:
        client = FakeGmailClient()
        source = GmailApiMessageSource(
            client=client,
            query='from:(jobs-noreply@linkedin.com) newer_than:2d',
            label_names=["LinkedIn Alerts"],
            processed_label_name="LinkedIn Digest Processed",
        )

        messages = source.iter_messages()

        self.assertEqual(len(messages), 1)
        self.assertEqual(
            client.messages_query,
            {
                "q": 'from:(jobs-noreply@linkedin.com) newer_than:2d -label:"LinkedIn Digest Processed"',
                "labelIds": ["Label_Alerts"],
                "maxResults": 25,
            },
        )

    def test_mark_processed_adds_checkpoint_label_and_clears_unread(self) -> None:
        client = FakeGmailClient()
        source = GmailApiMessageSource(
            client=client,
            query="from:(jobs-noreply@linkedin.com)",
            processed_label_name="LinkedIn Digest Processed",
            mark_read=True,
        )

        source.mark_processed("msg-1")

        self.assertEqual(client.ensured_label_names, ["LinkedIn Digest Processed"])
        self.assertEqual(
            client.modified_messages,
            [
                {
                    "message_id": "msg-1",
                    "add_label_ids": ["Label_Processed"],
                    "remove_label_ids": ["UNREAD"],
                }
            ],
        )


if __name__ == "__main__":
    unittest.main()
