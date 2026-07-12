const questionInput = document.querySelector("#question");
const runButton = document.querySelector("#runCheck");
const riskTitle = document.querySelector("#riskTitle");
const riskBadge = document.querySelector("#riskBadge");
const answerNode = document.querySelector("#answer");
const actionsNode = document.querySelector("#actions");
const citationsNode = document.querySelector("#citations");
const riskFilter = document.querySelector("#riskFilter");
let currentResult = null;

function retrieve(question, rules, topK = 3) {
  const normalizedQuestion = question.toLowerCase();
  return rules
    .map((rule) => {
      const keywordHits = rule.keywords.filter((keyword) => normalizedQuestion.includes(keyword.toLowerCase())).length;
      const topicHit = rule.topic && normalizedQuestion.includes(rule.topic.toLowerCase()) ? 1 : 0;
      const titleHit = normalizedQuestion.includes(rule.title.toLowerCase()) ? 1 : 0;
      return { score: keywordHits * 10 + topicHit * 5 + titleHit, rule };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, topK)
    .map((item) => item.rule);
}

function assess(question, matches) {
  if (matches.length === 0) {
    return {
      risk: "待人工核验",
      answer: "样例知识库未检索到足够依据，不能据此作出合规结论。",
      actions: ["补充适用的现行法规或标准", "由法规/质量人员复核产品类别与适用范围"],
      citations: []
    };
  }

  let risk = matches[0].risk_level || "提示";
  if (question.includes("年代号")) {
    risk = "需核验";
  } else if (/散装食品|现制现售|适用范围|格式|表格|专人负责|专人审核|责任人/.test(question)) {
    risk = "提示";
  } else if (/没有|没写|未标|漏标|缺少|无标签|预防|治疗|增强免疫力|特供|专供|内供|零添加|不添加|致敏|花生|脱氢乙酸|不一致|找不到|涂改|覆盖|含量只有|只有[0-9]/.test(question)) {
    risk = "高风险";
  } else if (risk === "高风险" && /是否|能否|怎么|多少|要求|需要|可以/.test(question)) {
    risk = "需核验";
  }

  return {
    risk,
    answer: matches[0].guidance,
    actions: matches[0].actions,
    citations: matches.map((rule) => ({
      standard: rule.title,
      clause: rule.clause,
      topic: rule.topic,
      riskLevel: rule.risk_level || "提示",
      riskType: rule.risk_type,
      sourceType: rule.source_type,
      effectiveDate: rule.effective_date,
      productScope: rule.product_scope,
      excerpt: rule.text,
      source: rule.source
    }))
  };
}

function setBadge(risk) {
  riskBadge.textContent = risk;
  riskBadge.className = "badge";
  if (risk === "高风险") riskBadge.classList.add("high");
  else if (risk === "需核验" || risk === "待人工核验") riskBadge.classList.add("check");
  else riskBadge.classList.add("info");
}

function render(result) {
  currentResult = result;
  riskTitle.textContent = result.risk;
  setBadge(result.risk);
  answerNode.textContent = result.answer;

  actionsNode.replaceChildren();
  result.actions.forEach((action) => {
    const item = document.createElement("li");
    item.textContent = action;
    actionsNode.appendChild(item);
  });

  renderCitations();
}

function renderCitations() {
  const selectedRisk = riskFilter.value;
  const citations = currentResult ? currentResult.citations : [];
  const visibleCitations = selectedRisk === "全部"
    ? citations
    : citations.filter((citation) => citation.riskLevel === selectedRisk);

  citationsNode.replaceChildren();
  if (citations.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "无；请补充知识库后人工核验。";
    citationsNode.appendChild(empty);
    return;
  }

  if (visibleCitations.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "当前筛选条件下没有引用条款。";
    citationsNode.appendChild(empty);
    return;
  }

  visibleCitations.forEach((citation) => {
    const card = document.createElement("details");
    card.className = "citation";
    card.open = visibleCitations.length === 1;

    const summary = document.createElement("summary");
    const title = document.createElement("strong");
    title.textContent = `${citation.standard} ${citation.clause}`;
    const badge = document.createElement("span");
    badge.className = "mini-badge";
    badge.textContent = citation.riskLevel;
    summary.append(title, badge);

    const meta = document.createElement("p");
    meta.className = "citation-meta";
    meta.textContent = `${citation.topic}｜${citation.sourceType}｜${citation.effectiveDate}`;

    const excerpt = document.createElement("p");
    excerpt.textContent = citation.excerpt;

    const source = document.createElement("a");
    source.href = citation.source;
    source.target = "_blank";
    source.rel = "noreferrer";
    source.textContent = citation.source;

    const scope = document.createElement("p");
    scope.className = "citation-meta";
    scope.textContent = `适用范围：${citation.productScope}`;

    card.append(summary, meta, excerpt, scope, source);
    citationsNode.appendChild(card);
  });
}

function runCheck() {
  const question = questionInput.value.trim();
  const result = assess(question, retrieve(question, window.FOODSAFE_RULES || []));
  render(result);
}

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => {
    questionInput.value = button.dataset.example;
    runCheck();
  });
});

runButton.addEventListener("click", runCheck);
riskFilter.addEventListener("change", renderCitations);
runCheck();
