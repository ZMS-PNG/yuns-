# MAPES 指挥开发文档

项目：多 Agent 个性化表现评分系统  
仓库：ZMS-PNG/yuns-  
版本：MVP 0.1  
目标周期：3 天  
核心目标：把当前仓库推进成一个可演示、可测试、可扩展的多 Agent 个性化表现评分系统。

---

## 1. 项目一句话定义

MAPES 是一个面向生活陪伴、娱乐角色扮演、智能玩具、App 截图助手、沉浸式展陈等场景的多 Agent 表现评分系统。系统输入场景、角色设定、Agent 输出和可选 OCR 文本，通过 ERNIE-as-a-Judge 或 Mock Judge 进行六维评分，并输出总分、等级、优点、短板和改进建议。

---

## 2. 当前开发原则

本项目必须按照 Harness Engineering 的方式推进。任何开发者、AI Agent 或后续接手者，都必须先读以下文件：

1. `AGENTS.md`
2. `prd/PRD.md`
3. `docs/ARCHITECTURE.md`
4. `feature_list.json`
5. `progress.md`
6. `session-handoff.md`

开发过程遵守以下原则：

- 一次只推进一个 active feature。
- 每次修改都必须能被测试或 demo 验证。
- 不把 API Key、Token、Cookie、私密配置写入仓库。
- OCR、Judge、评分、报告生成必须解耦。
- 文本输入闭环必须始终可运行。
- ERNIE 和 PaddleOCR 是增强能力，不应阻断 MVP 演示。

---

## 3. MVP 交付边界

### 3.1 必须交付

- 可安装 Python 包。
- 可运行 CLI。
- 可读取 demo case。
- 可使用 Mock Judge 跑完整评测。
- 可计算六维评分、总分和等级。
- 可输出 JSON 报告。
- 有 PRD、架构文档、Rubric、Dify 工作流说明。
- 有 GitHub Actions CI。
- 有 3 到 6 条 demo case。

### 3.2 暂不交付

- 完整前端页面。
- 大规模在线 Benchmark 平台。
- 多 Judge 投票系统。
- 复杂人工标注平台。
- 生产级权限系统。
- 生产级数据库。

---

## 4. 系统架构指挥图

```text
Case JSON
  ↓
Case Loader
  ↓
OCR Adapter optional
  ↓
Context Builder
  ↓
Judge Provider
  ├── MockJudge default
  └── ErnieJudge optional
  ↓
Scoring Engine
  ↓
Report Generator
  ↓
CLI / Dify / API Output
```

各模块职责：

| 模块 | 文件 | 职责 |
|---|---|---|
| Case Loader | `src/mapes/pipeline.py` | 读取并校验测试用例 |
| OCR Adapter | `src/mapes/ocr/paddle_ocr_client.py` | 从图片提取文本，失败不阻断主流程 |
| Judge Provider | `src/mapes/judges/ernie_judge.py` | Mock 或 ERNIE 评分 |
| Scoring Engine | `src/mapes/scoring.py` | 计算加权总分和等级 |
| Report Builder | `src/mapes/report.py` | 整合 case、judge 结果和 warnings |
| CLI | `src/mapes/cli.py` | 命令行运行入口 |
| Schema | `schemas/evaluation_result.schema.json` | 约束 Judge 输出结构 |

---

## 5. 六维评分标准

系统统一使用 0 到 5 分，最终转为百分制。

| 维度 | 权重 | 说明 |
|---|---:|---|
| persona_consistency | 20% | 是否稳定符合角色设定 |
| personality_expressiveness | 15% | 是否有鲜明、自然、可识别的个性 |
| context_awareness | 20% | 是否理解并利用场景、OCR 和上下文 |
| emotional_alignment | 15% | 是否能识别用户情绪并做出合适回应 |
| multi_agent_collaboration | 20% | 多 Agent 是否分工清楚、互相补充、共同推进 |
| hallucination_safety | 10% | 是否避免事实编造、危险建议和越界内容 |

等级规则：

| 分数 | 等级 |
|---:|---|
| 90-100 | S |
| 80-89 | A |
| 70-79 | B |
| 60-69 | C |
| 0-59 | D |

---

## 6. 仓库当前结构目标

```text
.
├── README.md
├── AGENTS.md
├── feature_list.json
├── progress.md
├── session-handoff.md
├── init.sh
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
├── prd/
│   └── PRD.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── RUBRIC.md
│   ├── COMPONENT_FUSION.md
│   ├── DEVELOPMENT_PLAN_3DAY.md
│   ├── DIFY_WORKFLOW.md
│   ├── GITHUB_STUDY_NOTES.md
│   └── COMMAND_DEVELOPMENT_GUIDE.md
├── prompts/
│   └── ernie_judge_prompt.txt
├── schemas/
│   └── evaluation_result.schema.json
├── src/
│   └── mapes/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── models.py
│       ├── pipeline.py
│       ├── report.py
│       ├── scoring.py
│       ├── judges/
│       │   ├── __init__.py
│       │   └── ernie_judge.py
│       └── ocr/
│           ├── __init__.py
│           └── paddle_ocr_client.py
├── data/
│   └── cases/
│       ├── demo_cases.json
│       └── demo_cases_extended.json
├── dify/
│   └── workflow_spec.json
├── examples/
│   └── demo_report.example.json
├── skills/
│   └── persona-eval/
│       └── SKILL.md
├── tests/
│   ├── test_scoring.py
│   └── test_pipeline_basic.py
└── .github/
    └── workflows/
        └── ci.yml
```

---

## 7. 本地开发启动指令

### 7.1 首次启动

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### 7.2 运行测试

```bash
python -m pytest
```

### 7.3 运行 demo

```bash
mkdir -p artifacts
python -m mapes --input data/cases/demo_cases.json --output artifacts/demo_report.json
```

扩展示例：

```bash
python -m mapes --input data/cases/demo_cases_extended.json --output artifacts/demo_report_extended.json
```

---

## 8. 开发任务拆分

## Phase 1：稳定 MVP 闭环

目标：确保不接外部 API 也能跑通。

任务：

1. 检查 `pyproject.toml` 是否能安装包。
2. 确认 `python -m mapes` 可执行。
3. 确认 `MockJudge` 默认启用。
4. 确认 `demo_cases.json` 生成报告。
5. 确认 `pytest` 全部通过。

验收命令：

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m mapes --input data/cases/demo_cases.json --output artifacts/demo_report.json
```

完成标准：

- `artifacts/demo_report.json` 存在。
- 每条 case 都有 `final_score`、`grade`、`scores`、`strengths`、`weaknesses`、`improvement_suggestions`。
- CI 通过。

---

## Phase 2：ERNIE Judge 真实接入

目标：把 Mock Judge 替换为真实 ERNIE-as-a-Judge，同时保留 Mock fallback。

需要配置环境变量：

```bash
ERNIE_API_URL=你的ERNIE接口地址
ERNIE_API_KEY=你的ERNIE密钥
MAPES_JUDGE_PROVIDER=ernie
```

开发要求：

1. `ErnieJudge` 只负责请求模型和解析结果。
2. Prompt 必须从 `prompts/ernie_judge_prompt.txt` 读取。
3. 如果 ERNIE 返回非 JSON，必须进行一次修复重试。
4. 如果仍失败，要给出明确错误，不要静默吞掉。
5. MockJudge 必须保持可用。

验收命令：

```bash
MAPES_JUDGE_PROVIDER=mock python -m mapes --input data/cases/demo_cases.json --output artifacts/mock_report.json
MAPES_JUDGE_PROVIDER=ernie python -m mapes --input data/cases/demo_cases.json --output artifacts/ernie_report.json
```

完成标准：

- Mock 模式稳定可运行。
- ERNIE 模式输出符合 `schemas/evaluation_result.schema.json`。
- 每个维度分数在 0 到 5 之间。

---

## Phase 3：JSON Schema 校验与错误恢复

目标：防止 Judge 输出格式漂移导致系统崩溃。

任务：

1. 在 pipeline 中加载 `schemas/evaluation_result.schema.json`。
2. 对 JudgeResult 原始 dict 做 schema validate。
3. 缺失字段时进入 repair 或 fallback。
4. 报告中保留 `warnings`。

推荐规则：

- 缺少 score：按 0 分处理，并加入 warning。
- score 超出 0-5：截断到范围内，并加入 warning。
- 缺少 reasons：允许为空，但加入 warning。
- Judge 完全不可解析：返回 error report 或抛出清晰异常。

完成标准：

- 新增 `tests/test_schema_validation.py`。
- 构造错误 JSON case，测试 warning 行为。

---

## Phase 4：OCR 接入

目标：让图片截图场景变成可评分上下文。

当前原则：

- OCR 只负责提取文字。
- OCR 失败不应影响纯文本评分。
- 如果 case 已经有 `ocr_context`，不要再次调用 OCR。

开发任务：

1. 保留 `PaddleOCRClient.extract_text(image_path)`。
2. 在 `EvaluationCase` 中允许 `image_path`。
3. 在 `pipeline.enrich_with_ocr` 中处理 OCR 失败。
4. 为 OCR 增加 mock test，不要求 CI 安装 PaddleOCR。

完成标准：

- 没有图片时正常跑。
- 有 `ocr_context` 时直接使用。
- 有 `image_path` 但 OCR 失败时报告 metadata 或 warnings。

---

## Phase 5：Dify 工作流落地

目标：把 Python MVP 映射成 Dify 可搭建流程。

Dify 节点：

1. Start：输入场景、角色设定、Agent 输出、可选图片。
2. IF：判断是否有图片。
3. OCR HTTP Node：调用 PaddleOCR 服务。
4. Code Node：清洗 OCR 文本。
5. Template Node：组装 Judge Prompt。
6. LLM Node：调用 ERNIE。
7. Code Node：解析 JSON 并计算总分。
8. Template Node：生成报告。
9. End：返回 report JSON。

Dify 输入字段建议：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| scenario_type | string | 是 | 场景类型 |
| scene_context | string | 是 | 场景描述 |
| agent_setting | json/string | 是 | Agent 角色设定 |
| agent_output | string | 是 | Agent 输出 |
| image_file | file | 否 | 截图 |

Dify 输出字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| report_json | object | 最终评测报告 |
| final_score | number | 总分 |
| grade | string | 等级 |
| warnings | array | 运行警告 |

---

## 9. GitHub Issues 指挥拆分

建议建立以下 Issues：

### Issue 1：稳定本地 MVP 运行

内容：

- 安装包。
- 跑测试。
- 跑 demo。
- 修复 import 和路径问题。

验收：

```bash
python -m pytest
python -m mapes --input data/cases/demo_cases.json --output artifacts/demo_report.json
```

### Issue 2：完善 ERNIE Judge

内容：

- 对接真实 ERNIE 返回结构。
- 增加 JSON repair retry。
- 增加异常提示。

### Issue 3：补充 Schema 校验

内容：

- 使用 jsonschema 校验 Judge 输出。
- 增加错误 case 测试。
- 报告 warnings。

### Issue 4：补充 OCR 测试

内容：

- mock PaddleOCRClient。
- 测试 `ocr_context` 优先级。
- 测试 OCR 失败 fallback。

### Issue 5：完善 Dify 迁移文档

内容：

- 输出节点字段表。
- 输出 Code Node 示例。
- 输出 Prompt 模板。

### Issue 6：最终演示材料

内容：

- 6 条 demo case。
- demo report 示例。
- README 截图或运行说明。
- 最终验收清单。

---

## 10. 分支和提交规范

推荐分支：

```text
main
feature/stable-mvp
feature/ernie-judge
feature/schema-validation
feature/ocr-adapter
feature/dify-workflow
feature/final-demo
```

提交信息格式：

```text
Add package configuration
Fix CLI entrypoint
Add ERNIE judge retry
Add schema validation tests
Add Dify workflow guide
Update final demo report
```

不要使用含糊提交信息，例如：

```text
update
fix
change files
some work
```

---

## 11. 验收清单

最终交付前必须检查：

- [ ] `README.md` 可指导新用户运行。
- [ ] `python -m pip install -e ".[dev]"` 成功。
- [ ] `python -m pytest` 成功。
- [ ] `python -m mapes --input data/cases/demo_cases.json --output artifacts/demo_report.json` 成功。
- [ ] `examples/demo_report.example.json` 存在。
- [ ] `docs/COMMAND_DEVELOPMENT_GUIDE.md` 存在。
- [ ] `docs/DIFY_WORKFLOW.md` 可指导 Dify 搭建。
- [ ] `.env.example` 不包含真实密钥。
- [ ] `MockJudge` 默认可运行。
- [ ] `ErnieJudge` 可通过环境变量启用。
- [ ] CI 配置存在。

---

## 12. 风险和应对

| 风险 | 影响 | 应对 |
|---|---|---|
| ERNIE API 返回格式变化 | Judge 解析失败 | 增加多路径 content 提取和 repair retry |
| OCR 环境安装困难 | 截图 case 无法跑 | OCR 设为 optional，允许直接传 ocr_context |
| LLM 评分不稳定 | 分数波动 | Prompt 固定、temperature 降低、Schema 校验 |
| 多 Agent 输出格式混乱 | 协作评分不准 | 要求 case 中保留 Agent 名称和发言顺序 |
| Demo 时间紧 | 无法完整产品化 | 先保证 CLI 和 Dify 文档可演示 |

---

## 13. 最终演示流程

演示时按以下顺序：

1. 展示问题：多 Agent 个性化表现难以量化。
2. 展示架构：Case → OCR → Judge → Scoring → Report。
3. 展示 Rubric：六维评分体系。
4. 运行命令：

```bash
python -m mapes --input data/cases/demo_cases.json --output artifacts/demo_report.json
```

5. 打开报告：展示总分、等级、优势、短板和建议。
6. 说明扩展：ERNIE、PaddleOCR、Dify、多 Judge Debate。

---

## 14. 下一步开发优先级

立即执行顺序：

1. 确认 CI 是否通过。
2. 修复 CI 中发现的问题。
3. 完善 ERNIE Judge 的真实返回解析。
4. 加入 JSON Schema 校验。
5. 增加 OCR mock tests。
6. 完成 Dify 可迁移版文档。
7. 生成最终 demo report。

---

## 15. 项目完成定义

当以下条件全部满足时，可以宣布 MVP 完成：

- 本地 CLI 可跑。
- CI 可跑。
- Mock Judge 可跑。
- ERNIE Judge 有明确接入路径。
- OCR 有 adapter 和 fallback。
- 至少 3 条 demo case 可输出评分报告。
- 文档足够让下一位开发者继续推进。
- 所有功能状态在 `feature_list.json` 和 `progress.md` 中同步更新。
