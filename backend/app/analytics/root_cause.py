import polars as pl
import pandas as pd
import numpy as np
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor, export_text

class RootCauseFactor(BaseModel):
    factor_name: str
    contribution_score: float
    segment_condition: str
    impact_description: str

class RootCauseAnalysisReport(BaseModel):
    target_metric: str
    top_root_causes: List[RootCauseFactor]
    tree_rules_summary: str

class RootCauseAnalysisEngine:
    """
    Root Cause Analysis (RCA) Engine: Uses shallow decision tree split rules and variance
    decomposition to isolate exact segment drivers behind KPI changes.
    """
    
    @staticmethod
    def analyze_root_causes(df: pl.DataFrame, target_col: Optional[str] = None) -> RootCauseAnalysisReport:
        pdf = df.to_pandas()
        
        cols_lower = {c.lower(): c for c in pdf.columns}
        if not target_col:
            target_col = cols_lower.get("churn") or cols_lower.get("revenue") or cols_lower.get("sales")
            
        if not target_col or target_col not in pdf.columns:
            num_cols = [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]
            target_col = num_cols[0] if num_cols else None
            
        if not target_col or len(pdf) < 10:
            return RootCauseAnalysisReport(
                target_metric=target_col or "N/A",
                top_root_causes=[],
                tree_rules_summary="Insufficient data for root cause decision tree decomposition."
            )

        clean_df = pdf.dropna(subset=[target_col]).copy()
        y = clean_df[target_col]
        X_raw = clean_df.drop(columns=[target_col])
        X = pd.get_dummies(X_raw, drop_first=True).select_dtypes(include=[np.number]).fillna(0)

        if X.shape[1] == 0:
            return RootCauseAnalysisReport(
                target_metric=target_col,
                top_root_causes=[],
                tree_rules_summary="No valid numeric or encoded features for root cause split analysis."
            )

        is_binary = len(y.unique()) == 2
        if is_binary:
            dt = DecisionTreeClassifier(max_depth=3, random_state=42)
        else:
            dt = DecisionTreeRegressor(max_depth=3, random_state=42)

        dt.fit(X, y)
        rules = export_text(dt, feature_names=list(X.columns))
        
        # Rank features by Gini / MSE variance reduction
        importances = dt.feature_importances_
        sorted_indices = np.argsort(importances)[::-1]
        
        factors: List[RootCauseFactor] = []
        for idx in sorted_indices[:3]:
            if importances[idx] > 0.01:
                col_name = X.columns[idx]
                factors.append(RootCauseFactor(
                    factor_name=col_name,
                    contribution_score=round(float(importances[idx] * 100), 2),
                    segment_condition=f"Subgroup split on {col_name}",
                    impact_description=f"Feature '{col_name}' accounts for {importances[idx]*100:.1f}% of total variance in '{target_col}'."
                ))

        return RootCauseAnalysisReport(
            target_metric=target_col,
            top_root_causes=factors,
            tree_rules_summary=rules[:500]
        )
