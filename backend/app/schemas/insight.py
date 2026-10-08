from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class InsightCard(BaseModel):
    title: str
    evidence: str
    metric: str
    magnitude: str
    explanation: str
    confidence: str  # High, Medium, Low
    business_implication: str

class InsightReport(BaseModel):
    insights: List[InsightCard]
