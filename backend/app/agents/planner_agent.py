from typing import Optional
from backend.app.schemas.profiling import DataProfile
from backend.app.schemas.research import ResearchReport
from backend.app.schemas.plan import AnalysisPlan
from backend.app.llm.provider import LLMProvider, get_llm_provider

class PlannerAgent:
    """
    Planner Agent (Agent 4): Synthesizes business objective, profile, and research report
    into an executable analytical plan specifying required node tasks and validation rules.
    """
    
    def __init__(self, provider: Optional[LLMProvider] = None):
        self.provider = provider or get_llm_provider()
        
    def plan(self, business_goal: str, profile: DataProfile, research: ResearchReport) -> AnalysisPlan:
        prompt = f"""
Business Goal: {business_goal}
Profile Summary: Rows={profile.total_rows}, Cols={profile.total_columns}, Suspicious Cols={profile.suspicious_columns}
Research Methodology: {research.methodology}
Recommended KPIs: {research.relevant_kpis}

Construct an executable analytical plan.
"""
        system_prompt = "You are an Analytics Lead Planner. Decide exact required analytical steps, KPIs, features, statistical tests, and visualizations."
        response = self.provider.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            response_schema=AnalysisPlan
        )
        
        if response.parsed:
            return AnalysisPlan(**response.parsed)
        return AnalysisPlan(
            goal=business_goal,
            objectives=["Data Quality Assessment", "KPI Discovery", "Statistical Testing"],
            required_analysis=["data_quality", "kpi_discovery", "statistical_testing", "visualization"],
            kpis=research.relevant_kpis,
            features=["tenure", "recency"],
            statistical_tests=research.statistical_methods,
            visualizations=["bar_chart", "line_chart"]
        )
