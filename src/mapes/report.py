from __future__ import annotations

from .models import EvaluationCase, EvaluationReport, JudgeResult
from .scoring import METRIC_WEIGHTS, calculate_final_score, grade_for_score


def build_report(case: EvaluationCase, judge_result: JudgeResult) -> EvaluationReport:
    warnings = []
    for metric in METRIC_WEIGHTS:
        if metric not in judge_result.scores:
            warnings.append(f"Missing score for {metric}; treated as 0.")
    final_score = calculate_final_score(judge_result.scores)
    return EvaluationReport(
        case_id=case.case_id,
        scenario_type=case.scenario_type,
        final_score=final_score,
        grade=grade_for_score(final_score),
        scores={k: float(judge_result.scores.get(k, 0.0)) for k in METRIC_WEIGHTS},
        reasons=judge_result.reasons,
        strengths=judge_result.strengths,
        weaknesses=judge_result.weaknesses,
        improvement_suggestions=judge_result.improvement_suggestions,
        overall_comment=judge_result.overall_comment,
        warnings=warnings,
    )
