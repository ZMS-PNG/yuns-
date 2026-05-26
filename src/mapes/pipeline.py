from __future__ import annotations

import json
from pathlib import Path
from typing import List

from .judges.ernie_judge import JudgeProvider, get_judge_provider
from .models import EvaluationCase, EvaluationReport
from .ocr.paddle_ocr_client import PaddleOCRClient
from .report import build_report


def load_cases(path: str) -> List[EvaluationCase]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        raw = raw.get("cases", [])
    return [EvaluationCase.model_validate(item) for item in raw]


def enrich_with_ocr(case: EvaluationCase, ocr_client: PaddleOCRClient | None = None) -> EvaluationCase:
    if case.ocr_context or not case.image_path:
        return case
    client = ocr_client or PaddleOCRClient()
    try:
        text = client.extract_text(case.image_path)
        return case.model_copy(update={"ocr_context": text})
    except Exception as exc:
        metadata = dict(case.metadata)
        metadata["ocr_error"] = str(exc)
        return case.model_copy(update={"metadata": metadata})


def evaluate_case(case: EvaluationCase, judge: JudgeProvider | None = None) -> EvaluationReport:
    case = enrich_with_ocr(case)
    provider = judge or get_judge_provider()
    judge_result = provider.evaluate(case)
    return build_report(case, judge_result)


def evaluate_file(input_path: str, output_path: str) -> List[EvaluationReport]:
    reports = [evaluate_case(case) for case in load_cases(input_path)]
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps([r.model_dump() for r in reports], ensure_ascii=False, indent=2), encoding="utf-8")
    return reports
