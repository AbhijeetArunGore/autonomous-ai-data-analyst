from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AnalysisPlan(BaseModel):
    goal: str
    objectives: List[str]
    required_analysis: List[str]
    optional_analysis: List[str] = []
    kpis: List[str]
    features: List[str]
    statistical_tests: List[str]
    visualizations: List[str]
    risks: List[str] = []
    validation_rules: List[str] = []
