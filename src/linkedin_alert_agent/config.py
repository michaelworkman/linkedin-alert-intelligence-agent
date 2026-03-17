from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name: str) -> list[str]:
    value = os.getenv(name, "")
    if not value.strip():
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(slots=True)
class Config:
    source_mode: str = "filesystem"
    settings_path: Path = Path("settings.json")
    filesystem_input_dir: Path = Path("examples/data")
    database_path: Path = Path("data/linkedin_alerts.sqlite3")
    output_dir: Path = Path("output")
    failed_dir: Path = Path("output/failed")
    profile_path: Path = Path("profile.json")
    gmail_access_token: str = ""
    gmail_query: str = "from:(jobalerts-noreply@linkedin.com OR jobs-noreply@linkedin.com) newer_than:2d"
    gmail_label_names: list[str] = field(default_factory=list)
    gmail_label_ids: list[str] = field(default_factory=list)
    gmail_max_results: int = 25
    gmail_mark_read: bool = False
    gmail_client_id: str = ""
    gmail_client_secret: str = ""
    gmail_client_secrets_path: Path = Path("secrets/google-oauth-client.json")
    gmail_token_path: Path = Path("secrets/google-token.json")
    gmail_redirect_uri: str = "http://127.0.0.1:8765/callback"
    gmail_auth_timeout_seconds: int = 180
    daily_send_time: str = "07:00"
    timezone_name: str = "America/New_York"
    digest_from_email: str = ""
    digest_to_email: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_use_tls: bool = True
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-mini"
    openai_base_url: str = "https://api.openai.com/v1/responses"
    openai_reasoner_enabled: bool = False

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            source_mode=os.getenv("SOURCE_MODE", "filesystem").strip().lower(),
            settings_path=Path(os.getenv("SETTINGS_PATH", "settings.json")),
            filesystem_input_dir=Path(os.getenv("FILESYSTEM_INPUT_DIR", "examples/data")),
            database_path=Path(os.getenv("DATABASE_PATH", "data/linkedin_alerts.sqlite3")),
            output_dir=Path(os.getenv("OUTPUT_DIR", "output")),
            failed_dir=Path(os.getenv("FAILED_DIR", "output/failed")),
            profile_path=Path(os.getenv("PROFILE_PATH", "profile.json")),
            gmail_access_token=os.getenv("GMAIL_ACCESS_TOKEN", "").strip(),
            gmail_query=os.getenv(
                "GMAIL_QUERY",
                "from:(jobalerts-noreply@linkedin.com OR jobs-noreply@linkedin.com) newer_than:2d",
            ).strip(),
            gmail_label_names=_env_list("GMAIL_LABEL_NAMES"),
            gmail_label_ids=_env_list("GMAIL_LABEL_IDS"),
            gmail_max_results=int(os.getenv("GMAIL_MAX_RESULTS", "25")),
            gmail_mark_read=_env_bool("GMAIL_MARK_READ", False),
            gmail_client_id=os.getenv("GMAIL_CLIENT_ID", "").strip(),
            gmail_client_secret=os.getenv("GMAIL_CLIENT_SECRET", "").strip(),
            gmail_client_secrets_path=Path(
                os.getenv("GMAIL_CLIENT_SECRETS_PATH", "secrets/google-oauth-client.json")
            ),
            gmail_token_path=Path(os.getenv("GMAIL_TOKEN_PATH", "secrets/google-token.json")),
            gmail_redirect_uri=os.getenv(
                "GMAIL_REDIRECT_URI",
                "http://127.0.0.1:8765/callback",
            ).strip(),
            gmail_auth_timeout_seconds=int(os.getenv("GMAIL_AUTH_TIMEOUT_SECONDS", "180")),
            daily_send_time=os.getenv("DAILY_SEND_TIME", "07:00").strip(),
            timezone_name=os.getenv("TIMEZONE_NAME", "America/New_York").strip(),
            digest_from_email=os.getenv("DIGEST_FROM_EMAIL", "").strip(),
            digest_to_email=os.getenv("DIGEST_TO_EMAIL", "").strip(),
            smtp_host=os.getenv("SMTP_HOST", "").strip(),
            smtp_port=int(os.getenv("SMTP_PORT", "587")),
            smtp_username=os.getenv("SMTP_USERNAME", "").strip(),
            smtp_password=os.getenv("SMTP_PASSWORD", "").strip(),
            smtp_use_tls=_env_bool("SMTP_USE_TLS", True),
            openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip(),
            openai_base_url=os.getenv(
                "OPENAI_BASE_URL",
                "https://api.openai.com/v1/responses",
            ).strip(),
            openai_reasoner_enabled=_env_bool("OPENAI_REASONER_ENABLED", False),
        )

    def ensure_directories(self) -> None:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.failed_dir.mkdir(parents=True, exist_ok=True)
        self.gmail_token_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def smtp_ready(self) -> bool:
        return bool(self.smtp_host and self.digest_from_email and self.digest_to_email)

    @property
    def openai_ready(self) -> bool:
        return bool(self.openai_reasoner_enabled and self.openai_api_key and self.openai_model)

    @property
    def gmail_scopes(self) -> list[str]:
        if self.gmail_mark_read:
            return ["https://www.googleapis.com/auth/gmail.modify"]
        return ["https://www.googleapis.com/auth/gmail.readonly"]

    @property
    def gmail_delivery_scopes(self) -> list[str]:
        scopes = list(self.gmail_scopes)
        if self.digest_to_email:
            scopes.append("https://www.googleapis.com/auth/gmail.send")
        return list(dict.fromkeys(scopes))
