import pytest
import polars as pl
import pandas as pd
from backend.app.analytics.root_cause import RootCauseAnalysisEngine
from backend.app.analytics.scenario_engine import WhatIfScenarioEngine, ScenarioParameter

@pytest.fixture
def rca_df():
    data = {
        "customer_id": [f"C{i}" for i in range(20)],
        "segment_is_smb": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "support_tickets": [5, 6, 7, 8, 5, 6, 7, 8, 9, 6, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2],
        "churn": [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
    return pl.from_pandas(pd.DataFrame(data))

def test_root_cause_analysis(rca_df):
    report = RootCauseAnalysisEngine.analyze_root_causes(rca_df, target_col="churn")
    assert report.target_metric == "churn"
    assert len(report.top_root_causes) > 0
    assert report.top_root_causes[0].contribution_score > 0

def test_scenario_engine(rca_df):
    sim = WhatIfScenarioEngine.simulate_scenario(
        df=rca_df,
        scenario_name="5% Retention Boost",
        target_metric="churn",
        parameters=[
            ScenarioParameter(variable_name="retention", adjustment_type="percentage", adjustment_value=-5.0)
        ]
    )
    assert sim.percentage_change == -5.0
    assert sim.simulated_value < sim.baseline_value
