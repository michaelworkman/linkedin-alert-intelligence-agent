from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from linkedin_alert_agent.config import Config


TIME_RE = re.compile(r"^\d{1,2}:\d{2}(\s?[AaPp][Mm])?$")


@dataclass(slots=True)
class UserSettings:
    source_mode: str = "filesystem"
    digest_to_email: str = ""
    daily_send_time: str = "07:00"
    timezone_name: str = "America/New_York"
    gmail_label_names: list[str] = field(default_factory=lambda: ["LinkedIn Alerts"])
    gmail_mark_read: bool = False


def load_user_settings(path: Path) -> UserSettings:
    if not path.exists():
        return UserSettings()
    payload = json.loads(path.read_text(encoding="utf-8"))
    return UserSettings(
        source_mode=str(payload.get("source_mode", "filesystem")).strip() or "filesystem",
        digest_to_email=str(payload.get("digest_to_email", "")).strip(),
        daily_send_time=str(payload.get("daily_send_time", "07:00")).strip() or "07:00",
        timezone_name=str(payload.get("timezone_name", "America/New_York")).strip() or "America/New_York",
        gmail_label_names=[str(item).strip() for item in payload.get("gmail_label_names", ["LinkedIn Alerts"]) if str(item).strip()],
        gmail_mark_read=bool(payload.get("gmail_mark_read", False)),
    )


def save_user_settings(path: Path, settings: UserSettings) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")


def apply_user_settings(config: Config, settings: UserSettings) -> Config:
    if "SOURCE_MODE" not in os.environ and settings.source_mode:
        config.source_mode = settings.source_mode
    if "DIGEST_TO_EMAIL" not in os.environ and settings.digest_to_email:
        config.digest_to_email = settings.digest_to_email
    if "DAILY_SEND_TIME" not in os.environ and settings.daily_send_time:
        config.daily_send_time = settings.daily_send_time
    if "TIMEZONE_NAME" not in os.environ and settings.timezone_name:
        config.timezone_name = settings.timezone_name
    if "GMAIL_LABEL_NAMES" not in os.environ and settings.gmail_label_names:
        config.gmail_label_names = settings.gmail_label_names
    if "GMAIL_MARK_READ" not in os.environ:
        config.gmail_mark_read = settings.gmail_mark_read
    return config


def interactive_setup(config: Config) -> UserSettings:
    existing = load_user_settings(config.settings_path)

    digest_to_email = _prompt_text(
        "What email address should receive your daily digest?",
        existing.digest_to_email,
    )
    daily_send_time = _prompt_time(
        "What time should the digest arrive each morning?",
        existing.daily_send_time,
    )
    timezone_name = _prompt_text(
        "What time zone should I use?",
        existing.timezone_name,
    ) or existing.timezone_name
    label_name = _prompt_text(
        "What Gmail label should I watch for LinkedIn alerts? Type 'all' if you want every LinkedIn alert email.",
        existing.gmail_label_names[0] if existing.gmail_label_names else "all",
    )
    gmail_mark_read = _prompt_yes_no(
        "After processing, should I mark those LinkedIn alert emails as read?",
        existing.gmail_mark_read,
    )

    settings = UserSettings(
        source_mode="gmail",
        digest_to_email=digest_to_email,
        daily_send_time=daily_send_time,
        timezone_name=timezone_name,
        gmail_label_names=[] if label_name.strip().lower() in {"all", "none"} else [label_name],
        gmail_mark_read=gmail_mark_read,
    )
    save_user_settings(config.settings_path, settings)
    return settings


def render_status(config: Config) -> str:
    settings = load_user_settings(config.settings_path)
    gmail_ready = "yes" if config.gmail_token_path.exists() else "not yet"
    digest_recipient = settings.digest_to_email or "not set"
    label_name = settings.gmail_label_names[0] if settings.gmail_label_names else "All LinkedIn alert emails"
    return "\n".join(
        [
            "LinkedIn Alert Intelligence Agent status",
            f"- Settings file: {config.settings_path}",
            f"- Source mailbox: {settings.source_mode}",
            f"- Gmail authorization saved: {gmail_ready}",
            f"- Gmail label: {label_name}",
            f"- Processed checkpoint label: {config.gmail_processed_label_name or 'disabled'}",
            f"- Daily digest recipient: {digest_recipient}",
            f"- Daily send time: {settings.daily_send_time} {settings.timezone_name}",
            f"- Mark processed emails read: {'yes' if settings.gmail_mark_read else 'no'}",
            "- Digest delivery method: Gmail account",
        ]
    )


def _prompt_text(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    response = input(f"{prompt}{suffix}\n> ").strip()
    return response or default


def _prompt_yes_no(prompt: str, default: bool) -> bool:
    suffix = "Y/n" if default else "y/N"
    response = input(f"{prompt} [{suffix}]\n> ").strip().lower()
    if not response:
        return default
    return response in {"y", "yes"}


def _prompt_time(prompt: str, default: str) -> str:
    while True:
        response = _prompt_text(prompt, default)
        if TIME_RE.match(response):
            return response
        print("Please use a time like 7:00 AM or 07:00.")
