# GitHub 学习笔记与项目编程约束

## 1. 学习结论

Harness Engineering 的核心不是更复杂的 Prompt，而是给 Agent 建一个可恢复、可验证、边界清晰的工作环境。本项目采用五件套：

- `AGENTS.md`：开发规则和启动路径。
- `feature_list.json`：功能状态和完成标准。
- `progress.md`：执行证据。
- `init.sh`：初始化和验证入口。
- `session-handoff.md`：跨会话交接。

## 2. 编程约束

- 一个会话只推进一个 active feature。
- 所有外部服务都通过 adapter 封装。
- MVP 默认 mock judge 可运行。
- OCR 只做上下文提取，不直接参与评分。
- 评分结果必须可 JSON Schema 校验。
- 任何“完成”都必须有测试或 demo 输出证据。

## 3. 参考组件融合

- Harness Creator：项目级开发约束。
- LLM-as-a-Judge：自动评分。
- PaddleOCR：截图上下文提取。
- Dify：评测流程编排。
- Python CLI：本地可验证原型。
