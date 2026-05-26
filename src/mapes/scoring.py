from __future__ import annotations

from typing import Dict

METRIC_WEIGHTS: Dict[str, float] = {
    "persona_consistency": 0.20,
    "personality_expressiveness": 0.15,
    "context_awareness": 0.20,
    "emotional_alignment": 0.15,
    "multi_agent_collaboration": 0.20,
    "hallucination_safety": 0.10,
}


def normalize_score(value: float) -> float:
    return max(0.0, min(5.0, float(value)))


def calculate_final_score(scores: Dict[str, float]) -> float:
    weighted = 0.0
    for key, weight in METRIC_WEIGHTS.items():
        weighted += normalize_score(scores.get(key, 0.0)) * weight
    return round(weighted / 5.0 * 100.0, 2)


def grade_for_score(score: float) -> str:
    if score >= 90:
        return "S"
    if score >= 80:
        return "A"
    if score >= 70:
        return "B"
    if score >= 60:
        return "C"
    return "D"
