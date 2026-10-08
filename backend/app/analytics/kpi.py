import polars as pl
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict, Any

class KPIDefinition(BaseModel):
    name: str
    formula: str
    required_columns: List[str]
    business_meaning: str
    why_relevant: str
    limitations: str
    calculated_value: float
    formatted_value: str

class KPICatalog(BaseModel):
    kpis: List[KPIDefinition]

class DeterministicKPIEngine:
    @staticmethod
    def discover_and_compute(df: pl.DataFrame, business_goal: str) -> KPICatalog:
        pdf = df.to_pandas()
        cols_lower = {c.lower(): c for c in pdf.columns}
        kpis: List[KPIDefinition] = []
        
        # 1. Total Revenue KPI
        rev_col = cols_lower.get("revenue") or cols_lower.get("sales") or cols_lower.get("amount")
        if rev_col and pd.api.types.is_numeric_dtype(pdf[rev_col]):
            tot_rev = float(pdf[rev_col].sum())
            kpis.append(KPIDefinition(
                name="Total Revenue",
                formula=f"SUM({rev_col})",
                required_columns=[rev_col],
                business_meaning="Aggregate top-line monetary revenue generated",
                why_relevant="Primary indicator of business scale and top-line growth",
                limitations="Does not account for cost of goods sold or operating expenses",
                calculated_value=tot_rev,
                formatted_value=f"${tot_rev:,.2f}"
            ))
            
            # Average Order / Transaction Value KPI
            aov = float(pdf[rev_col].mean())
            kpis.append(KPIDefinition(
                name="Average Order Value (AOV)",
                formula=f"MEAN({rev_col})",
                required_columns=[rev_col],
                business_meaning="Average monetary value per transaction/order",
                why_relevant="Indicates customer basket size and purchasing power",
                limitations="Sensitive to extreme high-value outliers",
                calculated_value=aov,
                formatted_value=f"${aov:,.2f}"
            ))

        # 2. Churn Rate KPI
        churn_col = cols_lower.get("churn") or cols_lower.get("is_churn") or cols_lower.get("churned")
        if churn_col:
            churn_val = pdf[churn_col]
            if pd.api.types.is_numeric_dtype(churn_val):
                churn_rate = float(churn_val.mean() * 100)
            else:
                churn_rate = float((churn_val.astype(str).str.lower().isin(["1", "true", "yes"])).mean() * 100)
                
            kpis.append(KPIDefinition(
                name="Churn Rate",
                formula=f"MEAN({churn_col} == 1) * 100",
                required_columns=[churn_col],
                business_meaning="Percentage of customers lost during the period",
                why_relevant="Direct indicator of customer dissatisfaction and revenue risk",
                limitations="Does not capture partial downgrade churn",
                calculated_value=churn_rate,
                formatted_value=f"{churn_rate:.1f}%"
            ))

        # 3. Customer Retention Rate KPI
        if churn_col and len(kpis) > 0 and kpis[-1].name == "Churn Rate":
            retention_rate = 100.0 - kpis[-1].calculated_value
            kpis.append(KPIDefinition(
                name="Customer Retention Rate",
                formula="100 - Churn Rate",
                required_columns=[churn_col],
                business_meaning="Percentage of customers retained over the period",
                why_relevant="Primary health metric for customer lifetime value (LTV)",
                limitations="Inverse of churn rate",
                calculated_value=retention_rate,
                formatted_value=f"{retention_rate:.1f}%"
            ))
            
        # Fallback if no specific named KPIs matched
        if len(kpis) == 0:
            total_records = float(len(pdf))
            kpis.append(KPIDefinition(
                name="Total Volume / Records",
                formula="COUNT(*)",
                required_columns=[list(pdf.columns)[0]],
                business_meaning="Total count of analyzed transactions / records",
                why_relevant="Establishes baseline sample size",
                limitations="Non-monetary metric",
                calculated_value=total_records,
                formatted_value=f"{int(total_records):,}"
            ))
            
        return KPICatalog(kpis=kpis)
