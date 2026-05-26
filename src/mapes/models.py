from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class AgentRole(BaseModel):
    name: str
    role: str


class AgentSetting(BaseModel):
    agent_count: int = 1
    agents: List[AgentRole] = Field(default_factory=list)


class EvaluationCase(BaseModel):
    case_id: str
    scenario_type: str
    scene_context: str
    agent_setting: AgentSetting
    agent_output: str
    ocr_context: str = ""
    image_path: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class JudgeResult(BaseModel):
    scores: Dict[str, float]
    reasons: Dict[str, str] = Field(default_factory=dict)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    improvement_suggestions: List[str] = Field(default_factory=list)
    overall_comment: str = ""


class EvaluationReport(BaseModel):
    case_id: str
    scenario_type: str
    final_score: float
    grade: str
    scores: Dict[str, float]
    reasons: Dict[str, str]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: List[str]
    overall_comment: str
    warnings: List[str] = Field(default_factory=list)
