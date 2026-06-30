from pydantic import BaseModel, Field
from typing import Optional


class RiskItem(BaseModel):
    severity: str = Field(description="critical/high/medium/low")
    probability: float = Field(ge=0, le=100, description="0-100 percentage")
    business_impact: str
    description: str
    recommended_action: str
    evidence: str


class OpportunityItem(BaseModel):
    category: str
    description: str
    potential_impact: str
    recommended_action: str
    confidence: float = Field(ge=0, le=100)


class ActionItem(BaseModel):
    action: str
    reason: str
    urgency: str = Field(description="immediate/today/week/month")
    link: Optional[str] = None


class ExecutiveSummary(BaseModel):
    business_health_score: int = Field(ge=0, le=100)
    health_explanation: str
    summary: str
    top_risks: list[RiskItem] = Field(default_factory=list)
    top_opportunities: list[OpportunityItem] = Field(default_factory=list)
    recommended_actions: list[ActionItem] = Field(default_factory=list)
    key_metrics_summary: str


class HealthScoreResponse(BaseModel):
    score: int = Field(ge=0, le=100)
    explanation: str
    risks: list[RiskItem] = Field(default_factory=list)
    opportunities: list[OpportunityItem] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    confidence: float = Field(ge=0, le=100)
    evidence: list[str] = Field(default_factory=list)
    suggested_followups: list[str] = Field(default_factory=list)
