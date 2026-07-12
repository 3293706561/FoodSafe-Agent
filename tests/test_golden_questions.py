import json
import unittest
from pathlib import Path

from foodsafety_agent import ask


ROOT = Path(__file__).resolve().parents[1]
GOLDEN_FILE = ROOT / "data" / "golden_questions.json"


class GoldenQuestionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.questions = json.loads(GOLDEN_FILE.read_text(encoding="utf-8"))

    def test_golden_question_schema(self):
        required = {
            "id",
            "question",
            "expected_topic",
            "expected_risk",
            "expected_citation",
            "expected_action",
        }
        self.assertEqual(len(self.questions), 30)
        for item in self.questions:
            with self.subTest(item=item.get("id")):
                self.assertTrue(required.issubset(item))
                for field in required:
                    self.assertTrue(item[field])

    def test_golden_questions_are_answered_with_expected_risk(self):
        failures = []
        for item in self.questions:
            result = ask(item["question"])
            if result["risk"] != item["expected_risk"] or not result["citations"]:
                failures.append(
                    {
                        "id": item["id"],
                        "expected_risk": item["expected_risk"],
                        "actual_risk": result["risk"],
                        "has_citation": bool(result["citations"]),
                    }
                )
        self.assertFalse(failures, failures)


if __name__ == "__main__":
    unittest.main()
