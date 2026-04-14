from __future__ import annotations

import json
import tempfile
import unittest
from email.message import EmailMessage
from pathlib import Path
from unittest.mock import patch

from linkedin_alert_agent.config import Config
from linkedin_alert_agent.models import SourceMessage
from linkedin_alert_agent.pipeline import rebuild_latest_digest, run_pipeline
from linkedin_alert_agent.storage import Storage


def build_email(message_id: str, subject: str, html: str) -> bytes:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = "jobs-noreply@linkedin.com"
    message["To"] = "michael@example.com"
    message["Date"] = "Tue, 17 Mar 2026 07:00:00 -0400"
    message["Message-ID"] = f"<{message_id}>"
    message.set_content("LinkedIn jobs")
    message.add_alternative(html, subtype="html")
    return message.as_bytes()


EMAIL_ONE = """
<html><body>
  <div>
    <a href="https://www.linkedin.com/jobs/view/12345/?trk=email">Creative Director</a>
    <div>Acme Studio</div>
    <div>Boston, Massachusetts, United States</div>
    <div>Hybrid</div>
    <div>Lead brand storytelling and AI-forward digital experiences.</div>
    <div>2 days ago</div>
    <div>$180,000 - $210,000</div>
  </div>
</body></html>
"""

EMAIL_TWO = """
<html><body>
  <div>
    <a href="https://www.linkedin.com/jobs/view/12345/?trk=another-email">Creative Director</a>
    <div>Acme Studio</div>
    <div>Boston, Massachusetts, United States</div>
    <div>Hybrid</div>
    <div>Lead brand storytelling and AI-forward digital experiences.</div>
  </div>
  <div>
    <a href="https://www.linkedin.com/jobs/view/67890/?trk=email">Brand Experience Lead</a>
    <div>Civic Media Lab</div>
    <div>New York, New York, United States</div>
    <div>Hybrid</div>
    <div>Actively recruiting Own experiential design strategy and editorial storytelling.</div>
    <div>1 day ago</div>
  </div>
</body></html>
"""


class PipelineTests(unittest.TestCase):
    def test_pipeline_dedupes_and_ranks_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_dir = root / "input"
            output_dir = root / "output"
            input_dir.mkdir()
            output_dir.mkdir()

            (input_dir / "alert-1.eml").write_bytes(build_email("message-1", "Jobs alert for Design Leadership", EMAIL_ONE))
            (input_dir / "alert-2.eml").write_bytes(build_email("message-2", "Jobs alert for Design Leadership", EMAIL_TWO))

            profile_path = root / "profile.json"
            profile_path.write_text(
                json.dumps(
                    {
                        "target_titles": ["Creative Director", "Brand Experience Lead"],
                        "target_locations": ["Boston, MA", "New York, NY", "Remote"],
                        "remote_ok": True,
                        "must_have_keywords": ["leadership", "storytelling", "brand"],
                        "positive_keywords": ["AI", "editorial", "creative", "brand", "experience"],
                        "avoid_keywords": ["junior", "contract"],
                        "company_quality_signals": ["civic", "media"],
                        "classification_thresholds": {
                            "top_match": 70,
                            "worth_a_look": 50,
                            "low_priority": 30,
                        },
                    }
                ),
                encoding="utf-8",
            )

            config = Config(
                source_mode="filesystem",
                filesystem_input_dir=input_dir,
                database_path=root / "alerts.sqlite3",
                output_dir=output_dir,
                failed_dir=output_dir / "failed",
                profile_path=profile_path,
                gmail_token_path=root / "secrets" / "google-token.json",
            )
            summary = run_pipeline(config, dry_run=True)

            self.assertEqual(summary.processed_messages, 2)
            self.assertEqual(summary.parsed_jobs, 3)
            self.assertEqual(summary.new_jobs, 2)
            self.assertEqual(summary.duplicates_removed, 1)
            self.assertTrue(summary.digest_path.exists())
            digest_html = summary.digest_path.read_text(encoding="utf-8")
            self.assertIn("Creative Director", digest_html)
            self.assertIn("Brand Experience Lead", digest_html)
            self.assertIn("<div class='job-meta'><strong>Acme Studio</strong></div>", digest_html)
            self.assertIn("<div class='job-location'>Boston, MA (Hybrid)</div>", digest_html)
            self.assertIn("<div class='job-facts'><span class='job-fact'>Salary: $180,000 - $210,000</span><span class='job-fact'>Posted: 2 days ago</span></div>", digest_html)
            self.assertIn("<ul class='job-why'><li>Strong title fit: Creative Director</li><li>Target location: Boston, MA</li><li>Alignment keywords: AI, creative, brand</li></ul>", digest_html)
            self.assertNotIn("Open posting", digest_html)
            self.assertNotIn("job #", digest_html)
            self.assertNotIn("Actively recruiting", digest_html)
            self.assertNotIn("Duplicates removed", digest_html)
            self.assertNotIn("score ", digest_html)
            self.assertNotIn("<h2>Trends</h2>", digest_html)

    def test_rebuild_latest_digest_rescores_existing_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_dir = root / "input"
            output_dir = root / "output"
            input_dir.mkdir()
            output_dir.mkdir()

            (input_dir / "alert-1.eml").write_bytes(build_email("message-1", "Jobs alert for Design Leadership", EMAIL_ONE))

            profile_path = root / "profile.json"
            profile_path.write_text(
                json.dumps(
                    {
                        "target_titles": ["Creative Director"],
                        "target_locations": ["Boston, MA"],
                        "classification_thresholds": {
                            "top_match": 90,
                            "worth_a_look": 50,
                            "low_priority": 30,
                        },
                    }
                ),
                encoding="utf-8",
            )

            config = Config(
                source_mode="filesystem",
                filesystem_input_dir=input_dir,
                database_path=root / "alerts.sqlite3",
                output_dir=output_dir,
                failed_dir=output_dir / "failed",
                profile_path=profile_path,
                gmail_token_path=root / "secrets" / "google-token.json",
                digest_to_email="user@example.com",
            )
            with patch("linkedin_alert_agent.pipeline.send_html_email", return_value="2026-03-17T12:00:00+00:00"):
                run_pipeline(config, dry_run=False)

            profile_path.write_text(
                json.dumps(
                    {
                        "target_titles": ["Creative Director"],
                        "target_locations": ["Boston, MA"],
                        "classification_thresholds": {
                            "top_match": 60,
                            "worth_a_look": 45,
                            "low_priority": 30,
                        },
                    }
                ),
                encoding="utf-8",
            )

            summary = rebuild_latest_digest(config, send_email=False)
            digest_html = summary.digest_path.read_text(encoding="utf-8")
            self.assertIn("Top matches", digest_html)

    def test_pipeline_rolls_back_state_when_delivery_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = root / "output"
            output_dir.mkdir()

            profile_path = root / "profile.json"
            profile_path.write_text(
                json.dumps(
                    {
                        "target_titles": ["Creative Director"],
                        "target_locations": ["Boston, MA"],
                    }
                ),
                encoding="utf-8",
            )

            message = SourceMessage(
                message_id="message-1",
                raw_bytes=build_email("message-1", "Jobs alert for Design Leadership", EMAIL_ONE),
            )

            class RecordingSource:
                def __init__(self, source_message: SourceMessage) -> None:
                    self.source_message = source_message
                    self.marked: list[str] = []

                def iter_messages(self) -> list[SourceMessage]:
                    return [self.source_message]

                def mark_processed(self, message_id: str) -> None:
                    self.marked.append(message_id)

            source = RecordingSource(message)
            config = Config(
                source_mode="gmail",
                database_path=root / "alerts.sqlite3",
                output_dir=output_dir,
                failed_dir=output_dir / "failed",
                profile_path=profile_path,
                gmail_token_path=root / "secrets" / "google-token.json",
                digest_to_email="michael@example.com",
            )

            with patch("linkedin_alert_agent.pipeline._build_source", return_value=source):
                with patch("linkedin_alert_agent.pipeline.send_html_email", side_effect=RuntimeError("send failed")):
                    with self.assertRaises(RuntimeError):
                        run_pipeline(config, dry_run=False)

            storage = Storage(config.database_path)
            try:
                self.assertFalse(storage.has_processed_alert("message-1"))
                self.assertIsNone(storage.latest_digest())
            finally:
                storage.close()
            self.assertEqual(source.marked, [])

    def test_dry_run_does_not_persist_alert_state(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            input_dir = root / "input"
            output_dir = root / "output"
            input_dir.mkdir()
            output_dir.mkdir()

            (input_dir / "alert-1.eml").write_bytes(build_email("message-1", "Jobs alert for Design Leadership", EMAIL_ONE))

            profile_path = root / "profile.json"
            profile_path.write_text(
                json.dumps(
                    {
                        "target_titles": ["Creative Director"],
                        "target_locations": ["Boston, MA"],
                    }
                ),
                encoding="utf-8",
            )

            config = Config(
                source_mode="filesystem",
                filesystem_input_dir=input_dir,
                database_path=root / "alerts.sqlite3",
                output_dir=output_dir,
                failed_dir=output_dir / "failed",
                profile_path=profile_path,
                gmail_token_path=root / "secrets" / "google-token.json",
            )

            summary = run_pipeline(config, dry_run=True)
            self.assertEqual(summary.processed_messages, 1)
            self.assertTrue(summary.digest_path.exists())

            storage = Storage(config.database_path)
            try:
                self.assertFalse(storage.has_processed_alert("message-1"))
                self.assertIsNone(storage.latest_digest())
            finally:
                storage.close()


if __name__ == "__main__":
    unittest.main()
