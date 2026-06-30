from pydantic import BaseModel, Field
from typing import Optional


class ReorderRecommendation(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    reorder_level: int
    recommended_quantity: int
    urgency: str = Field(description="immediate/soon/planned")
    explanation: str
    supplier_suggestion: Optional[str] = None
    confidence: float = Field(ge=0, le=100)


class SupplierComparisonItem(BaseModel):
    supplier_name: str
    unit_cost: float
    lead_time_days: int
    reliability_score: float
    quality_score: float
    overall_score: float
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)


class SupplierComparisonResponse(BaseModel):
    recommendations: list[ReorderRecommendation] = Field(default_factory=list)
    ai_analysis: str
    confidence: float = Field(ge=0, le=100)


class WhatIfScenario(BaseModel):
    scenario_description: str
    affected_products: list[str] = Field(default_factory=list)
    estimated_impact: str
    mitigation_suggestions: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=100)
