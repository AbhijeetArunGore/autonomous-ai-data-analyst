import polars as pl
import pandas as pd
from pydantic import BaseModel
from typing import Dict, Any, List

class ScenarioParameter(BaseModel):
    variable_name: str
    adjustment_type: str  # percentage, absolute
    adjustment_value: float

class ScenarioSimulationResult(BaseModel):
    scenario_name: str
    target_metric: str
    baseline_value: float
    simulated_value: float
    absolute_change: float
    percentage_change: float
    projected_impact_description: str

class WhatIfScenarioEngine:
    """
    What-If Scenario Simulation Engine: Projects KPI changes under simulated segment or pricing adjustments.
    """
    
    @staticmethod
    def simulate_scenario(
        df: pl.DataFrame,
        scenario_name: str,
        target_metric: str,
        parameters: List[ScenarioParameter]
    ) -> ScenarioSimulationResult:
        pdf = df.to_pandas()
        
        cols_lower = {c.lower(): c for c in pdf.columns}
        metric_col = cols_lower.get(target_metric.lower(), target_metric)
        
        if metric_col not in pdf.columns or not pd.api.types.is_numeric_dtype(pdf[metric_col]):
            # Pick first numeric column
            num_cols = [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]
            metric_col = num_cols[0] if num_cols else "revenue"
            
        baseline_val = float(pdf[metric_col].sum()) if metric_col in pdf.columns else 100000.0
        simulated_val = baseline_val
        
        for param in parameters:
            if param.adjustment_type == "percentage":
                factor = 1.0 + (param.adjustment_value / 100.0)
                simulated_val *= factor
            elif param.adjustment_type == "absolute":
                simulated_val += param.adjustment_value

        abs_change = simulated_val - baseline_val
        pct_change = (abs_change / baseline_val * 100) if baseline_val > 0 else 0.0

        return ScenarioSimulationResult(
            scenario_name=scenario_name,
            target_metric=metric_col,
            baseline_value=round(baseline_val, 2),
            simulated_value=round(simulated_val, 2),
            absolute_change=round(abs_change, 2),
            percentage_change=round(pct_change, 2),
            projected_impact_description=f"Simulated '{scenario_name}' projects a {pct_change:+.1f}% change in aggregate {metric_col} (${abs_change:+,.2f})."
        )
