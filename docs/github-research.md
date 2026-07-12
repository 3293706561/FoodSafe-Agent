# GitHub 同类项目调研（2026-07-12）

结论：没有发现足够匹配、可直接二开的中国食品合规项目，自建领域 MVP 更能体现“食品专业 + AI 应用 + 企业合规”。搜索覆盖 food safety RAG、food compliance agent、regulation QA、食品安全法规 RAG、食品合规智能体等中英文关键词。

| 候选 | 技术栈 / 可运行性 | 匹配度 | 可借鉴点 | 风险 |
|---|---|---:|---|---|
| [Raven](https://github.com/kyouens/raven_public) | 法规 RAG、实验型 Web 问答；论文给出源码，运行需模型/检索依赖 | 3/5 | 权威语料限定、引用、法规问答评测 | 美国临床实验室法规，非食品/中国法规；模型配置变化会影响结果 |
| [Controllable-RAG-Agent](https://github.com/NirDiamant/Controllable-RAG-Agent) | Python、LangGraph/图式 RAG；可按 README 配置 | 2/5 | 查询路由、检索流程控制 | 架构偏重，缺领域规则与食品语料，依赖外部模型 |
| [rag-web-ui](https://github.com/rag-web-ui/rag-web-ui) | 通用 RAG Web UI；文档完整，可本地部署 | 2/5 | 上传、切分、引用展示与 UI | 通用知识库产品，二开成本高，不能直接做合规判断 |
| [ragcompliance](https://github.com/dakshtrehan/ragcompliance) | Python/FastAPI，可选 Supabase/仪表盘 | 2/5 | 审计、脱敏、企业接入思路 | 重点是 RAG 系统自身合规，不是食品法规咨询；基础设施过重 |
| [FoodSafetyMangemntSystem gist](https://gist.github.com/opexxx/114a3ca805c9c1752b49c0dc42822709) | ISO 22000 审核问题清单；非完整应用 | 1/5 | 可转为审核检查表/规则库 | 不是 RAG 或 Agent，缺代码、数据治理和许可证说明 |

## 决策

不复制候选代码，自建无依赖内核。复用的是设计原则：法规条款版本化、答案逐条引用、未命中拒答、规则与生成分离、建立小型评测集。作品集展示优先采用静态 Web Demo；未来如需要企业内网部署，再将当前 `ask()` 封装成 FastAPI 服务，而不先引入完整通用平台。

## 权威语料入口

- [国家卫健委：GB 7718-2025 官方问答](https://www.nhc.gov.cn/sps/c100087/202509/bc824a504ec34c27883da73f14c20d44.shtml)
- [国家卫健委：2025 年第 2 号标准发布公告](https://www.nhc.gov.cn/wjw/zcwjgg/202503/97802a2683b840dd8be0e1449982c6a5.shtml)
- [国家卫健委：食品安全法](https://www.nhc.gov.cn/fzs/c100048/201808/31b2202291464a5fb9e1f64bebc4d877.shtml)
- [市场监管总局：食品标识监督管理办法](https://www.samr.gov.cn/cms_files/filemanager/1647978232/attach/20253/ed58300458664454a1609c74355cb725.pdf)
