from __future__ import annotations

import unittest
from email.message import EmailMessage

from linkedin_alert_agent.parsers import parse_alert_email


def build_email(subject: str, html: str) -> bytes:
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = "jobs-noreply@linkedin.com"
    message["To"] = "michael@example.com"
    message["Date"] = "Tue, 17 Mar 2026 07:00:00 -0400"
    message["Message-ID"] = "<sample-message-1>"
    message.set_content("LinkedIn jobs")
    message.add_alternative(html, subtype="html")
    return message.as_bytes()


SAMPLE_HTML = """
<html>
  <body>
    <div>
      <a href="https://www.linkedin.com/jobs/view/12345/?trk=email">Creative Director</a>
      <div>Acme Studio</div>
      <div>Boston, Massachusetts, United States</div>
      <div>Hybrid</div>
      <div>Lead brand storytelling and AI-forward digital experiences.</div>
      <div>2 days ago</div>
      <div>$180,000 - $210,000</div>
    </div>
    <div>
      <a href="https://www.linkedin.com/jobs/view/67890/?trk=email">Director of UX, AI Products</a>
      <div>Future Labs</div>
      <div>Remote, United States</div>
      <div>Remote</div>
      <div>Lead a product design team shaping AI workflows.</div>
      <div>1 day ago</div>
    </div>
  </body>
</html>
"""


class ParserTests(unittest.TestCase):
    def test_parse_alert_email_extracts_normalized_jobs(self) -> None:
        parsed = parse_alert_email(
            build_email("Jobs alert for Design Leadership", SAMPLE_HTML),
            source_message_id="gmail-1",
        )

        self.assertEqual(parsed.alert_name, "Design Leadership")
        self.assertEqual(len(parsed.jobs), 2)

        first = parsed.jobs[0]
        self.assertEqual(first.title_normalized, "Creative Director")
        self.assertEqual(first.company_normalized, "Acme Studio")
        self.assertEqual(first.location_normalized, "Boston, MA")
        self.assertEqual(first.work_mode, "Hybrid")

        second = parsed.jobs[1]
        self.assertEqual(second.location_normalized, "Remote")
        self.assertEqual(second.work_mode, "Remote")
        self.assertIn("AI", second.title_normalized)

    def test_parse_alert_email_decodes_double_escaped_entities(self) -> None:
        html = """
        <html>
          <body>
            <div>
              <a href="https://www.linkedin.com/jobs/view/24680/?trk=email">Manager, Media &amp;amp; Interactive Design</a>
              <div>AT&amp;amp;T Inc.</div>
              <div>Boston, Massachusetts, United States</div>
              <div>Hybrid</div>
              <div>Lead brand storytelling &amp;amp; editorial direction.</div>
            </div>
          </body>
        </html>
        """
        parsed = parse_alert_email(
            build_email("Jobs alert for Design Leadership", html),
            source_message_id="gmail-entities",
        )

        self.assertEqual(len(parsed.jobs), 1)
        job = parsed.jobs[0]
        self.assertEqual(job.title_normalized, "Manager, Media & Interactive Design")
        self.assertEqual(job.company_normalized, "AT&T")
        self.assertIn("&", job.snippet)


if __name__ == "__main__":
    unittest.main()
