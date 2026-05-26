# 类似项目学习与组件融合方案

## 1. 参考项目/方法

| 方向 | 可借鉴点 | 融合方式 |
|---|---|---|
| Harness Engineering | 指令、状态、验证、范围、生命周期 | 落地为 AGENTS.md、feature_list、progress、init.sh、handoff |
| OpenAI Evals 类框架 | 数据集 + evaluator + report | 用 case JSON + judge prompt + report JSON 替代复杂平台 |
| DeepEval/Ragas 类框架 | 指标化评分、结构化结果 | 使用六维指标和 JSON Schema |
| G-Eval/LLM-as-Judge | Rubric + form filling | ERNIE 输出固定 JSON，不输出自由文本 |
| ChatEval | 多评委/多 Agent 讨论 | MVP 先做单 Judge，后续扩展成多 Judge debate |
| PaddleOCR | 截图文本提取 | 作为场景上下文提取器，不参与打分 |
| Dify | 工作流编排 | 串联 OCR、上下文、Judge、报告节点 |

## 2. 融合后的最小组件组合

```text
Case JSON
  → OCR Adapter(optional)
  → Context Builder
  → ERNIE Judge
  → Scoring Engine
  → Report Generator
  → Dify/API/CLI Output
```

## 3. 为什么这样组合

- 用 Harness 保证 3 天开发不失控。
- 用 JSON Case 降低前端依赖。
- 用 ERNIE-as-a-Judge 快速实现主观维度自动评估。
- 用 PaddleOCR 覆盖截图类真实生活场景。
- 用 Dify 做产品化编排，Python 原型负责验证核心逻辑。
