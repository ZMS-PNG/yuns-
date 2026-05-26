# Dify 工作流设计

## 节点清单

1. Start：接收 scene_context、agent_setting、agent_output、image_file。
2. IF image exists：判断是否需要 OCR。
3. HTTP OCR Node：调用 PaddleOCR 服务。
4. Code Node：清洗 OCR 文本。
5. Template Node：组装 Judge Prompt。
6. LLM Node：调用 ERNIE。
7. Code Node：解析 JSON，计算总分和等级。
8. Template Node：生成最终报告。
9. End：输出 report_json。

## 节点契约

### OCR 输入

```json
{"image_url": "..."}
```

### OCR 输出

```json
{"ocr_context": "识别出的文字"}
```

### Judge 输出

必须符合 `schemas/evaluation_result.schema.json`。

## 错误处理

- OCR 失败：使用空字符串并标记 `ocr_status=failed`。
- Judge 非 JSON：重试一次，仍失败则返回 error report。
- 缺失 score：按 0 分处理并在 warnings 中记录。
