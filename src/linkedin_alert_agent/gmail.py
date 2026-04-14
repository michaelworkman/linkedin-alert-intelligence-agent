from __future__ import annotations

import base64
import json
import secrets
import threading
import webbrowser
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen


GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
GMAIL_MODIFY_SCOPE = "https://www.googleapis.com/auth/gmail.modify"
GMAIL_SEND_SCOPE = "https://www.googleapis.com/auth/gmail.send"
DEFAULT_AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"
DEFAULT_GMAIL_API_BASE_URL = "https://gmail.googleapis.com/gmail/v1/users/me"
SCOPE_IMPLICATIONS = {
    GMAIL_MODIFY_SCOPE: {GMAIL_READONLY_SCOPE},
}


class GmailAuthError(RuntimeError):
    """Raised when Gmail authentication configuration or tokens are invalid."""


@dataclass(slots=True)
class GoogleOAuthClientConfig:
    client_id: str
    client_secret: str
    redirect_uri: str
    auth_uri: str = DEFAULT_AUTH_URI
    token_uri: str = DEFAULT_TOKEN_URI


@dataclass(slots=True)
class GoogleTokenBundle:
    access_token: str
    refresh_token: str
    scopes: list[str]
    token_type: str = "Bearer"
    expiry_utc: str | None = None

    @classmethod
    def from_payload(cls, payload: dict) -> "GoogleTokenBundle":
        raw_scope = str(payload.get("scope", "")).strip()
        scopes = [scope for scope in raw_scope.split() if scope]
        return cls(
            access_token=str(payload.get("access_token", "")).strip(),
            refresh_token=str(payload.get("refresh_token", "")).strip(),
            scopes=scopes,
            token_type=str(payload.get("token_type", "Bearer")).strip() or "Bearer",
            expiry_utc=str(payload.get("expiry_utc", "")).strip() or None,
        )

    def to_payload(self) -> dict[str, object]:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "scope": " ".join(self.scopes),
            "token_type": self.token_type,
            "expiry_utc": self.expiry_utc,
        }

    def is_expired(self, skew_seconds: int = 120) -> bool:
        if not self.expiry_utc:
            return False
        try:
            expires_at = datetime.fromisoformat(self.expiry_utc)
        except ValueError:
            return True
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        return datetime.now(timezone.utc) >= (expires_at - timedelta(seconds=skew_seconds))

    def includes_scopes(self, required_scopes: list[str]) -> bool:
        granted = set(self.scopes)
        expanded = set(granted)
        for scope in granted:
            expanded.update(SCOPE_IMPLICATIONS.get(scope, set()))
        return all(scope in expanded for scope in required_scopes)


def load_google_client_config(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    client_secrets_path: Path,
) -> GoogleOAuthClientConfig:
    resolved_client_id = client_id
    resolved_client_secret = client_secret
    resolved_redirect_uri = redirect_uri
    auth_uri = DEFAULT_AUTH_URI
    token_uri = DEFAULT_TOKEN_URI

    if client_secrets_path.exists():
        payload = json.loads(client_secrets_path.read_text(encoding="utf-8"))
        container = payload.get("installed") or payload.get("web") or payload
        resolved_client_id = resolved_client_id or str(container.get("client_id", "")).strip()
        resolved_client_secret = resolved_client_secret or str(container.get("client_secret", "")).strip()
        auth_uri = str(container.get("auth_uri", DEFAULT_AUTH_URI)).strip() or DEFAULT_AUTH_URI
        token_uri = str(container.get("token_uri", DEFAULT_TOKEN_URI)).strip() or DEFAULT_TOKEN_URI
        if not redirect_uri.strip():
            redirect_uris = [str(uri).strip() for uri in container.get("redirect_uris", []) if str(uri).strip()]
            resolved_redirect_uri = next(
                (
                    uri
                    for uri in redirect_uris
                    if urlparse(uri).hostname in {"127.0.0.1", "localhost"}
                ),
                resolved_redirect_uri,
            )

    if not resolved_client_id:
        raise GmailAuthError(
            f"Missing Gmail OAuth client ID. Set GMAIL_CLIENT_ID or add a desktop OAuth client JSON at {client_secrets_path}."
        )
    if not resolved_redirect_uri:
        raise GmailAuthError("Missing Gmail redirect URI. Set GMAIL_REDIRECT_URI or include one in the OAuth client JSON.")
    return GoogleOAuthClientConfig(
        client_id=resolved_client_id,
        client_secret=resolved_client_secret,
        redirect_uri=resolved_redirect_uri,
        auth_uri=auth_uri,
        token_uri=token_uri,
    )


class GoogleOAuthManager:
    def __init__(
        self,
        client_config: GoogleOAuthClientConfig,
        token_path: Path,
        opener: Callable[..., object] = urlopen,
    ) -> None:
        self.client_config = client_config
        self.token_path = token_path
        self.opener = opener

    def load_token(self) -> GoogleTokenBundle | None:
        if not self.token_path.exists():
            return None
        payload = json.loads(self.token_path.read_text(encoding="utf-8"))
        return GoogleTokenBundle.from_payload(payload)

    def save_token(self, token: GoogleTokenBundle) -> None:
        self.token_path.parent.mkdir(parents=True, exist_ok=True)
        self.token_path.write_text(json.dumps(token.to_payload(), indent=2), encoding="utf-8")

    def get_token(self, required_scopes: list[str]) -> GoogleTokenBundle:
        token = self.load_token()
        if token is None:
            raise GmailAuthError(
                f"No Gmail token found at {self.token_path}. Run `PYTHONPATH=src python3 -m linkedin_alert_agent gmail-auth` first."
            )
        if not token.includes_scopes(required_scopes):
            raise GmailAuthError(
                "The saved Gmail token does not include the scopes required for this run. Re-run `gmail-auth` with the needed permissions."
            )
        if token.is_expired():
            if not token.refresh_token:
                raise GmailAuthError("The saved Gmail token has expired and does not include a refresh token. Re-run `gmail-auth`.")
            token = self.refresh_token(token)
            self.save_token(token)
        return token

    def refresh_token(self, token: GoogleTokenBundle) -> GoogleTokenBundle:
        payload = {
            "client_id": self.client_config.client_id,
            "refresh_token": token.refresh_token,
            "grant_type": "refresh_token",
        }
        if self.client_config.client_secret:
            payload["client_secret"] = self.client_config.client_secret
        response = self._post_token_request(payload)
        access_token = str(response.get("access_token", "")).strip()
        if not access_token:
            raise GmailAuthError("Google token refresh did not return an access token.")
        refreshed = GoogleTokenBundle(
            access_token=access_token,
            refresh_token=token.refresh_token,
            scopes=token.scopes,
            token_type=str(response.get("token_type", token.token_type)).strip() or token.token_type,
            expiry_utc=_expiry_from_response(response),
        )
        scope_text = str(response.get("scope", "")).strip()
        if scope_text:
            refreshed.scopes = [scope for scope in scope_text.split() if scope]
        return refreshed

    def authorize(
        self,
        scopes: list[str],
        open_browser: bool = True,
        timeout_seconds: int = 180,
    ) -> GoogleTokenBundle:
        redirect = urlparse(self.client_config.redirect_uri)
        if redirect.hostname not in {"127.0.0.1", "localhost"}:
            raise GmailAuthError(
                f"Unsupported redirect URI {self.client_config.redirect_uri}. Use a loopback redirect such as http://127.0.0.1:8765/callback."
            )
        if not redirect.port:
            raise GmailAuthError(
                f"Redirect URI {self.client_config.redirect_uri} must include an explicit port for the local callback server."
            )

        state = secrets.token_urlsafe(24)
        params_holder: dict[str, str] = {}
        event = threading.Event()

        class OAuthCallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # type: ignore[override]
                parsed = urlparse(self.path)
                query = parse_qs(parsed.query)
                params_holder["state"] = query.get("state", [""])[0]
                params_holder["code"] = query.get("code", [""])[0]
                params_holder["error"] = query.get("error", [""])[0]
                body = (
                    "Authorization received. You can close this tab and return to the terminal."
                    if not params_holder["error"]
                    else f"Authorization failed: {params_holder['error']}"
                )
                body_bytes = body.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.send_header("Content-Length", str(len(body_bytes)))
                self.end_headers()
                self.wfile.write(body_bytes)
                event.set()

            def log_message(self, format: str, *args) -> None:  # noqa: A003
                _ = format, args

        server = HTTPServer((redirect.hostname, redirect.port), OAuthCallbackHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            auth_url = self._build_auth_url(scopes, state)
            if open_browser:
                webbrowser.open(auth_url)
            print("Open this URL to authorize Gmail access:")
            print(auth_url)
            if not event.wait(timeout=timeout_seconds):
                raise GmailAuthError("Timed out waiting for the Gmail OAuth callback. Re-run `gmail-auth` and try again.")
            if params_holder.get("error"):
                raise GmailAuthError(f"Gmail authorization failed: {params_holder['error']}")
            if params_holder.get("state") != state:
                raise GmailAuthError("OAuth state mismatch during Gmail authorization.")
            code = params_holder.get("code", "")
            if not code:
                raise GmailAuthError("Google did not return an authorization code.")
            token = self.exchange_code(code)
            if not token.refresh_token:
                existing = self.load_token()
                if existing and existing.refresh_token:
                    token.refresh_token = existing.refresh_token
            self.save_token(token)
            return token
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=1)

    def exchange_code(self, code: str) -> GoogleTokenBundle:
        payload = {
            "code": code,
            "client_id": self.client_config.client_id,
            "redirect_uri": self.client_config.redirect_uri,
            "grant_type": "authorization_code",
        }
        if self.client_config.client_secret:
            payload["client_secret"] = self.client_config.client_secret
        response = self._post_token_request(payload)
        access_token = str(response.get("access_token", "")).strip()
        if not access_token:
            raise GmailAuthError("Google token exchange did not return an access token.")
        scopes = [scope for scope in str(response.get("scope", "")).split() if scope]
        return GoogleTokenBundle(
            access_token=access_token,
            refresh_token=str(response.get("refresh_token", "")).strip(),
            scopes=scopes,
            token_type=str(response.get("token_type", "Bearer")).strip() or "Bearer",
            expiry_utc=_expiry_from_response(response),
        )

    def _build_auth_url(self, scopes: list[str], state: str) -> str:
        return (
            f"{self.client_config.auth_uri}?"
            + urlencode(
                {
                    "client_id": self.client_config.client_id,
                    "redirect_uri": self.client_config.redirect_uri,
                    "response_type": "code",
                    "scope": " ".join(scopes),
                    "access_type": "offline",
                    "include_granted_scopes": "true",
                    "prompt": "consent",
                    "state": state,
                }
            )
        )

    def _post_token_request(self, payload: dict[str, str]) -> dict:
        request = Request(
            self.client_config.token_uri,
            data=urlencode(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with self.opener(request, timeout=30) as response:
                raw = response.read()
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise GmailAuthError(f"Google OAuth request failed with HTTP {exc.code}: {error_body}") from exc
        return json.loads(raw.decode("utf-8"))


class GmailApiClient:
    def __init__(
        self,
        access_token_supplier: Callable[[], str],
        base_url: str = DEFAULT_GMAIL_API_BASE_URL,
        opener: Callable[..., object] = urlopen,
    ) -> None:
        self.access_token_supplier = access_token_supplier
        self.base_url = base_url
        self.opener = opener

    def request_json(
        self,
        method: str,
        path: str,
        params: dict[str, object] | None = None,
        payload: dict | None = None,
    ) -> dict:
        url = f"{self.base_url}{path}"
        if params:
            query = urlencode(
                [
                    (key, value)
                    for key, raw_value in params.items()
                    for value in (raw_value if isinstance(raw_value, list) else [raw_value])
                    if value not in (None, "")
                ],
                doseq=True,
            )
            if query:
                url = f"{url}?{query}"
        body = None
        headers = {
            "Authorization": f"Bearer {self.access_token_supplier()}",
            "Accept": "application/json",
        }
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = Request(url, data=body, headers=headers, method=method)
        try:
            with self.opener(request, timeout=30) as response:
                raw = response.read()
        except HTTPError as exc:
            error_body = exc.read().decode("utf-8", errors="replace")
            raise GmailAuthError(f"Gmail API request failed with HTTP {exc.code}: {error_body}") from exc
        return json.loads(raw.decode("utf-8"))

    def list_labels(self) -> list[dict]:
        payload = self.request_json("GET", "/labels")
        return payload.get("labels", [])

    def create_label(
        self,
        name: str,
        label_list_visibility: str = "labelShow",
        message_list_visibility: str = "show",
    ) -> dict:
        return self.request_json(
            "POST",
            "/labels",
            payload={
                "name": name,
                "labelListVisibility": label_list_visibility,
                "messageListVisibility": message_list_visibility,
            },
        )

    def send_message(self, raw_message: bytes) -> dict:
        encoded = base64.urlsafe_b64encode(raw_message).decode("utf-8")
        return self.request_json("POST", "/messages/send", payload={"raw": encoded})

    def resolve_label_ids(self, label_names: list[str], fallback_label_ids: list[str]) -> list[str]:
        if not label_names:
            return fallback_label_ids
        labels = self.list_labels()
        name_to_id = {str(label.get("name", "")).strip().lower(): str(label.get("id", "")).strip() for label in labels}
        resolved: list[str] = []
        missing: list[str] = []
        for name in label_names:
            label_id = name_to_id.get(name.strip().lower())
            if not label_id:
                missing.append(name)
                continue
            resolved.append(label_id)
        if missing:
            raise GmailAuthError(
                f"Could not find Gmail label(s): {', '.join(missing)}. Use `gmail-labels` to inspect available labels."
            )
        return list(dict.fromkeys(resolved + fallback_label_ids))

    def ensure_label_id(self, label_name: str) -> str:
        label_name = label_name.strip()
        if not label_name:
            raise GmailAuthError("Processed Gmail label name cannot be empty.")
        labels = self.list_labels()
        name_to_id = {str(label.get("name", "")).strip().lower(): str(label.get("id", "")).strip() for label in labels}
        existing = name_to_id.get(label_name.lower())
        if existing:
            return existing
        created = self.create_label(label_name)
        created_id = str(created.get("id", "")).strip()
        if not created_id:
            raise GmailAuthError(f"Gmail did not return an ID after creating label {label_name!r}.")
        return created_id

    def modify_message_labels(
        self,
        message_id: str,
        add_label_ids: list[str] | None = None,
        remove_label_ids: list[str] | None = None,
    ) -> dict:
        return self.request_json(
            "POST",
            f"/messages/{message_id}/modify",
            payload={
                "addLabelIds": add_label_ids or [],
                "removeLabelIds": remove_label_ids or [],
            },
        )


def _expiry_from_response(payload: dict) -> str | None:
    expires_in = payload.get("expires_in")
    if expires_in in (None, ""):
        return None
    try:
        seconds = int(expires_in)
    except (TypeError, ValueError):
        return None
    return (datetime.now(timezone.utc) + timedelta(seconds=seconds)).isoformat()
