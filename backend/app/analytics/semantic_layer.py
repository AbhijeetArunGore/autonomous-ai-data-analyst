import polars as pl
import pandas as pd
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SemanticField(BaseModel):
    column_name: str
    inferred_type: str  # numeric, categorical, datetime, boolean, text
    semantic_type: str  # entity_id, monetary_amount, status_flag, timestamp, metric_value, categorical_dimension
    role: str           # entity, target, feature, timestamp, dimension
    confidence: float
    description: str

class SemanticDataSchema(BaseModel):
    fields: List[SemanticField]
    primary_entity_id: Optional[str] = None
    target_candidates: List[str] = []
    timestamp_column: Optional[str] = None

class UniversalSemanticMapper:
    """
    Universal Semantic Mapper: Maps arbitrary domain columns into semantic business roles
    (Healthcare, Finance, SaaS, Retail, Construction, Manufacturing, HR, Logistics).
    """
    
    @staticmethod
    def infer_semantics(df: pl.DataFrame) -> SemanticDataSchema:
        pdf = df.to_pandas()
        fields: List[SemanticField] = []
        primary_entity_id = None
        target_candidates = []
        timestamp_col = None
        
        for col in pdf.columns:
            series = pdf[col]
            col_lower = col.lower()
            dtype_str = str(series.dtype).lower()
            unique_count = series.nunique()
            total_rows = len(pdf)
            
            # Determine data type & semantic role
            if "int" in dtype_str or "float" in dtype_str:
                inferred_type = "numeric"
                if "id" in col_lower or "key" in col_lower or "code" in col_lower or unique_count == total_rows:
                    semantic_type = "entity_id"
                    role = "entity"
                    if not primary_entity_id:
                        primary_entity_id = col
                elif any(k in col_lower for k in ["churn", "target", "label", "readmission", "fraud", "breach", "delay", "attrition"]):
                    semantic_type = "status_flag"
                    role = "target"
                    target_candidates.append(col)
                elif any(k in col_lower for k in ["revenue", "sales", "amount", "cost", "price", "charge", "spend", "mrr", "income", "profit"]):
                    semantic_type = "monetary_amount"
                    role = "feature"
                    if col not in target_candidates and any(t in col_lower for t in ["target", "revenue"]):
                        target_candidates.append(col)
                else:
                    semantic_type = "metric_value"
                    role = "feature"
            elif "date" in dtype_str or "time" in dtype_str or pd.api.types.is_datetime64_any_dtype(series) or "date" in col_lower:
                inferred_type = "datetime"
                semantic_type = "timestamp"
                role = "timestamp"
                if not timestamp_col:
                    timestamp_col = col
            else:
                inferred_type = "categorical"
                if "id" in col_lower or "code" in col_lower or unique_count == total_rows:
                    semantic_type = "entity_id"
                    role = "entity"
                    if not primary_entity_id:
                        primary_entity_id = col
                elif any(k in col_lower for k in ["churn", "target", "label", "readmission", "fraud", "breach", "delay", "attrition"]):
                    semantic_type = "status_flag"
                    role = "target"
                    target_candidates.append(col)
                else:
                    semantic_type = "categorical_dimension"
                    role = "dimension"

            fields.append(SemanticField(
                column_name=col,
                inferred_type=inferred_type,
                semantic_type=semantic_type,
                role=role,
                confidence=0.92,
                description=f"Inferred semantic role '{role}' ({semantic_type}) for column '{col}'"
            ))

        return SemanticDataSchema(
            fields=fields,
            primary_entity_id=primary_entity_id,
            target_candidates=target_candidates,
            timestamp_column=timestamp_col
        )
