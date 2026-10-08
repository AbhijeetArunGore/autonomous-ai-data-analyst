from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class BusinessRecommendation(BaseModel):
    recommendation: str
    why: str
    expected_impact: str  # High, Medium, Low
    required_action: str
    owner: str
    priority: str  # High, Medium, Low
    effort: str    # Low, Medium, High
    risk: str
    measurement_kpi: str

class RecommendationReport(BaseModel):
    recommendations: List[BusinessRecommendation]
