import pytest
import polars as pl
import pandas as pd
from backend.app.analytics.forecasting import ForecastingEngine

def test_forecasting_engine():
    data = {
        "transaction_date": ["2023-01-15", "2023-02-15", "2023-03-15", "2023-04-15", "2023-05-15", "2023-06-15"],
        "revenue": [1000.0, 1200.0, 1500.0, 1400.0, 1800.0, 2100.0]
    }
    df = pl.from_pandas(pd.DataFrame(data))
    
    report = ForecastingEngine.forecast(df, target_col="revenue", periods=3)
    assert report.metric_name == "revenue"
    assert report.periods_forecasted == 3
    assert len(report.data_points) == 9  # 6 historical + 3 forecast
