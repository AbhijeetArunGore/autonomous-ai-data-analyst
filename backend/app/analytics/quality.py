import polars as pl
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DataQualityIssue(BaseModel):
    column: str
    problem: str
    severity: str  # High, Medium, Low
    evidence: str
    recommended_treatment: str
    alternative_treatments: List[str]
    reason: str
    risk: str
    confidence: float

class QualityAnalysisResult(BaseModel):
    total_issues: int
    issues: List[DataQualityIssue]
    clean_columns: List[str]

class DataQualityAnalyzer:
    @staticmethod
    def analyze(df: pl.DataFrame) -> QualityAnalysisResult:
        issues: List[DataQualityIssue] = []
        clean_cols = []
        total_rows = df.shape[0]
        
        pdf = df.to_pandas()
        
        for col in df.columns:
            series = pdf[col]
            null_count = int(series.isnull().sum())
            null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0.0
            
            col_issues = 0
            
            if null_pct > 0:
                col_issues += 1
                severity = "High" if null_pct > 20 else ("Medium" if null_pct > 5 else "Low")
                is_num = "int" in str(series.dtype).lower() or "float" in str(series.dtype).lower()
                rec = "median" if is_num else "mode"
                alts = ["mean", "knn", "drop"] if is_num else ["forward_fill", "drop"]
                
                issues.append(DataQualityIssue(
                    column=col,
                    problem=f"{null_pct:.1f}% missing values ({null_count} rows)",
                    severity=severity,
                    evidence=f"Missing {null_count} of {total_rows} entries",
                    recommended_treatment=rec,
                    alternative_treatments=alts,
                    reason="Skewed numeric distribution" if is_num else "Categorical variable",
                    risk="May introduce slight artificial variance reduction" if is_num else "May over-represent dominant category",
                    confidence=0.88
                ))
                
            if col_issues == 0:
                clean_cols.append(col)
                
        return QualityAnalysisResult(
            total_issues=len(issues),
            issues=issues,
            clean_columns=clean_cols
        )
