import polars as pl
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Any
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class ClusterSegment(BaseModel):
    segment_id: int
    segment_name: str
    sample_count: int
    percentage_of_total: float
    feature_means: Dict[str, float]
    business_description: str

class SegmentationReport(BaseModel):
    optimal_clusters_k: int
    silhouette_score: float
    segments: List[ClusterSegment]

class SegmentationEngine:
    """
    Segmentation Engine: Conducts customer/product segmentation via K-Means clustering,
    evaluating silhouette score stability and generating business profiles.
    """
    
    @staticmethod
    def segment(df: pl.DataFrame, k: int = 3) -> SegmentationReport:
        pdf = df.to_pandas()
        num_cols = [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]
        
        if len(num_cols) < 2 or len(pdf) < 15:
            return SegmentationReport(
                optimal_clusters_k=1,
                silhouette_score=0.0,
                segments=[]
            )

        X = pdf[num_cols].fillna(pdf[num_cols].median())
        # Scale features
        X_scaled = (X - X.mean()) / (X.std() + 1e-6)
        
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)
        sil = float(silhouette_score(X_scaled, labels)) if len(set(labels)) > 1 else 0.0
        
        segments: List[ClusterSegment] = []
        total_len = len(pdf)
        
        for cluster_idx in range(k):
            cluster_mask = labels == cluster_idx
            cluster_df = X[cluster_mask]
            count = int(len(cluster_df))
            pct = round((count / total_len * 100), 2)
            
            means = {col: round(float(cluster_df[col].mean()), 2) for col in num_cols[:5]}
            
            segments.append(ClusterSegment(
                segment_id=cluster_idx + 1,
                segment_name=f"Segment {cluster_idx + 1}",
                sample_count=count,
                percentage_of_total=pct,
                feature_means=means,
                business_description=f"Cluster {cluster_idx + 1} represents {pct}% of dataset with key characteristics: {means}"
            ))

        return SegmentationReport(
            optimal_clusters_k=k,
            silhouette_score=round(sil, 3),
            segments=segments
        )
