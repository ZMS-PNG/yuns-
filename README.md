# MAPES: 多 Agent 个性化表现评分系统 MVP

MAPES（Multi-Agent Persona Evaluation System）是一个面向生活化、娱乐化、沉浸式互动场景的多 Agent 个性化表现评测原型。

3 天 MVP 目标：

- 支持文本场景、角色设定、Agent 输出输入；
- 可选接入 PaddleOCR，把截图文字转成场景上下文；
- 使用 ERNIE-as-a-Judge 依据 Rubric 输出六维评分；
- 自动计算总分、等级、优势、短板和优化建议；
- 使用 Harness Engineering 约束项目开发流程，保证可恢复、可验证、可扩展。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m mapes.cli --input data/cases/demo_cases.json --output artifacts/demo_report.json
```

如果没有配置 ERNIE API，系统会使用 `mock` judge 跑通闭环。

## 目录结构

```text
.
├── AGENTS.md
├── feature_list.json
├── progress.md
├── session-handoff.md
├── init.sh
├── prd/PRD.md
├── docs/
├── prompts/ernie_judge_prompt.txt
├── schemas/evaluation_result.schema.json
├── src/mapes/
├── data/cases/demo_cases.json
├── tests/
└── skills/persona-eval/SKILL.md
```

## 核心评测维度

1. 角色一致性 Persona Consistency
2. 个性表达力 Personality Expressiveness
3. 场景感知度 Context Awareness
4. 情感共鸣力 Emotional Alignment
5. 多 Agent 协作演绎 Multi-Agent Collaboration
6. 幻觉与安全控制 Hallucination & Safety
