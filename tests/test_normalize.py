from __future__ import annotations

import unittest

from linkedin_alert_agent.normalize import canonicalize_job_url, normalize_company, normalize_location, normalize_title


class NormalizeTests(unittest.TestCase):
    def test_normalize_title_expands_common_abbreviations(self) -> None:
        self.assertEqual(normalize_title("Sr. Design Director"), "Senior Design Director")

    def test_normalize_location_shortens_us_state_names(self) -> None:
        self.assertEqual(
            normalize_location("Boston, Massachusetts, United States"),
            "Boston, MA",
        )

    def test_canonicalize_job_url_drops_tracking_parameters(self) -> None:
        self.assertEqual(
            canonicalize_job_url("https://www.linkedin.com/jobs/view/12345/?trk=public_jobs&refId=abc#fragment"),
            "https://www.linkedin.com/jobs/view/12345",
        )

    def test_normalize_decodes_double_escaped_html_entities(self) -> None:
        self.assertEqual(
            normalize_title("Manager, Media &amp;Amp; Interactive Design"),
            "Manager, Media & Interactive Design",
        )
        self.assertEqual(
            normalize_company("AT&amp;Amp;T Inc."),
            "AT&T",
        )


if __name__ == "__main__":
    unittest.main()
