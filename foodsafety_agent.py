"""FoodSafe Agent: dependency-free retrieval and compliance rules MVP."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "regulations.json"


def load_rules(path: Path = DATA_FILE) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def retrieve(question: str, rules: list[dict], top_k: int = 3) -> list[dict]:
    ranked = []
    for rule in rules:
        keyword_hits = sum(1 for keyword in rule["keywords"] if keyword.lower() in question.lower())
        topic_hit = 1 if rule.get("topic", "").lower() in question.lower() else 0
        title_hit = 1 if rule["title"].lower() in question.lower() else 0
        if keyword_hits or topic_hit or title_hit:
            ranked.append((keyword_hits * 10 + topic_hit * 5 + title_hit, rule))
    return [rule for _, rule in sorted(ranked, key=lambda item: item[0], reverse=True)[:top_k]]


def assess(question: str, matches: list[dict]) -> dict:
    if not matches:
        return {
            "risk": "待人工核验",
            "answer": "样例知识库未检索到足够依据，不能据此作出合规结论。",
            "actions": ["补充适用的现行法规或标准", "由法规/质量人员复核产品类别与适用范围"],
            "citations": [],
        }

    primary = matches[0]
    risk = primary.get("risk_level", "提示")
    if "年代号" in question:
        risk = "需核验"
    elif re.search(r"散装食品|现制现售|适用范围|格式|表格|专人负责|专人审核|责任人", question):
        risk = "提示"
    elif re.search(r"没有|没写|未标|漏标|缺少|无标签|预防|治疗|增强免疫力|特供|专供|内供|零添加|不添加|致敏|花生|脱氢乙酸|不一致|找不到|涂改|覆盖|含量只有|只有[0-9]", question):
        risk = "高风险"
    elif risk == "高风险" and re.search(r"是否|能否|怎么|多少|要求|需要|可以", question):
        risk = "需核验"

    return {
        "risk": risk,
        "answer": primary["guidance"],
        "actions": primary["actions"],
        "citations": [
            {"standard": r["title"], "clause": r["clause"], "excerpt": r["text"], "source": r["source"]}
            for r in matches
        ],
    }


def ask(question: str, path: Path = DATA_FILE) -> dict:
    return assess(question, retrieve(question, load_rules(path)))


def render(result: dict) -> str:
    lines = [f"风险判断：{result['risk']}", f"结论：{result['answer']}", "整改建议："]
    lines.extend(f"- {item}" for item in result["actions"])
    lines.append("引用依据：")
    if not result["citations"]:
        lines.append("- 无；请补充知识库后人工核验。")
    for item in result["citations"]:
        lines.append(f"- {item['standard']} {item['clause']}：{item['excerpt']}\n  {item['source']}")
    lines.append("免责声明：本工具仅用于作品演示与初筛，不构成正式法律或合规意见。")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="食安智问：食品法规检索与合规初筛")
    parser.add_argument("question", nargs="*", help="食品法规、配料或标签问题")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    question = " ".join(args.question).strip() or input("请输入食品法规/标签问题：").strip()
    result = ask(question)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else render(result))


if __name__ == "__main__":
    main()
