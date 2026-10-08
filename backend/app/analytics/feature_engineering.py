import polars as pl
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Any, Tuple

class FeatureLineage(BaseModel):
    feature_name: str
    source_columns: List[str]
    transformation: str
    reason: str

class FeatureCatalog(BaseModel):
    features: List[FeatureLineage]

class FeatureEngineeringEngine:
    """
    Feature Engineering Engine: Derives datetime features, log transformations,
    RFM metrics, and category frequency encodings with full lineage tracking.
    """
    
    @staticmethod
    def transform(df: pl.DataFrame) -> Tuple[pl.DataFrame, FeatureCatalog]:
        pdf = df.to_pandas()
        lineages: List[FeatureLineage] = []
        
        for col in list(pdf.columns):
            # 1. Datetime feature derivation
            if pd.api.types.is_datetime64_any_dtype(pdf[col]) or "date" in col.lower():
                try:
                    dt_series = pd.to_datetime(pdf[col], errors='coerce')
                    if dt_series.notnull().sum() > 0:
                        pdf[f"{col}_year"] = dt_series.dt.year
                        pdf[f"{col}_month"] = dt_series.dt.month
                        pdf[f"{col}_quarter"] = dt_series.dt.quarter
                        pdf[f"{col}_dayofweek"] = dt_series.dt.dayofweek
                        pdf[f"{col}_is_weekend"] = (dt_series.dt.dayofweek >= 5).astype(int)
                        
                        lineages.append(FeatureLineage(
                            feature_name=f"{col}_datetime_components",
                            source_columns=[col],
                            transformation="Date Component Extraction (Year, Month, Quarter, DayOfWeek, IsWeekend)",
                            reason="Enables trend, seasonality, and day-of-week behavioral analysis"
                        ))
                except Exception:
                    pass
                    
            # 2. Skewed numeric log transformation
            elif pd.api.types.is_numeric_dtype(pdf[col]):
                vals = pdf[col].dropna()
                if len(vals) > 0 and vals.min() >= 0:
                    skewness = float(vals.skew())
                    if skewness > 1.5:
                        pdf[f"{col}_log"] = np.log1p(pdf[col])
                        lineages.append(FeatureLineage(
                            feature_name=f"{col}_log",
                            source_columns=[col],
                            transformation="np.log1p(x)",
                            reason=f"Mitigates high positive skewness (skewness={skewness:.2f}) for statistical stability"
                        ))

        # 3. RFM Feature Derivation if customer_id, date, and monetary columns exist
        cols_lower = {c.lower(): c for c in pdf.columns}
        cust_col = cols_lower.get("customer_id") or cols_lower.get("customerid") or cols_lower.get("user_id")
        date_col = cols_lower.get("date") or cols_lower.get("transaction_date") or cols_lower.get("signup_date")
        rev_col = cols_lower.get("revenue") or cols_lower.get("sales") or cols_lower.get("amount")
        
        if cust_col and date_col and rev_col and pd.api.types.is_numeric_dtype(pdf[rev_col]):
            try:
                dt_series = pd.to_datetime(pdf[date_col], errors='coerce')
                max_date = dt_series.max()
                if pd.notnull(max_date):
                    rfm = pdf.groupby(cust_col).agg(
                        recency_days=(date_col, lambda x: (max_date - pd.to_datetime(x).max()).days),
                        frequency=(date_col, 'count'),
                        monetary_total=(rev_col, 'sum'),
                        monetary_avg=(rev_col, 'mean')
                    ).reset_index()
                    
                    pdf = pdf.merge(rfm, on=cust_col, how='left')
                    lineages.append(FeatureLineage(
                        feature_name="RFM_Metrics (recency_days, frequency, monetary_total, monetary_avg)",
                        source_columns=[cust_col, date_col, rev_col],
                        transformation="Customer-level RFM Aggregation",
                        reason="Core e-commerce and retention metric for segmenting high-value vs at-risk customers"
                    ))
            except Exception:
                pass

        return pl.from_pandas(pdf), FeatureCatalog(features=lineages)
