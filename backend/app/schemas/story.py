from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ExecutiveStory(BaseModel):
    headline: str
    what_happened: str
    why_it_matters: str
    primary_drivers: str
    recommended_actions: str
    narration_script: str  # Audio TTS script text

class TechnicalStory(BaseModel):
    methodology_summary: str
    data_transformations: str
    statistical_findings: str
    model_performance: str
    limitations_and_assumptions: str

class DualStoryReport(BaseModel):
    executive_version: ExecutiveStory
    technical_version: TechnicalStory
