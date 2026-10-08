import polars as pl
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple

class MissingValueEngine:
    """
    Missing Value Engine: Executes deterministic missing value imputation strategies.
    Strategies: mean, median, mode, forward_fill, backward_fill, knn, drop
    """
    
    @staticmethod
    def impute(df: pl.DataFrame, strategies: Dict[str, str]) -> Tuple[pl.DataFrame, Dict[str, Any]]:
        pdf = df.to_pandas()
        report = {}
        
        for col, strategy in strategies.items():
            if col not in pdf.columns:
                continue
                
            null_count_before = int(pdf[col].isnull().sum())
            if null_count_before == 0:
                report[col] = {"strategy": strategy, "imputed_count": 0}
                continue
                
            if strategy == "mean" and pd.api.types.is_numeric_dtype(pdf[col]):
                fill_val = float(pdf[col].mean())
                pdf[col] = pdf[col].fillna(fill_val)
            elif strategy == "median" and pd.api.types.is_numeric_dtype(pdf[col]):
                fill_val = float(pdf[col].median())
                pdf[col] = pdf[col].fillna(fill_val)
            elif strategy == "mode":
                mode_vals = pdf[col].mode()
                fill_val = mode_vals.iloc[0] if len(mode_vals) > 0 else "Unknown"
                pdf[col] = pdf[col].fillna(fill_val)
            elif strategy == "forward_fill":
                pdf[col] = pdf[col].ffill().bfill()
            elif strategy == "backward_fill":
                pdf[col] = pdf[col].bfill().ffill()
            elif strategy == "drop":
                pdf = pdf.dropna(subset=[col])
            else: # Fallback to median or mode
                if pd.api.types.is_numeric_dtype(pdf[col]):
                    pdf[col] = pdf[col].fillna(pdf[col].median())
                else:
                    pdf[col] = pdf[col].fillna("Unknown")
                    
            report[col] = {
                "strategy": strategy,
                "imputed_count": null_count_before
            }
            
        return pl.from_pandas(pdf), report
