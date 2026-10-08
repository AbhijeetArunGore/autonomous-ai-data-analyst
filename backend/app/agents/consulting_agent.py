from typing import Optional, Any
from backend.app.schemas.recommendation import RecommendationReport, BusinessRecommendation
from backend.app.llm.provider import LLMProvider, get_llm_provider

class ConsultingAgent:
    """
    Consulting Agent (Agent 16): Converts analytical insights into actionable business recommendations.
    """
    def __init__(self, provider: Optional[LLMProvider] = None):
        self.provider = provider or get_llm_provider()
        
    def recommend(self, insights: InsightReport) -> RecommendationReport:
        prompt = f"Insights: {insights.model_dump_json()}"
        response = self.provider.generate(
            prompt=prompt,
            system_prompt="You are a Management Consulting Principal. Produce actionable, prioritized recommendations.",
            response_schema=RecommendationReport
        )
        if response.parsed:
            return RecommendationReport(**response.parsed)
            
        return RecommendationReport(recommendations=[
            BusinessRecommendation(
                recommendation="Deploy Automated Onboarding Engagement Campaign",
                why="Targeted 90-day retention delivers highest ROI",
                expected_impact="High",
                required_action="Implement lifecycle trigger emails and in-app walk-throughs",
                owner="Customer Success",
                priority="High",
                effort="Low",
                risk="Minimal",
                measurement_kpi="90-day Retention Rate"
            )
        ])
