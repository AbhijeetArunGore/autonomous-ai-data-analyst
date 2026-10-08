import pytest
import os
import tempfile
import polars as pl
from backend.app.agents.intake_agent import DataIntakeAgent
from backend.app.agents.profiler_agent import DataProfilingAgent

def test_data_intake_agent_csv():
    csv_content = """customer_id,age,income,churn,signup_date
C101,25,50000.0,0,2023-01-15
C102,34,75000.5,1,2023-02-20
C103,45,,0,2023-03-10
C104,25,50000.0,0,2023-01-15
"""
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False, encoding="utf-8") as f:
        f.write(csv_content)
        temp_path = f.name
        
    try:
        agent = DataIntakeAgent()
        metadata, df = agent.process_file(temp_path, "test_customers.csv")
        
        assert metadata.filename == "test_customers.csv"
        assert metadata.rows == 4
        assert metadata.columns == 5
        assert metadata.file_format == "csv"
        assert metadata.delimiter == ","
        assert isinstance(df, pl.DataFrame)
    finally:
        os.remove(temp_path)

def test_data_profiling_agent():
    csv_content = """customer_id,age,income,churn
C101,20,30000,0
C102,30,50000,0
C103,40,70000,1
C104,50,90000,1
C105,60,110000,1
"""
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w", delete=False, encoding="utf-8") as f:
        f.write(csv_content)
        temp_path = f.name
        
    try:
        intake = DataIntakeAgent()
        metadata, df = intake.process_file(temp_path, "profiling_test.csv")
        
        profiler = DataProfilingAgent()
        profile = profiler.profile(df, metadata.dataset_id)
        
        assert profile.total_rows == 5
        assert profile.total_columns == 4
        assert "age" in profile.columns
        assert profile.columns["age"].numeric_stats.mean == 40.0
        assert profile.columns["age"].numeric_stats.median == 40.0
        assert profile.columns["age"].numeric_stats.min == 20.0
        assert profile.columns["age"].numeric_stats.max == 60.0
        assert profile.columns["churn"].is_possible_target is True
    finally:
        os.remove(temp_path)
