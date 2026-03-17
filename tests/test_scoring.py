from __future__ import annotations

import unittest

from linkedin_alert_agent.models import JobRecord
from linkedin_alert_agent.normalize import normalize_job_record
from linkedin_alert_agent.scoring import JobScorer


class ScoringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = {
            "target_titles": ["Creative Director", "Design Director", "Brand Director"],
            "target_locations": ["Boston, MA", "New York, NY", "Remote"],
            "remote_ok": True,
            "preferred_seniority_keywords": [
                "director",
                "head",
                "lead",
                "manager",
                "principal",
            ],
            "emphasis_keywords": ["marketing", "product"],
            "positive_keywords": ["AI", "editorial", "brand"],
            "must_have_keywords": ["storytelling", "strategy"],
            "avoid_keywords": ["contract", "temporary"],
            "hard_exclude_keywords": [
                "architect",
                "architecture",
                "engineering",
                "facilities",
                "environmental",
                "ops",
                "operations",
                "devops",
                "security",
            ],
            "company_quality_signals": ["agency", "media"],
            "core_function_keywords": [
                "design",
                "brand",
                "ux",
                "ui",
                "experience",
                "editorial",
                "storytelling",
                "visual",
                "content strategy",
                "art direction",
                "digital",
            ],
            "classification_thresholds": {
                "top_match": 65,
                "worth_a_look": 50,
                "low_priority": 30,
            },
        }
        self.scorer = JobScorer(self.profile)

    def test_target_design_leadership_role_becomes_top_match(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Design Director",
                company_raw="Elmwood Brand & Design Consultancy",
                location_raw="New York, New York, United States",
                snippet="Lead brand storytelling and design strategy across major accounts.",
                posted_text="2 days ago",
                work_mode="Hybrid",
            )
        )
        score = self.scorer.score(job)
        self.assertEqual(score.classification, "Top matches")
        self.assertGreaterEqual(score.total, 65)

    def test_irrelevant_senior_role_gets_penalized(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Director, EHS Informatics & Communication",
                company_raw="Inside Higher Ed",
                location_raw="Boston, Massachusetts, United States",
                snippet="Lead the research informatics and environmental communications team.",
                posted_text="2 days ago",
                work_mode="On-site",
            )
        )
        score = self.scorer.score(job)
        self.assertNotEqual(score.classification, "Top matches")
        self.assertLess(score.total, 50)

    def test_manager_role_in_target_function_can_be_top_match(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Manager, Interactive Design",
                company_raw="Mission Media Studio",
                location_raw="Boston, Massachusetts, United States",
                snippet="Lead brand storytelling, digital design strategy, and cross-functional creative delivery.",
                posted_text="1 day ago",
                work_mode="Hybrid",
            )
        )
        score = self.scorer.score(job)
        self.assertEqual(score.classification, "Top matches")
        self.assertGreaterEqual(score.total, 65)

    def test_architecture_roles_are_hard_filtered(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Manager, Design and Architecture",
                company_raw="Vantage Group",
                location_raw="Boston, Massachusetts, United States",
                snippet="Lead design and architecture planning across facilities.",
                posted_text="1 day ago",
                work_mode="On-site",
            )
        )
        score = self.scorer.score(job)
        self.assertEqual(score.classification, "Filtered out")
        self.assertEqual(score.total, 0)

    def test_engineering_facilities_and_environmental_roles_are_hard_filtered(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Director, Facilities Engineering",
                company_raw="Civic Campus",
                location_raw="Boston, Massachusetts, United States",
                snippet="Lead environmental planning and engineering operations across facilities.",
                posted_text="1 day ago",
                work_mode="On-site",
            )
        )
        score = self.scorer.score(job)
        self.assertEqual(score.classification, "Filtered out")
        self.assertEqual(score.total, 0)

    def test_ops_and_devops_roles_are_hard_filtered(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Director, Studio Operations",
                company_raw="Mission Studio",
                location_raw="Boston, Massachusetts, United States",
                snippet="Lead creative ops and devops workflow planning across teams.",
                posted_text="1 day ago",
                work_mode="Hybrid",
            )
        )
        score = self.scorer.score(job)
        self.assertEqual(score.classification, "Filtered out")
        self.assertEqual(score.total, 0)

    def test_ops_exclusion_uses_word_boundaries(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Visual Design Director",
                company_raw="BrightShops",
                location_raw="Boston, Massachusetts, United States",
                snippet="Lead brand storytelling and digital design direction.",
                posted_text="1 day ago",
                work_mode="Hybrid",
            )
        )
        score = self.scorer.score(job)
        self.assertNotEqual(score.classification, "Filtered out")

    def test_security_roles_are_hard_filtered(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Senior Vice President, Global Security",
                company_raw="Lensa",
                location_raw="New York, New York, United States",
                snippet="Lead enterprise security strategy and global operations.",
                posted_text="1 day ago",
                work_mode="On-site",
            )
        )
        score = self.scorer.score(job)
        self.assertEqual(score.classification, "Filtered out")
        self.assertEqual(score.total, 0)

    def test_product_and_marketing_roles_get_extra_weight(self) -> None:
        job = normalize_job_record(
            JobRecord(
                title_raw="Director, Product Design",
                company_raw="Mission Product Studio",
                location_raw="Boston, Massachusetts, United States",
                snippet="Lead product design strategy and marketing collaboration for digital launches.",
                posted_text="1 day ago",
                work_mode="Hybrid",
            )
        )
        score = self.scorer.score(job)
        self.assertGreaterEqual(score.total, 65)
        self.assertEqual(score.classification, "Top matches")
        self.assertIn("product", score.rationale.lower())


if __name__ == "__main__":
    unittest.main()
