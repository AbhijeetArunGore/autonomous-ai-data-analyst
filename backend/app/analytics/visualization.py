from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

class ChartSpec(BaseModel):
    chart_id: str
    title: str
    chart_type: str  # line, bar, scatter, heatmap, boxplot
    x_axis: str
    y_axis: Optional[str] = None
    data_points: List[Dict[str, Any]]
    explanation: str

class VisualizationCatalog(BaseModel):
    charts: List[ChartSpec]

class DeterministicVisualizationEngine:
    """
    Deterministic Visualization Engine: Generates chart specs (line, bar, scatter, heatmap, boxplot)
    directly from dataset tables and statistical findings.
    """
    
    @staticmethod
    def generate_charts(df, kpis: List[Any], stats_report: Any) -> VisualizationCatalog:
        pdf = df.to_pandas()
        charts: List[ChartSpec] = []
        
        cols_lower = {c.lower(): c for c in pdf.columns}
        
        # 1. Category Bar Chart
        cat_cols = [c for c in pdf.columns if not pd.api.types.is_numeric_dtype(pdf[c])]
        num_cols = [c for c in pdf.columns if pd.api.types.is_numeric_dtype(pdf[c])]
        
        if cat_cols and num_cols:
            cat_col = cat_cols[0]
            num_col = num_cols[0]
            grouped = pdf.groupby(cat_col)[num_col].mean().head(8).reset_index()
            data_pts = grouped.to_dict(orient="records")
            data_pts = [{k: (float(v) if isinstance(v, (int, float, np.number)) else str(v)) for k, v in row.items()} for row in data_pts]
            
            charts.append(ChartSpec(
                chart_id="chart_cat_bar",
                title=f"Average {num_col} by {cat_col}",
                chart_type="bar",
                x_axis=cat_col,
                y_axis=num_col,
                data_points=data_pts,
                explanation=f"Bar chart illustrating metric variation of {num_col} across top categories in {cat_col}."
            ))
            
        # 2. Time-series Line Chart if date exists
        date_col = cols_lower.get("date") or cols_lower.get("signup_date") or cols_lower.get("transaction_date")
        if date_col and num_cols:
            num_col = num_cols[0]
            try:
                pdf["_dt"] = pd.to_datetime(pdf[date_col], errors="coerce")
                trend = pdf.dropna(subset=["_dt"]).set_index("_dt").resample("ME")[num_col].sum().reset_index()
                trend["_dt"] = trend["_dt"].dt.strftime("%Y-%m")
                data_pts = trend.to_dict(orient="records")
                data_pts = [{"date": str(row["_dt"]), num_col: float(row[num_col])} for row in data_pts]
                
                charts.append(ChartSpec(
                    chart_id="chart_trend_line",
                    title=f"Monthly Trend of {num_col}",
                    chart_type="line",
                    x_axis="date",
                    y_axis=num_col,
                    data_points=data_pts,
                    explanation=f"Time-series line chart tracking monthly aggregate {num_col}."
                ))
            except Exception:
                pass
                
        return VisualizationCatalog(charts=charts)
