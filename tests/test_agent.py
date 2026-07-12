import unittest

from foodsafety_agent import ask


class FoodSafeAgentTest(unittest.TestCase):
    def test_missing_label_item_is_high_risk_and_cited(self):
        result = ask("预包装饼干没有标生产日期，可以销售吗？")
        self.assertEqual(result["risk"], "高风险")
        self.assertTrue(result["citations"])
        cited = " ".join(item["clause"] for item in result["citations"])
        self.assertIn("第67条", cited)

    def test_standard_code_question(self):
        result = ask("执行标准的年代号能否不写？")
        self.assertEqual(result["risk"], "需核验")
        self.assertIn("年代号", result["answer"])
        self.assertIn("不标示", result["answer"])

    def test_unknown_question_abstains(self):
        result = ask("冷链车应该使用哪种压缩机？")
        self.assertEqual(result["risk"], "待人工核验")
        self.assertFalse(result["citations"])


if __name__ == "__main__":
    unittest.main()
