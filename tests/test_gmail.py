from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from linkedin_alert_agent.gmail import (
    GMAIL_MODIFY_SCOPE,
    GMAIL_READONLY_SCOPE,
    GMAIL_SEND_SCOPE,
    GmailApiClient,
    GmailAuthError,
    GoogleOAuthClientConfig,
    GoogleOAuthManager,
    GoogleTokenBundle,
    load_google_client_config,
)


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        _ = exc_type, exc, tb


class GmailTests(unittest.TestCase):
    def test_load_google_client_config_reads_installed_client_json(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            secrets_path = Path(temp_dir) / "google-oauth-client.json"
            secrets_path.write_text(
                json.dumps(
                    {
                        "installed": {
                            "client_id": "abc.apps.googleusercontent.com",
                            "client_secret": "secret-value",
                            "auth_uri": "https://accounts.google.com/o/oauth2/v2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": ["http://127.0.0.1:8765/callback"],
                        }
                    }
                ),
                encoding="utf-8",
            )

            client_config = load_google_client_config(
                client_id="",
                client_secret="",
                redirect_uri="",
                client_secrets_path=secrets_path,
            )

            self.assertEqual(client_config.client_id, "abc.apps.googleusercontent.com")
            self.assertEqual(client_config.redirect_uri, "http://127.0.0.1:8765/callback")

    def test_refresh_token_updates_access_token_and_expiry(self) -> None:
        requests: list[bytes] = []

        def fake_opener(request, timeout=30):  # noqa: ARG001
            requests.append(request.data or b"")
            return FakeResponse(
                {
                    "access_token": "fresh-token",
                    "expires_in": 3600,
                    "scope": GMAIL_READONLY_SCOPE,
                    "token_type": "Bearer",
                }
            )

        manager = GoogleOAuthManager(
            client_config=GoogleOAuthClientConfig(
                client_id="abc.apps.googleusercontent.com",
                client_secret="shh",
                redirect_uri="http://127.0.0.1:8765/callback",
            ),
            token_path=Path("/tmp/test-google-token.json"),
            opener=fake_opener,
        )
        refreshed = manager.refresh_token(
            GoogleTokenBundle(
                access_token="old-token",
                refresh_token="refresh-me",
                scopes=[GMAIL_READONLY_SCOPE],
                expiry_utc="2000-01-01T00:00:00+00:00",
            )
        )

        self.assertEqual(refreshed.access_token, "fresh-token")
        self.assertEqual(refreshed.refresh_token, "refresh-me")
        self.assertTrue(refreshed.expiry_utc)
        self.assertTrue(any(b"refresh_token=refresh-me" in request for request in requests))

    def test_resolve_label_ids_from_names(self) -> None:
        client = GmailApiClient(access_token_supplier=lambda: "token")
        client.list_labels = lambda: [  # type: ignore[method-assign]
            {"id": "Label_1", "name": "LinkedIn Alerts", "type": "user"},
            {"id": "INBOX", "name": "INBOX", "type": "system"},
        ]

        resolved = client.resolve_label_ids(["LinkedIn Alerts"], ["INBOX"])

        self.assertEqual(resolved, ["Label_1", "INBOX"])

    def test_get_token_requires_matching_scopes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            token_path = Path(temp_dir) / "google-token.json"
            token_path.write_text(
                json.dumps(
                    GoogleTokenBundle(
                        access_token="access",
                        refresh_token="refresh",
                        scopes=[GMAIL_READONLY_SCOPE],
                    ).to_payload()
                ),
                encoding="utf-8",
            )
            manager = GoogleOAuthManager(
                client_config=GoogleOAuthClientConfig(
                    client_id="abc.apps.googleusercontent.com",
                    client_secret="",
                    redirect_uri="http://127.0.0.1:8765/callback",
                ),
                token_path=token_path,
            )
            with self.assertRaises(GmailAuthError):
                manager.get_token([GMAIL_MODIFY_SCOPE])

    def test_modify_scope_satisfies_readonly_requests(self) -> None:
        token = GoogleTokenBundle(
            access_token="access",
            refresh_token="refresh",
            scopes=[GMAIL_MODIFY_SCOPE],
        )

        self.assertTrue(token.includes_scopes([GMAIL_READONLY_SCOPE]))

    def test_send_message_posts_raw_payload(self) -> None:
        requests: list[bytes] = []

        def fake_opener(request, timeout=30):  # noqa: ARG001
            requests.append(request.data or b"")
            return FakeResponse({"id": "msg-1"})

        client = GmailApiClient(access_token_supplier=lambda: "token", opener=fake_opener)
        client.send_message(b"Subject: Test\r\n\r\nHello")

        self.assertTrue(any(b'"raw"' in request for request in requests))


if __name__ == "__main__":
    unittest.main()
