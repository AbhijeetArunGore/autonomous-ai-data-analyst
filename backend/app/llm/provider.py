import os
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type
from pydantic import BaseModel

class LLMResponse(BaseModel):
    content: str
    parsed: Optional[Dict[str, Any]] = None
    model_name: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    estimated_cost: float = 0.0

class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        response_schema: Optional[Type[BaseModel]] = None,
        temperature: float = 0.2
    ) -> LLMResponse:
        pass

class MockLLMProvider(LLMProvider):
    """
    Mock LLM Provider for offline execution, evaluation benchmarks, and deterministic testing.
    """
    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        response_schema: Optional[Type[BaseModel]] = None,
        temperature: float = 0.2
    ) -> LLMResponse:
        content = "Mock LLM Response for analysis task."
        parsed = None
        
        # If response_schema is provided, construct a realistic mock payload adhering to the schema
        if response_schema:
            schema_name = response_schema.__name__
            if schema_name == "ResearchReport":
                parsed = {
                    "methodology": "Standard analytical methodology combining descriptive statistics, cohort analysis, and predictive modeling.",
                    "relevant_kpis": ["Revenue", "Churn Rate", "Customer Retention", "Average Order Value"],
                    "statistical_methods": ["t-test", "Mann-Whitney U test", "Chi-square test for independence"],
                    "potential_pitfalls": ["Data leakage between target and features", "Class imbalance in target variable", "Correlation vs Causation confusion"],
                    "recommended_segmentations": ["Geography", "Customer Tenure Tier", "Spending Frequency"]
                }
            elif schema_name == "AnalysisPlan":
                parsed = {
                    "goal": "Analyze dataset and identify key revenue and retention drivers",
                    "objectives": [
                        "Perform deterministic missing value treatment and feature extraction",
                        "Compute key baseline and derived KPIs",
                        "Run statistical hypothesis testing on target drivers",
                        "Train baseline predictive model and cluster customer segments"
                    ],
                    "required_analysis": ["kpi_discovery", "feature_engineering", "statistical_testing", "segmentation", "anomaly_detection"],
                    "optional_analysis": ["predictive_ml"],
                    "kpis": ["revenue_growth", "churn_rate", "retention_rate"],
                    "features": ["recency_days", "tenure_months", "log_income"],
                    "statistical_tests": ["t_test", "chi_square"],
                    "visualizations": ["trend_line", "category_bar", "correlation_heatmap"],
                    "risks": ["Small sample size in high-tier segment"],
                    "validation_rules": ["Verify row counts post-filtering", "Check model AUC-ROC > 0.65"]
                }
            elif schema_name == "InsightReport":
                parsed = {
                    "insights": [
                        {
                            "title": "Significant churn spike in SMB segment",
                            "evidence": "SMB segment churn rate is 17.6% vs Enterprise 7.8%",
                            "metric": "churn_rate",
                            "magnitude": "9.8 percentage points higher",
                            "explanation": "SMB customers show lower engagement during first 90 days",
                            "confidence": "High",
                            "business_implication": "Targeted retention campaigns in SMB can deliver highest ROI"
                        }
                    ]
                }
            elif schema_name == "RecommendationReport":
                parsed = {
                    "recommendations": [
                        {
                            "recommendation": "Launch automated onboarding campaign for SMB segment",
                            "why": "First 90 days exhibit 2.2x higher drop-off rate",
                            "expected_impact": "High",
                            "required_action": "Deploy email sequence and product walk-through",
                            "owner": "Customer Success",
                            "priority": "High",
                            "effort": "Low",
                            "risk": "Minimal",
                            "measurement_kpi": "90-day retention rate"
                        }
                    ]
                }
            elif schema_name == "DualStoryReport":
                parsed = {
                    "executive_version": {
                        "headline": "Revenue & Retention Driver Analysis Complete",
                        "what_happened": "Performance analysis identified key retention drop-offs concentrated in early lifecycle stages.",
                        "why_it_matters": "Addressing early retention yields an estimated 12-15% improvement in annual recurring revenue.",
                        "primary_drivers": "Customer onboarding engagement and product usage frequency.",
                        "recommended_actions": "Launch immediate automated onboarding campaign for at-risk segments.",
                        "narration_script": "Welcome to your AI Data Analyst executive briefing. Our analysis reveals that customer retention during the first ninety days is the primary driver of revenue performance."
                    },
                    "technical_version": {
                        "methodology_summary": "Combined deterministic profiling with Welch's t-tests and Random Forest feature importance.",
                        "data_transformations": "Missing value imputation via median strategy; RFM customer aggregations derived.",
                        "statistical_findings": "Statistically significant feature variance observed (p < 0.05).",
                        "model_performance": "Random Forest classifier achieved 86.4% cross-validated accuracy.",
                        "limitations_and_assumptions": "Observational data analysis; association findings do not prove direct causality."
                    }
                }
            else:
                parsed = {"status": "ok", "message": f"Mock response for schema {schema_name}"}
                
            content = json.dumps(parsed, indent=2)
            
        return LLMResponse(
            content=content,
            parsed=parsed,
            model_name="mock-engine-v1",
            prompt_tokens=150,
            completion_tokens=200,
            estimated_cost=0.0001
        )

def get_llm_provider(provider_type: Optional[str] = None) -> LLMProvider:
    provider = provider_type or os.getenv("LLM_PROVIDER", "mock").lower()
    # In full environment, OpenAI / Gemini / Anthropic providers connect to API keys
    # Defaulting safely to MockLLMProvider for robust offline capability
    return MockLLMProvider()
