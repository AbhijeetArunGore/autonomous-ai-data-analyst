from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ResearchReport(BaseModel):
    methodology: str
    relevant_kpis: List[str]
    statistical_methods: List[str]
    potential_pitfalls: List[str]
    recommended_segmentations: List[str]
    domain_insights: Optional[str] = None
