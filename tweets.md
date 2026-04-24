# risk-guard 发推特文草稿

## 版本 A：blunt / 吐槽型（单推）

现在的 AI Agent 工具都在教人怎么更快写代码，但几乎没人教 Agent 怎么在动刀前停下来想想。

risk-guard v2.0 就是干这个的。不是另一个代码助手，是 Agent 的刹车片 + 显微镜。

两层速度：Quick Review 秒级安全扫描，Full Review 6 个 phase 把计划从 checklists 撕到 pre-mortem 再撕到 resilience。底层全是 Gawande / Munger / Klein / Kahneman / Taleb 那帮人研究了一辈子的事。

开源，Apache 2.0。Claude Code / Gemini / Codex / Cursor / Hermes 通用。

github.com/Laplace-bit/risk-guard

---

## 版本 B：叙事型（Thread x3）

**Tweet 1**
最近半年写 risk-guard 的动机很单纯：看了太多 Agent 因为没做基础安全检查就把自己炸了的案例。

不是模型不够聪明，是没人给它装刹车。

**Tweet 2**
所以塞了两套制动系统进去：

Quick Review：几秒钟跑完 12 个场景分类 + 7 维风险建模，日常够用了。

Full Review：Checklists → Inversion → Pre-mortem → Stress Test → Scenario Planning → Resilience。

把 blind spot 全翻出来。

**Tweet 3**
Phase 1 借 Gawande 的手术清单，Phase 3 借 Klein 的 pre-mortem（能多找出 30% 失败原因），Phase 6 借 Taleb 的 antifragility。

不想写说明书了，自己看吧：

github.com/Laplace-bit/risk-guard

Apache 2.0，全平台 Agent 通用。

---

## 版本 C：极简技术型（单推）

Agent 决策的三层防御：
- Checklists 防遗忘
- 认知框架切换防盲区  
- Resilience 防不可预测

risk-guard v2.0 把这三层塞进了各家 Agent 的 skill / plugin 接口里。一个 repo，Claude / Gemini / Codex / Cursor / Hermes 通用。附带 Python risk engine。

开源，Apache 2.0。

github.com/Laplace-bit/risk-guard

---

## 版本 D：自嘲 / 创造者视角（单推）

作为一个自己炸过无数次、事后才想起来 "早检查一步就好了" 的人，写了 risk-guard。

本质上就是让 Agent 在 action 之前先跑一轮 "如果我现在就动手，最蠢的失败方式是什么"。

从 checklists 到 pre-mortem 到 scenario planning，底层全是正经认知科学，不是玄学。v2.0 加了完整的 Full Review 6-phase 和 Python risk engine。

Claude Code、Gemini、Codex、Cursor、Hermes 都能装。免费，开源。

github.com/Laplace-bit/risk-guard
