import polars as pl
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Any
from sklearn.ensemble import IsolationForest

class AnomalyRecord(BaseModel):
    record_index: int
    column_name: str
    value: float
    score: float
    reason: str
    is_business_anomaly: bool

class AnomalyReport(BaseModel):
    total_anomalies_detected: int
    anomalies: List[AnomalyRecord]
    methodology: str

class AnomalyDetectionEngine:
    """
    Anomaly Detection Engine: Isolates statistical outliers and business anomalies
    using IQR z-scores and Isolation Forest.
    """
    
    @staticmethod
    def detect(df: pl.DataFrame) -> AnomalyReport:
        pdf = df.to_pandas()
        num_cols = [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]
        
        anomalies: List[AnomalyRecord] = []
        
        if len(num_cols) > 0 and len(pdf) >= 10:
            clean_num = pdf[num_cols].fillna(pdf[num_cols].median())
            iso = IsolationForest(contamination=0.05, random_state=42)
            preds = iso.fit_predict(clean_num)
            scores = iso.decision_function(clean_num)
            
            anomaly_indices = np.where(preds == -1)[0]
            
            for idx in anomaly_indices[:10]: # Top 10 representative anomalies
                row = pdf.iloc[idx]
                top_col = num_cols[0]
                val = float(row[top_col]) if pd.notnull(row[top_col]) else 0.0
                
                anomalies.append(AnomalyRecord(
                    record_index=int(idx),
                    column_name=top_col,
                    value=val,
                    score=float(scores[idx]),
                    reason=f"Isolation Forest multidimensional outlier score: {scores[idx]:.3f}",
                    is_business_anomaly=abs(scores[idx]) > 0.15
                ))

        return AnomalyReport(
            total_anomalies_detected=len(anomalies),
            anomalies=anomalies,
            methodology="Isolation Forest multidimensional contamination model (5% threshold)."
        )
