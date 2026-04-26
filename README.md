# Risk Guard ☀️

> 一句话提醒可能避免一场事故。不需要全面分析，只需要在对的时刻说对的话。

**Risk Guard** 是一个 AI 助手技能，在用户描述涉及安全、健康、财产或依赖人的计划时，主动提醒关键风险。

核心理念：**不是等用户问"安不安全"，而是在对的时刻主动说出关键提醒。**

## 三层渐进披露

信息分层使用，不一次全倒出来：

| 层级 | 何时触发 | 内容 |
|------|----------|------|
| **L0 快速提醒** | 默认 | 场景识别 + 复合风险 + 简洁输出（≤5句话） |
| **L1 场景清单** | 用户追问或风险较高 | 对应场景的逐项检查清单 |
| **L2 深度分析** | 用户明确要求全面分析 | 6阶段框架：检查清单→逆向→预验尸→压力测试→情景规划→韧性设计 |

## 它怎么工作

### 快速提醒（默认模式）

当你提到出差、见陌生人、大额交易、就医等计划时，Risk Guard 会：

1. **识别场景** — 匹配到 19 个风险场景之一（出行、诈骗、户外、面试……）
2. **评估复合风险** — 单一风险可控，组合才致命（如：术后+高海拔+无医疗支持）
3. **简洁提醒** — 1-3个关键风险 + 1条具体建议，不超过5句话

示例：

> 下周呼和浩特出差？最近那边降温到 -15°C，你膝盖恢复好了吗？出发前确认下酒店附近有没有医院。

### 深度分析（按需）

用户主动要求时，运行完整的 6 阶段分析：

| 阶段 | 方法 | 来源 |
|------|------|------|
| Phase 1 | 检查清单 | Atul Gawande, *The Checklist Manifesto* |
| Phase 2 | 逆向思维 + 预防原则 | Charlie Munger / Descartes / Wingspread Declaration |
| Phase 3 | 预验尸 + 红队 + 恐惧设定 | Gary Klein / 军事红队 / Tim Ferriss / 斯多葛学派 |
| Phase 4 | 复杂度/耦合 + 认知去偏 | Charles Perrow / Daniel Kahneman |
| Phase 5 | 情景规划 | Peter Schwartz / Shell |
| Phase 6 | 反脆弱 + 优雅降级 | Nassim Taleb / Erik Hollnagel |

## 19 个风险场景

| # | 场景 | # | 场景 |
|---|------|---|------|
| 1 | ✈️ 出行与交通 | 11 | 🧳 商务出差 |
| 2 | 🏢 工地/工厂/实验室 | 12 | 💻 诈骗与钓鱼 |
| 3 | 🏥 健康敏感活动 | 13 | 💼 面试与入职 |
| 4 | 👤 陌生人见面 | 14 | 🏥 就医与医疗决策 |
| 5 | 🏠 看房/租房 | 15 | 🌊 自然灾害应对 |
| 6 | 💰 交易与支付 | 16 | 🏠 家庭与居家安全 |
| 7 | 👶 看护与依赖 | 17 | 🤝 求职与兼职陷阱 |
| 8 | 🏕️ 户外与环境 | 18 | 🏋️ 运动与健身 |
| 9 | 🌙 夜间与独处 | 19 | 🔧 家政与装修 |
| 10 | 🌐 线上转线下 | | |

## Red Flags

用户说这些话时，Risk Guard 必须提醒：

| 用户说 | 实际可能是 |
|--------|-----------|
| "应该没事" | 没有验证的假设 |
| "就去一趟" | 低估了暴露时间 |
| "我身体还行" | 需要确认而不是自我评估 |
| "他们看起来靠谱" | 感觉不是验证 |
| "以前都没事" | 幸存者偏差 |
| "没时间考虑了" | 时间压力本身就是风险 |

## 安装

### Claude Code

```bash
claude plugin marketplace add Laplace-bit/risk-guard
claude plugin install risk-guard@risk-guard-dev
```

或本地开发：
```bash
claude --plugin-dir /path/to/risk-guard
```

### Gemini CLI

```bash
gemini extensions install https://github.com/Laplace-bit/risk-guard
```

### OpenAI Codex CLI

```bash
git clone https://github.com/Laplace-bit/risk-guard.git ~/.codex/risk-guard
mkdir -p ~/.agents/skills
ln -s ~/.codex/risk-guard ~/.agents/skills/risk-guard
```

### OpenCode

在 `opencode.json` 中添加：
```json
{
  "plugin": ["risk-guard@git+https://github.com/Laplace-bit/risk-guard.git"]
}
```

## 命令

| 命令 | 用途 |
|------|------|
| `/risk-guard check "计划描述"` | 快速安全提醒（默认模式） |
| `/risk-guard analyze "计划描述"` | 深度6阶段分析 |

大多数情况下不需要命令——Risk Guard 会在识别到风险场景时主动提醒。

## 项目结构

```
risk-guard/
├── SKILL.md                          # 核心技能：触发条件 + 执行流程 + 渐进披露
├── agents/
│   └── risk-reviewer.md              # 深度审查 agent persona
├── commands/
│   ├── check.md                      # 快速检查命令
│   └── analyze.md                    # 深度分析命令
├── hooks/
│   ├── hooks.json                    # Claude Code hooks
│   ├── hooks-cursor.json             # Cursor hooks
│   └── session-start                 # 会话启动提示
├── references/
│   ├── scenario-map.md               # 19个场景详细描述
│   ├── checklists.md                 # L1：各场景检查清单
│   ├── risk-taxonomy.md              # 风险分类、复合逻辑、等级定义
│   ├── question-bank.md              # 高价值追问
│   ├── output-examples.md            # 输出格式示例
│   ├── risk-engine-schema.md         # 结构化输入 schema
│   ├── inversion-and-precaution.md   # L2：逆向与预防
│   ├── premortem-redteam-fearsetting.md  # L2：预验尸、红队
│   ├── stress-test.md                # L2：压力测试
│   ├── scenario-planning.md          # L2：情景规划
│   └── resilience-building.md        # L2：韧性设计
├── scripts/
│   └── risk_engine.py                # 结构化评分引擎（可选）
├── tests/
│   └── test_risk_engine.py
├── package.json
└── README.md
```

## 设计原则

1. **提醒优先，不是分析优先** — 大多数时候5句话就够了
2. **渐进披露** — 信息分层，按需深入，不一次全倒出来
3. **复合风险优先** — 单一因素可控，组合才致命
4. **宁虚警勿漏报** — 当后果不可逆时，保守比乐观好
5. **具体可操作** — 不是"注意安全"，而是"确认最近医院在xx路上"
6. **主动触发** — 不等用户问"安不安全"，识别到风险场景就提醒
7. **科学依据** — 每个阶段都有同行评审的认知科学研究支撑

## License

MIT