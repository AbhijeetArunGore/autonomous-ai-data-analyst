import pytest
import os
import tempfile
import sqlite3
import pandas as pd
from backend.app.storage.data_source import FileDataSource, SQLDataSource

def test_parquet_and_json_data_source():
    df_raw = pd.DataFrame({"id": [1, 2, 3], "val": [10.0, 20.0, 30.0]})
    
    with tempfile.NamedTemporaryFile(suffix=".parquet", delete=False) as f:
        parquet_path = f.name
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        json_path = f.name
        
    try:
        df_raw.to_parquet(parquet_path)
        df_raw.to_json(json_path)
        
        ds_pq = FileDataSource(parquet_path)
        assert ds_pq.get_source_type() == "parquet"
        df_pq = ds_pq.read_dataframe()
        assert df_pq.shape == (3, 2)
        
        ds_js = FileDataSource(json_path)
        assert ds_js.get_source_type() == "json"
        df_js = ds_js.read_dataframe()
        assert df_js.shape == (3, 2)
    finally:
        if os.path.exists(parquet_path):
            os.remove(parquet_path)
        if os.path.exists(json_path):
            os.remove(json_path)

def test_sql_data_source():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
        
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE sales (id INT, amount FLOAT)")
        conn.execute("INSERT INTO sales VALUES (1, 100.0), (2, 200.0)")
        conn.commit()
        conn.close()
        
        sql_ds = SQLDataSource(f"sqlite:///{db_path}", "SELECT * FROM sales")
        df_sql = sql_ds.read_dataframe()
        assert df_sql.shape == (2, 2)
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
