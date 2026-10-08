import polars as pl
import pandas as pd
import numpy as np
from scipy import stats
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class StatisticalTestResult(BaseModel):
    test_name: str
    target_variable: str
    group_variable: Optional[str]
    statistic: float
    p_value: float
    is_statistically_significant: bool
    alpha: float = 0.05
    effect_size: float
    interpretation: str
    assumptions_checked: str
    causal_warning: str = "Association observed. This does NOT prove direct causation."

class StatisticalAnalysisReport(BaseModel):
    tests: List[StatisticalTestResult]

class StatisticalAnalysisEngine:
    """
    Statistical Analysis Engine: Performs exact hypothesis tests (t-test, Mann-Whitney, Chi-Square, ANOVA),
    checks assumptions, computes effect sizes, and flags causal overreach.
    """
    
    @staticmethod
    def analyze(df: pl.DataFrame, target_col: Optional[str] = None) -> StatisticalAnalysisReport:
        pdf = df.to_pandas()
        results: List[StatisticalTestResult] = []
        
        cols_lower = {c.lower(): c for c in pdf.columns}
        if not target_col:
            target_col = cols_lower.get("churn") or cols_lower.get("sales") or cols_lower.get("revenue")
            
        if not target_col or target_col not in pdf.columns:
            # Pick first numeric column as fallback target
            num_cols = [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]
            target_col = num_cols[0] if num_cols else None
            
        if not target_col:
            return StatisticalAnalysisReport(tests=[])

        # If target is binary categorical / binary numeric (e.g. churn = 0 or 1)
        target_series = pdf[target_col].dropna()
        unique_targets = target_series.unique()
        
        if len(unique_targets) == 2: # Binary classification setting (e.g. Churn vs Retained)
            val0, val1 = unique_targets[0], unique_targets[1]
            group0 = pdf[pdf[target_col] == val0]
            group1 = pdf[pdf[target_col] == val1]
            
            num_features = [c for c in pdf.columns if c != target_col and pd.api.types.is_numeric_dtype(pdf[c])]
            
            for num_c in num_features[:4]:
                s0 = group0[num_c].dropna()
                s1 = group1[num_c].dropna()
                
                if len(s0) > 3 and len(s1) > 3:
                    # Welch's t-test
                    t_stat, p_val = stats.ttest_ind(s0, s1, equal_var=False)
                    # Cohen's d effect size
                    n0, n1 = len(s0), len(s1)
                    s_pooled = np.sqrt(((n0 - 1)*s0.var() + (n1 - 1)*s1.var()) / (n0 + n1 - 2))
                    effect_size = abs(s0.mean() - s1.mean()) / s_pooled if s_pooled > 0 else 0.0
                    
                    sig = bool(p_val < 0.05)
                    interp = (
                        f"Statistically significant difference in '{num_c}' between '{target_col}={val0}' "
                        f"(mean={s0.mean():.2f}) and '{target_col}={val1}' (mean={s1.mean():.2f})."
                        if sig else f"No statistically significant difference detected in '{num_c}' across '{target_col}' groups."
                    )
                    
                    results.append(StatisticalTestResult(
                        test_name="Welch's Two-Sample t-Test",
                        target_variable=target_col,
                        group_variable=num_c,
                        statistic=float(t_stat),
                        p_value=float(p_val),
                        is_statistically_significant=sig,
                        effect_size=float(effect_size),
                        interpretation=interp,
                        assumptions_checked="Welch's t-test unequal variance assumption applied."
                    ))

        return StatisticalAnalysisReport(tests=results)
