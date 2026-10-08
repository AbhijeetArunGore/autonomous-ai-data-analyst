from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class NumericStats(BaseModel):
    mean: float
    std: float
    min: float
    q25: float
    median: float
    q75: float
    max: float
    skewness: float
    outlier_count_iqr: int

class CategoricalStats(BaseModel):
    top_categories: Dict[str, int]
    cardinality: int
    is_high_cardinality: bool

class DateStats(BaseModel):
    min_date: Optional[str]
    max_date: Optional[str]
    date_range_days: Optional[float]

class ColumnProfile(BaseModel):
    column_name: str
    data_type: str
    count: int
    missing_count: int
    missing_percentage: float
    unique_count: int
    cardinality_ratio: float
    is_constant: bool
    is_near_constant: bool
    is_possible_identifier: bool
    is_possible_target: bool
    numeric_stats: Optional[NumericStats] = None
    categorical_stats: Optional[CategoricalStats] = None
    date_stats: Optional[DateStats] = None

class DataProfile(BaseModel):
    dataset_id: str
    total_rows: int
    total_columns: int
    duplicate_rows_count: int
    duplicate_rows_percentage: float
    columns: Dict[str, ColumnProfile]
    correlation_matrix: Dict[str, Dict[str, float]] = {}
    suspicious_columns: List[str] = []
    potential_leakage_columns: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
