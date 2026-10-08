# Data Lineage & Evidence System

## End-to-End Traceability

AI Data Analyst OS ensures complete traceability from final business recommendations back to raw dataset source columns.

```text
Raw Dataset Column
       ↓ (Ingestion & Schema Ingestion)
Cleaned Column
       ↓ (Feature Transformation)
Engineered Feature
       ↓ (Aggregation / Formula)
Derived KPI
       ↓ (Hypothesis Test / Scikit-Learn Model)
Statistical Result / Segment
       ↓ (Synthesized Claim)
Insight Card
       ↓ (Action Plan Mapping)
Business Recommendation
```

## Artifact Schema

Every artifact generated during analysis contains standard metadata:
- `artifact_id`: Unique artifact identifier
- `version`: Version number (incremented on re-execution)
- `created_at`: UTC timestamp
- `created_by_agent`: Agent identifier
- `inputs`: List of source artifact IDs
- `parameters`: Execution parameters
- `status`: Validation state
- `content`: Typed data payload (JSON / Dataframe pointer / Image path)

## Evidence Citations
Insights are tagged with explicit URI schemas:
- `derived://kpi/churn_rate`
- `derived://stats/t_test_revenue`
- `derived://ml/feature_importance`

Clicking an insight card in the UI displays the underlying evidence artifact details.
