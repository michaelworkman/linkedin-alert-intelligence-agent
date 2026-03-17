from __future__ import annotations

import argparse
from pathlib import Path

from linkedin_alert_agent.config import Config
from linkedin_alert_agent.gmail import (
    GMAIL_MODIFY_SCOPE,
    GmailApiClient,
    GoogleOAuthManager,
    load_google_client_config,
)
from linkedin_alert_agent.pipeline import rebuild_latest_digest, run_pipeline
from linkedin_alert_agent.settings import apply_user_settings, interactive_setup, load_user_settings, render_status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Rank LinkedIn alert emails into a daily digest.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Process alerts and generate a digest.")
    run_parser.add_argument("--dry-run", action="store_true", help="Skip marking Gmail messages read and skip email delivery.")
    run_parser.add_argument("--source", choices=["filesystem", "gmail"], help="Override SOURCE_MODE.")
    run_parser.add_argument("--input-dir", type=Path, help="Directory of .eml files when using filesystem mode.")
    run_parser.add_argument("--db", type=Path, help="SQLite database path.")
    run_parser.add_argument("--output-dir", type=Path, help="Directory where digests are written.")
    run_parser.add_argument("--profile", type=Path, help="Profile JSON path.")

    auth_parser = subparsers.add_parser("gmail-auth", help="Authorize local Gmail API access and save a refreshable token.")
    auth_parser.add_argument("--allow-modify", action="store_true", help="Request gmail.modify so the agent can mark processed messages read.")
    auth_parser.add_argument("--no-open-browser", action="store_true", help="Print the auth URL without attempting to open a browser.")

    labels_parser = subparsers.add_parser("gmail-labels", help="List available Gmail labels using the saved OAuth token.")
    labels_parser.add_argument("--json", action="store_true", help="Print labels as JSON.")

    subparsers.add_parser("setup", help="Walk through the app setup in plain language.")
    subparsers.add_parser("status", help="Show what is configured and what is still missing.")

    refresh_parser = subparsers.add_parser("refresh-digest", help="Re-score saved jobs and rebuild the latest digest.")
    refresh_parser.add_argument("--send", action="store_true", help="Send the rebuilt digest after re-scoring it.")
    return parser


def _apply_overrides(config: Config, args: argparse.Namespace) -> Config:
    if getattr(args, "source", None):
        config.source_mode = args.source
    if getattr(args, "input_dir", None):
        config.filesystem_input_dir = args.input_dir
    if getattr(args, "db", None):
        config.database_path = args.db
    if getattr(args, "output_dir", None):
        config.output_dir = args.output_dir
        config.failed_dir = args.output_dir / "failed"
    if getattr(args, "profile", None):
        config.profile_path = args.profile
    return config


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = Config.from_env()
    config = apply_user_settings(config, load_user_settings(config.settings_path))
    config = _apply_overrides(config, args)

    if args.command == "run":
        summary = run_pipeline(config, dry_run=args.dry_run)
        print(f"Run date: {summary.run_date}")
        print(f"Processed messages: {summary.processed_messages}")
        print(f"Parsed jobs: {summary.parsed_jobs}")
        print(f"New jobs: {summary.new_jobs}")
        print(f"Duplicates removed: {summary.duplicates_removed}")
        print(f"Digest path: {summary.digest_path}")
        print(f"Subject: {summary.subject}")
        if summary.email_sent_at:
            print(f"Email sent at: {summary.email_sent_at}")
        return 0
    if args.command == "gmail-auth":
        scopes = list(config.gmail_delivery_scopes)
        if args.allow_modify:
            scopes = ["https://www.googleapis.com/auth/gmail.modify"] + [
                scope for scope in scopes if scope != "https://www.googleapis.com/auth/gmail.readonly"
            ]
            scopes = list(dict.fromkeys(scopes))
        oauth_manager = GoogleOAuthManager(
            client_config=load_google_client_config(
                client_id=config.gmail_client_id,
                client_secret=config.gmail_client_secret,
                redirect_uri=config.gmail_redirect_uri,
                client_secrets_path=config.gmail_client_secrets_path,
            ),
            token_path=config.gmail_token_path,
        )
        token = oauth_manager.authorize(
            scopes=scopes,
            open_browser=not args.no_open_browser,
            timeout_seconds=config.gmail_auth_timeout_seconds,
        )
        print(f"Saved Gmail token: {config.gmail_token_path}")
        print(f"Granted scopes: {' '.join(token.scopes)}")
        return 0
    if args.command == "gmail-labels":
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
            access_token_supplier=lambda: oauth_manager.get_token(config.gmail_scopes).access_token
        )
        labels = client.list_labels()
        if args.json:
            import json

            print(json.dumps(labels, indent=2))
        else:
            for label in labels:
                name = str(label.get("name", "")).strip()
                label_id = str(label.get("id", "")).strip()
                label_type = str(label.get("type", "")).strip()
                print(f"{name}\t{label_id}\t{label_type}")
        return 0
    if args.command == "setup":
        settings = interactive_setup(config)
        print("Saved your setup.")
        print(f"Source mailbox: {settings.source_mode}")
        print(f"Daily digest recipient: {settings.digest_to_email or 'not set'}")
        print(f"Daily send time: {settings.daily_send_time} {settings.timezone_name}")
        print(f"Gmail label: {settings.gmail_label_names[0] if settings.gmail_label_names else 'All LinkedIn alert emails'}")
        print(f"Mark processed emails read: {'yes' if settings.gmail_mark_read else 'no'}")
        return 0
    if args.command == "status":
        print(render_status(config))
        return 0
    if args.command == "refresh-digest":
        summary = rebuild_latest_digest(config, send_email=args.send)
        print(f"Run date: {summary.run_date}")
        print(f"Jobs rescored: {summary.new_jobs}")
        print(f"Digest path: {summary.digest_path}")
        print(f"Subject: {summary.subject}")
        if summary.email_sent_at:
            print(f"Email sent at: {summary.email_sent_at}")
        return 0
    parser.print_help()
    return 1
