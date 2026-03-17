from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from linkedin_alert_agent.config import Config
from linkedin_alert_agent.settings import UserSettings, apply_user_settings, load_user_settings, save_user_settings


class SettingsTests(unittest.TestCase):
    def test_save_and_load_user_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = Path(temp_dir) / "settings.json"
            original = UserSettings(
                source_mode="gmail",
                digest_to_email="user@example.com",
                daily_send_time="7:30 AM",
                timezone_name="America/New_York",
                gmail_label_names=["LinkedIn Alerts"],
                gmail_mark_read=True,
            )
            save_user_settings(settings_path, original)
            loaded = load_user_settings(settings_path)

            self.assertEqual(loaded.digest_to_email, "user@example.com")
            self.assertEqual(loaded.daily_send_time, "7:30 AM")
            self.assertEqual(loaded.source_mode, "gmail")
            self.assertTrue(loaded.gmail_mark_read)

    def test_apply_user_settings_populates_config_defaults(self) -> None:
        config = Config()
        applied = apply_user_settings(
            config,
            UserSettings(
                source_mode="gmail",
                digest_to_email="user@example.com",
                daily_send_time="8:00 AM",
                timezone_name="America/New_York",
                gmail_label_names=["LinkedIn Alerts"],
                gmail_mark_read=True,
            ),
        )

        self.assertEqual(applied.source_mode, "gmail")
        self.assertEqual(applied.digest_to_email, "user@example.com")
        self.assertEqual(applied.daily_send_time, "8:00 AM")
        self.assertEqual(applied.gmail_label_names, ["LinkedIn Alerts"])
        self.assertTrue(applied.gmail_mark_read)


if __name__ == "__main__":
    unittest.main()
