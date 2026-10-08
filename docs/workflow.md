# Analytical Dependency Graph & Workflow Engine

## Directed Acyclic Graph (DAG) Structure

Unlike linear AI agent chains (`Agent 1 -> Agent 2 -> Agent 3`), AI Data Analyst OS executes analysis over a structured **analytical dependency graph**.

```text
               [ Dataset Intake ]
                        │
             [ Dataset Profiling ]
                   /    │    \
      [ Data Quality ]  │   [ External Research ]
             │          │             │
      [ Imputation ]    │       [ Business Goal ]
             │          │             │
      [ Feature Eng ]   └──────┬──────┘
             │                 │
             └─────────► [ Analysis Plan ]
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
           [ KPIs ]     [ Statistics ]    [ ML / Clustering ]
                │              │              │
                └──────────────┼──────────────┘
                               ▼
                       [ Anomaly Detection ]
                               │
                       [ Visualizations ]
                               │
                       [ Validation Engine ]
                               │
                       [ Insight Synthesis ]
                               │
                    [ Consulting Recs ]
                               │
                    [ Storytelling & Audio ]
```

## Node Metadata Schema

Every node in the dependency graph tracks execution status and lineage:
- `node_id`: String (e.g. `node_kpi_discovery`)
- `agent`: Name of responsible agent
- `inputs`: List of input artifact IDs
- `outputs`: List of output artifact IDs
- `parameters`: Configurable hyperparameter dictionary
- `status`: State enum (`PENDING`, `RUNNING`, `VALID`, `INVALIDATED`, `FAILED`, `SKIPPED`)
- `execution_time_ms`: Float
- `token_metrics`: Prompt, completion tokens & estimated cost
- `model_info`: Model identifier used
- `dependencies`: List of parent node IDs
- `validation_status`: Validation result
- `confidence`: Confidence level & explanation

## Human-In-The-Loop Selective Invalidation

When an analyst modifies a parameter (e.g., changing missing value treatment from `Median` to `Mean`):
1. The engine computes the downstream transitive closure of the modified node.
2. Only affected downstream nodes are transitioned to `INVALIDATED`.
3. Unrelated nodes (e.g., Dataset Profiling, External Research) remain `VALID`.
4. The user can inspect affected nodes before triggering a selective re-execution.
