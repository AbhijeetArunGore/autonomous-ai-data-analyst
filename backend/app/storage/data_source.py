import os
import json
import sqlite3
import pandas as pd
import polars as pl
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Tuple

class DataSource(ABC):
    """
    Universal Data Source Abstraction: Standard interface for loading, querying,
    sampling, and profiling arbitrary data sources (CSV, Excel, Parquet, JSON, SQL).
    """
    
    @abstractmethod
    def read_dataframe(self) -> pl.DataFrame:
        pass
        
    @abstractmethod
    def get_source_type(self) -> str:
        pass

class FileDataSource(DataSource):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.ext = os.path.splitext(file_path)[1].lower()

    def get_source_type(self) -> str:
        return self.ext[1:]

    def read_dataframe(self) -> pl.DataFrame:
        if self.ext == ".csv":
            try:
                return pl.read_csv(self.file_path, ignore_errors=True)
            except Exception:
                pdf = pd.read_csv(self.file_path, on_bad_lines='skip')
                return pl.from_pandas(pdf)
        elif self.ext in [".xlsx", ".xls"]:
            pdf = pd.read_excel(self.file_path)
            return pl.from_pandas(pdf)
        elif self.ext == ".parquet":
            return pl.read_parquet(self.file_path)
        elif self.ext == ".json":
            pdf = pd.read_json(self.file_path)
            return pl.from_pandas(pdf)
        else:
            raise ValueError(f"Unsupported data source extension: {self.ext}")

class SQLDataSource(DataSource):
    def __init__(self, connection_string: str, query: str):
        self.connection_string = connection_string
        self.query = query

    def get_source_type(self) -> str:
        return "sql"

    def read_dataframe(self) -> pl.DataFrame:
        conn = sqlite3.connect(self.connection_string.replace("sqlite:///", ""))
        pdf = pd.read_sql_query(self.query, conn)
        conn.close()
        return pl.from_pandas(pdf)
