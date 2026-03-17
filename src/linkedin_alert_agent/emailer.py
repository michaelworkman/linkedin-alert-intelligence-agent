from __future__ import annotations

import re
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage

from linkedin_alert_agent.config import Config
from linkedin_alert_agent.gmail import GmailApiClient, GoogleOAuthManager, load_google_client_config


def _plain_text_from_html(html: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", without_tags).strip()


def _build_message(config: Config, subject: str, html_body: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = config.digest_from_email or config.digest_to_email
    message["To"] = config.digest_to_email
    message.set_content(_plain_text_from_html(html_body))
    message.add_alternative(html_body, subtype="html")
    return message


def _send_via_gmail_api(config: Config, message: EmailMessage) -> str | None:
    if config.source_mode != "gmail" or not config.digest_to_email:
        return None
    if config.gmail_access_token:
        client = GmailApiClient(access_token_supplier=lambda: config.gmail_access_token)
    else:
        oauth_manager = GoogleOAuthManager(
            client_config=load_google_client_config(
                client_id=config.gmail_client_id,
                client_secret=config.gmail_client_secret,
                redirect_uri=config.gmail_redirect_uri,
                client_secrets_path=config.gmail_client_secrets_path,
            ),
            token_path=config.gmail_token_path,
        )
        client = GmailApiClient(
            access_token_supplier=lambda: oauth_manager.get_token(config.gmail_delivery_scopes).access_token
        )
    client.send_message(message.as_bytes())
    return datetime.now(timezone.utc).isoformat()


def send_html_email(config: Config, subject: str, html_body: str) -> str | None:
    message = _build_message(config, subject, html_body)

    if config.smtp_ready:
        with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=30) as server:
            if config.smtp_use_tls:
                server.starttls()
            if config.smtp_username:
                server.login(config.smtp_username, config.smtp_password)
            server.send_message(message)
        return datetime.now(timezone.utc).isoformat()
    return _send_via_gmail_api(config, message)
