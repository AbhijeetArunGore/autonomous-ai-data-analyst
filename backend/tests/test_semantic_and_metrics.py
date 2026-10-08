import pytest
import polars as pl
import pandas as pd
from backend.app.analytics.semantic_layer import UniversalSemanticMapper
from backend.app.analytics.metric_registry import MetricRegistry

def test_universal_semantic_mapper():
    data = {
        "patient_id": [f"P{i:03d}" for i in range(10)],
        "admission_date": ["2023-01-01"] * 10,
        "length_of_stay": [3, 5, 2, 8, 4, 6, 1, 7, 3, 5],
        "readmission_flag": [0, 1, 0, 0, 1, 0, 0, 1, 0, 0]
    }
    df = pl.from_pandas(pd.DataFrame(data))
    schema = UniversalSemanticMapper.infer_semantics(df)
    
    assert schema.primary_entity_id == "patient_id"
    assert "readmission_flag" in schema.target_candidates
    assert schema.timestamp_column == "admission_date"

def test_metric_registry():
    saas_metrics = MetricRegistry.list_metrics("SaaS")
    assert len(saas_metrics) > 0
    assert saas_metrics[0].metric_name == "Customer Churn Rate"
    
    health_metrics = MetricRegistry.list_metrics("Healthcare")
    assert len(health_metrics) > 0
    assert health_metrics[0].metric_name == "30-Day Readmission Rate"
