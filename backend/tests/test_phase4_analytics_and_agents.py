import pytest
import polars as pl
import pandas as pd
from backend.app.analytics.quality import DataQualityAnalyzer
from backend.app.analytics.imputation import MissingValueEngine
from backend.app.analytics.kpi import DeterministicKPIEngine
from backend.app.analytics.feature_engineering import FeatureEngineeringEngine
from backend.app.analytics.statistics import StatisticalAnalysisEngine
from backend.app.analytics.ml_engine import MLEngine
from backend.app.analytics.anomaly import AnomalyDetectionEngine
from backend.app.analytics.segmentation import SegmentationEngine
from backend.app.validators.validation_engine import ValidationEngine
from backend.app.agents.storytelling_agent import StorytellingAgent

@pytest.fixture
def sample_sales_df():
    data = {
        "customer_id": [f"C{i:03d}" for i in range(1, 41)],
        "age": [25, 30, 45, 22, 35, 50, 28, 40, 60, 32] * 4,
        "revenue": [100.0, 250.0, 500.0, 80.0, 300.0, 750.0, 150.0, 420.0, 900.0, 200.0] * 4,
        "churn": [0, 0, 1, 0, 0, 1, 0, 0, 1, 0] * 4,
        "signup_date": ["2023-01-01", "2023-01-15", "2023-02-01", "2023-02-10"] * 10
    }
    return pl.from_pandas(pd.DataFrame(data))

def test_data_quality_and_imputation(sample_sales_df):
    quality_result = DataQualityAnalyzer.analyze(sample_sales_df)
    assert quality_result.total_issues >= 0
    
    imputed_df, report = MissingValueEngine.impute(sample_sales_df, {"age": "median"})
    assert imputed_df.shape == sample_sales_df.shape

def test_kpi_engine(sample_sales_df):
    catalog = DeterministicKPIEngine.discover_and_compute(sample_sales_df, "Increase revenue and reduce churn")
    kpi_names = [k.name for k in catalog.kpis]
    assert "Total Revenue" in kpi_names or "Average Order Value (AOV)" in kpi_names
    assert len(catalog.kpis) > 0

def test_feature_engineering_engine(sample_sales_df):
    transformed_df, catalog = FeatureEngineeringEngine.transform(sample_sales_df)
    assert transformed_df.shape[1] >= sample_sales_df.shape[1]
    assert len(catalog.features) > 0

def test_statistical_and_ml_engines(sample_sales_df):
    stats_report = StatisticalAnalysisEngine.analyze(sample_sales_df, target_col="churn")
    assert len(stats_report.tests) > 0
    assert stats_report.tests[0].causal_warning != ""
    
    ml_report = MLEngine.train_and_evaluate(sample_sales_df, target_col="churn")
    assert ml_report.task_type == "classification"
    assert len(ml_report.models_evaluated) > 0

def test_anomaly_and_segmentation(sample_sales_df):
    anom_report = AnomalyDetectionEngine.detect(sample_sales_df)
    assert anom_report.total_anomalies_detected >= 0
    
    seg_report = SegmentationEngine.segment(sample_sales_df, k=3)
    assert len(seg_report.segments) == 3

def test_validation_and_storytelling(sample_sales_df):
    kpi_cat = DeterministicKPIEngine.discover_and_compute(sample_sales_df, "Goal")
    val_report = ValidationEngine.validate_analysis(
        df_rows=sample_sales_df.shape[0],
        kpi_catalog=kpi_cat,
        stats_report=None,
        ml_report=None,
        insights=[{"title": "Test Insight", "evidence": "p < 0.05"}],
        recommendations=[]
    )
    assert val_report.is_valid is True
    
    story_agent = StorytellingAgent()
    dual_story = story_agent.generate_story(insights=[], recommendations=[])
    assert dual_story.executive_version.narration_script != ""
