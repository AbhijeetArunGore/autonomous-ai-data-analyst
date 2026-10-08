from typing import Optional
from backend.app.schemas.profiling import DataProfile
from backend.app.schemas.research import ResearchReport
from backend.app.llm.provider import LLMProvider, get_llm_provider

class ResearcherAgent:
    """
    Researcher Agent (Agent 3): Researches analytical methodology, relevant KPIs,
    pitfalls, and segmentation strategies based on business goal and dataset profile.
    """
    
    def __init__(self, provider: Optional[LLMProvider] = None):
        self.provider = provider or get_llm_provider()
        
    def research(self, business_goal: str, profile: DataProfile, domain_context: str = "") -> ResearchReport:
        prompt = f"""
Business Objective: {business_goal}
Domain Context: {domain_context}
Dataset Metadata: Total Rows={profile.total_rows}, Total Columns={profile.total_columns}
Columns: {list(profile.columns.keys())}

Conduct methodological research for this analytical goal. Identify:
1. Standard analytical methodology
2. Relevant KPIs to derive
3. Recommended statistical tests
4. Potential data quality or analytical pitfalls
5. Recommended segmentation dimensions
"""
        system_prompt = "You are a Senior Analytics Researcher. Produce structured analytical methodology."
        response = self.provider.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            response_schema=ResearchReport
        )
        
        if response.parsed:
            return ResearchReport(**response.parsed)
        return ResearchReport(
            methodology=response.content,
            relevant_kpis=["Revenue", "Retention", "Conversion"],
            statistical_methods=["Descriptive", "Correlation"],
            potential_pitfalls=["Missing data", "Class imbalance"],
            recommended_segmentations=["Customer Type"]
        )
