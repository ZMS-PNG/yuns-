# 系统架构设计

## 1. 总体架构

```text
用户输入层
  ├── 文本场景 / 角色设定 / Agent输出
  └── 图片截图
        ↓
场景感知层
  └── PaddleOCR Adapter
        ↓
上下文组装层
  └── Context Builder
        ↓
评估执行层
  └── ERNIE Judge Adapter / Mock Judge
        ↓
评分聚合层
  └── Weighted Scoring Engine
        ↓
报告输出层
  └── JSON Report Generator
```

## 2. 分层职责

| 层 | 模块 | 职责 |
|---|---|---|
| 输入层 | Case Loader | 读取测试用例 |
| OCR层 | PaddleOCR Adapter | 把截图转为文本上下文 |
| 上下文层 | Context Builder | 合并场景、角色、OCR、Agent输出 |
| Judge层 | ERNIE Judge | 按 Rubric 输出结构化评分 |
| 评分层 | Scoring Engine | 计算加权总分和等级 |
| 报告层 | Report Generator | 输出JSON报告 |

## 3. Harness Engine 约束

本项目将 Harness Engineering 落成 5 个项目机制：

1. Instructions：`AGENTS.md` 定义启动路径、边界和完成标准。
2. State：`feature_list.json` 和 `progress.md` 保留任务状态。
3. Verification：`init.sh`、`pytest`、demo CLI 是验证闭环。
4. Scope：一次只推进一个 active feature。
5. Lifecycle：`session-handoff.md` 记录下次会话恢复信息。

## 4. 组件解耦原则

- OCR 不能耦合评分逻辑。
- Judge Provider 必须可替换。
- Rubric 和权重应配置化。
- Dify 工作流与 Python 原型共享相同数据结构。
