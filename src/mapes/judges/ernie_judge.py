from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Protocol

import requests

from mapes.models import EvaluationCase, JudgeResult


class JudgeProvider(Protocol):
    def evaluate(self, case: EvaluationCase) -> JudgeResult:
        ...


class MockJudge:
    """Deterministic fallback so the MVP can run without external credentials."""

    def evaluate(self, case: EvaluationCase) -> JudgeResult:
        collaboration = 4 if case.agent_setting.agent_count > 1 else 2
        context = 4 if case.ocr_context else 3
        return JudgeResult(
            scores={
                "persona_consistency": 4,
                "personality_expressiveness": 3,
                "context_awareness": context,
                "emotional_alignment": 4,
                "multi_agent_collaboration": collaboration,
                "hallucination_safety": 4,
            },
            reasons={
                "persona_consistency": "输出基本围绕角色设定展开。",
                "personality_expressiveness": "有一定表达风格，但仍可进一步增强独特口吻。",
                "context_awareness": "能使用主要场景信息。",
                "emotional_alignment": "回应中包含安抚和陪伴。",
                "multi_agent_collaboration": "多Agent具备基本分工，但仍需减少重复。",
                "hallucination_safety": "未发现明显危险建议或事实编造。",
            },
            strengths=["评分闭环可运行", "角色和场景信息被纳入评估"],
            weaknesses=["Mock Judge 不能代表真实模型判断", "多Agent协作证据需要更细粒度日志"],
            improvement_suggestions=["接入真实ERNIE API", "记录每个Agent的发言顺序和职责命中情况"],
            overall_comment="该案例达到MVP演示水平。",
        )


class ErnieJudge:
    def __init__(self, api_url: str | None = None, api_key: str | None = None, prompt_path: str | None = None):
        self.api_url = api_url or os.getenv("ERNIE_API_URL")
        self.api_key = api_key or os.getenv("ERNIE_API_KEY")
        self.prompt_template = Path(prompt_path or "prompts/ernie_judge_prompt.txt").read_text(encoding="utf-8")
        if not self.api_url or not self.api_key:
            raise ValueError("ERNIE_API_URL and ERNIE_API_KEY are required for ErnieJudge")

    def render_prompt(self, case: EvaluationCase) -> str:
        prompt = self.prompt_template
        replacements = {
            "{{scenario_type}}": case.scenario_type,
            "{{scene_context}}": case.scene_context,
            "{{ocr_context}}": case.ocr_context or "无",
            "{{agent_setting}}": case.agent_setting.model_dump_json(),
            "{{agent_output}}": case.agent_output,
        }
        for key, value in replacements.items():
            prompt = prompt.replace(key, value)
        return prompt

    def evaluate(self, case: EvaluationCase) -> JudgeResult:
        prompt = self.render_prompt(case)
        response = requests.post(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={"messages": [{"role": "user", "content": prompt}], "temperature": 0.1},
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        content = payload.get("result") or payload.get("choices", [{}])[0].get("message", {}).get("content")
        if not content:
            raise ValueError(f"Cannot find judge content in ERNIE response: {payload}")
        return JudgeResult.model_validate(json.loads(content))


def get_judge_provider() -> JudgeProvider:
    provider = os.getenv("MAPES_JUDGE_PROVIDER", "mock").lower()
    if provider == "ernie":
        return ErnieJudge()
    return MockJudge()
