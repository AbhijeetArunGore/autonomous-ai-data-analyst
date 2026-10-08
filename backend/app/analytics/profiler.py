import polars as pl
import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any, List
from backend.app.schemas.profiling import DataProfile, ColumnProfile, NumericStats, CategoricalStats, DateStats

class DeterministicProfiler:
    """
    Deterministic Profiler Engine: Computes exact statistical distributions, missing values,
    cardinality, correlations, anomalies, and suspicious patterns using Polars and NumPy/SciPy.
    """
    
    @staticmethod
    def profile_dataframe(df: pl.DataFrame, dataset_id: str) -> DataProfile:
        total_rows, total_cols = df.shape
        
        # Calculate duplicate rows count
        duplicate_rows_count = total_rows - df.unique().shape[0] if total_rows > 0 else 0
        duplicate_rows_pct = (duplicate_rows_count / total_rows * 100) if total_rows > 0 else 0.0
        
        column_profiles: Dict[str, ColumnProfile] = {}
        suspicious_cols = []
        potential_leakage_cols = []
        numeric_col_names = []
        
        pdf = df.to_pandas()
        
        for col in df.columns:
            series = df[col]
            null_count = series.null_count()
            missing_pct = (null_count / total_rows * 100) if total_rows > 0 else 0.0
            unique_count = series.n_unique()
            cardinality_ratio = (unique_count / total_rows) if total_rows > 0 else 0.0
            
            is_constant = unique_count <= 1
            # Near constant if top category accounts for >98% of non-null values
            val_counts = pdf[col].value_counts(normalize=True)
            top_val_pct = val_counts.iloc[0] if len(val_counts) > 0 else 0.0
            is_near_constant = top_val_pct > 0.98 and unique_count > 1
            
            is_possible_id = (unique_count == total_rows) and ("id" in col.lower() or "key" in col.lower() or "code" in col.lower())
            is_possible_target = ("target" in col.lower() or "churn" in col.lower() or "label" in col.lower() or "fraud" in col.lower() or "converted" in col.lower())
            
            # Detect leakage candidate if perfectly correlated or named leakage
            if "leak" in col.lower() or (is_possible_target and cardinality_ratio > 0.95):
                potential_leakage_cols.append(col)
                
            if is_constant or is_near_constant:
                suspicious_cols.append(col)
                
            dtype_str = str(series.dtype)
            
            numeric_s = None
            categorical_s = None
            date_s = None
            
            if "Int" in dtype_str or "Float" in dtype_str:
                numeric_col_names.append(col)
                data_type = "numeric"
                clean_arr = pdf[col].dropna().values
                if len(clean_arr) > 0:
                    q25, median, q75 = np.percentile(clean_arr, [25, 50, 75])
                    iqr = q75 - q25
                    lower_bound = q25 - 1.5 * iqr
                    upper_bound = q75 + 1.5 * iqr
                    outlier_count = int(np.sum((clean_arr < lower_bound) | (clean_arr > upper_bound)))
                    skew = float(stats.skew(clean_arr)) if len(clean_arr) > 2 else 0.0
                    
                    numeric_s = NumericStats(
                        mean=float(np.mean(clean_arr)),
                        std=float(np.std(clean_arr)),
                        min=float(np.min(clean_arr)),
                        q25=float(q25),
                        median=float(median),
                        q75=float(q75),
                        max=float(np.max(clean_arr)),
                        skewness=skew,
                        outlier_count_iqr=outlier_count
                    )
            elif "Date" in dtype_str or "Time" in dtype_str or pd.api.types.is_datetime64_any_dtype(pdf[col]):
                data_type = "datetime"
                dt_clean = pdf[col].dropna()
                if len(dt_clean) > 0:
                    min_d = str(dt_clean.min())
                    max_d = str(dt_clean.max())
                    date_s = DateStats(
                        min_date=min_d,
                        max_date=max_d,
                        date_range_days=float((dt_clean.max() - dt_clean.min()).days) if hasattr((dt_clean.max() - dt_clean.min()), 'days') else None
                    )
            else:
                data_type = "categorical"
                top_cats = pdf[col].value_counts().head(10).to_dict()
                top_cats = {str(k): int(v) for k, v in top_cats.items()}
                categorical_s = CategoricalStats(
                    top_categories=top_cats,
                    cardinality=unique_count,
                    is_high_cardinality=cardinality_ratio > 0.5 and unique_count > 50
                )
                
            column_profiles[col] = ColumnProfile(
                column_name=col,
                data_type=data_type,
                count=total_rows,
                missing_count=null_count,
                missing_percentage=round(missing_pct, 2),
                unique_count=unique_count,
                cardinality_ratio=round(cardinality_ratio, 4),
                is_constant=is_constant,
                is_near_constant=is_near_constant,
                is_possible_identifier=is_possible_id,
                is_possible_target=is_possible_target,
                numeric_stats=numeric_s,
                categorical_stats=categorical_s,
                date_stats=date_s
            )
            
        # Calculate correlation matrix for numeric columns
        corr_matrix: Dict[str, Dict[str, float]] = {}
        if len(numeric_col_names) > 1:
            num_df = pdf[numeric_col_names].dropna()
            if len(num_df) > 2:
                corr_df = num_df.corr().round(4)
                corr_matrix = corr_df.to_dict()
                
        return DataProfile(
            dataset_id=dataset_id,
            total_rows=total_rows,
            total_columns=total_cols,
            duplicate_rows_count=duplicate_rows_count,
            duplicate_rows_percentage=round(duplicate_rows_pct, 2),
            columns=column_profiles,
            correlation_matrix=corr_matrix,
            suspicious_columns=suspicious_cols,
            potential_leakage_columns=potential_leakage_cols
        )
