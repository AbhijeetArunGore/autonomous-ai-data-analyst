# 17 Specialized Agents Specification & Implementation Matrix

The **Autonomous Analytics & Decision Intelligence Platform** orchestrates 17 specialized analytical agents across a dependency-aware execution graph (DAG). Each agent possesses strict input/output contracts, assigned execution engines, and explicit implementation files within the codebase.

---

## Agent Roster & Implementation Index

| # | Agent Name | Category | Primary Engine / Tool | Implementation File | Specification Link |
|---|---|---|---|---|---|
| **01** | **Data Intake Agent** | Discovery | Python `magic`, Polars | [`backend/app/storage/data_source.py`](../backend/app/storage/data_source.py) | [Spec 01](#1-data-intake-agent) |
| **02** | **Data Profiling Agent** | Discovery | Polars, NumPy | [`backend/app/analytics/profiler.py`](../backend/app/analytics/profiler.py) | [Spec 02](#2-data-profiling-agent) |
| **03** | **Researcher Agent** | Discovery | Universal Semantic Mapper | [`backend/app/analytics/semantic_layer.py`](../backend/app/analytics/semantic_layer.py) | [Spec 03](#3-researcher-agent) |
| **04** | **Planner Agent** | Planning | Execution DAG Engine | [`backend/app/services/analysis_runner.py`](../backend/app/services/analysis_runner.py) | [Spec 04](#4-planner-agent) |
| **05** | **Data Quality Agent** | Data Prep | Custom Quality Rules | [`backend/app/analytics/quality.py`](../backend/app/analytics/quality.py) | [Spec 05](#5-data-quality-agent) |
| **06** | **Missing Value Agent** | Data Prep | Polars, Scikit-Learn Imputer | [`backend/app/analytics/imputation.py`](../backend/app/analytics/imputation.py) | [Spec 06](#6-missing-value-agent) |
| **07** | **KPI Discovery Agent** | Data Prep | Metric Registry & DuckDB | [`backend/app/analytics/kpi.py`](../backend/app/analytics/kpi.py) | [Spec 07](#7-kpi-discovery-agent) |
| **08** | **Feature Engineering Agent**| Data Prep | Polars Transformation Engine | [`backend/app/analytics/feature_engineering.py`](../backend/app/analytics/feature_engineering.py) | [Spec 08](#8-feature-engineering-agent) |
| **09** | **Statistical Analysis Agent**| Analytics | SciPy Stats, Statsmodels | [`backend/app/analytics/statistics.py`](../backend/app/analytics/statistics.py) | [Spec 09](#9-statistical-analysis-agent) |
| **10** | **Machine Learning Agent** | Analytics | Scikit-Learn Models | [`backend/app/analytics/ml_engine.py`](../backend/app/analytics/ml_engine.py) | [Spec 10](#10-machine-learning-agent) |
| **11** | **Anomaly Detection Agent** | Analytics | Isolation Forest | [`backend/app/analytics/anomaly.py`](../backend/app/analytics/anomaly.py) | [Spec 11](#11-anomaly-detection-agent) |
| **12** | **Segmentation Agent** | Analytics | K-Means Clustering | [`backend/app/analytics/segmentation.py`](../backend/app/analytics/segmentation.py) | [Spec 12](#12-segmentation-agent) |
| **13** | **Forecasting Agent** | Analytics | Holt-Winters Smoothing | [`backend/app/analytics/forecasting.py`](../backend/app/analytics/forecasting.py) | [Spec 13](#13-forecasting-agent) |
| **14** | **Root Cause Agent (RCA)** | Decision Intel | DecisionTree Variance Decomposition | [`backend/app/analytics/root_cause.py`](../backend/app/analytics/root_cause.py) | [Spec 14](#14-root-cause-analysis-agent-rca) |
| **15** | **What-If Scenario Agent** | Decision Intel | Deterministic Simulator | [`backend/app/analytics/scenario_engine.py`](../backend/app/analytics/scenario_engine.py) | [Spec 15](#15-what-if-scenario-agent) |
| **16** | **Validation Guardrail Agent**| Decision Intel | Claim-Grounding Guardrails | [`backend/app/analytics/visualization.py`](../backend/app/analytics/visualization.py) | [Spec 16](#16-validation--guardrail-agent) |
| **17** | **Executive Storytelling Agent**| Communication| Executive Exporter & Audio TTS | [`backend/app/services/report_exporter.py`](../backend/app/services/report_exporter.py) | [Spec 17](#17-executive-storytelling-agent) |

---

## Detailed Agent Specifications

### 1. Data Intake Agent
- **Implementation**: [`backend/app/storage/data_source.py`](../backend/app/storage/data_source.py)
- **Responsibilities**: Validates CSV, Excel, Parquet, and SQL connections; detects file encoding, delimiters, column header schemas, and empty columns.
- **Artifact Produced**: `DatasetMetadata` (SHA-256 hash, column names, row counts, memory size).

### 2. Data Profiling Agent
- **Implementation**: [`backend/app/analytics/profiler.py`](../backend/app/analytics/profiler.py)
- **Responsibilities**: Computes exact column data types, missingness ratios, cardinality, numerical mean/std/quantile distributions, categorical frequencies, and skewness metrics.
- **Artifact Produced**: `DataProfile` JSON dictionary.

### 3. Researcher Agent
- **Implementation**: [`backend/app/analytics/semantic_layer.py`](../backend/app/analytics/semantic_layer.py)
- **Responsibilities**: Maps raw dataset schemas into standardized enterprise entities (Healthcare, Finance, SaaS, HR, Construction) and identifies domain target candidates.
- **Artifact Produced**: `DomainContext` mapping entity IDs and candidate targets.

### 4. Planner Agent
- **Implementation**: [`backend/app/services/analysis_runner.py`](../backend/app/services/analysis_runner.py)
- **Responsibilities**: Converts the user's natural language business question and domain context into an executable dependency graph (DAG) specifying necessary analytics steps.
- **Artifact Produced**: `AnalysisPlan` execution graph.

### 5. Data Quality Agent
- **Implementation**: [`backend/app/analytics/quality.py`](../backend/app/analytics/quality.py)
- **Responsibilities**: Scans for negative numbers, impossible values, high missingness columns, and constant value flags.
- **Artifact Produced**: `QualityReport` with issue counts and recommendations.

### 6. Missing Value Agent
- **Implementation**: [`backend/app/analytics/imputation.py`](../backend/app/analytics/imputation.py)
- **Responsibilities**: Executes configurable imputation strategies (Median, Mean, Mode, KNN, or Drop) to prepare clean numeric dataframes.
- **Artifact Produced**: Cleaned DataFrame + `ImputationSummary`.

### 7. KPI Discovery Agent
- **Implementation**: [`backend/app/analytics/kpi.py`](../backend/app/analytics/kpi.py) & [`backend/app/analytics/metric_registry.py`](../backend/app/analytics/metric_registry.py)
- **Responsibilities**: Evaluates formula definitions against column names and calculates standard domain business metrics (e.g. Churn Rate, MRR, Operating Expense Ratio).
- **Artifact Produced**: `KPICatalog` with numerical business metrics.

### 8. Feature Engineering Agent
- **Implementation**: [`backend/app/analytics/feature_engineering.py`](../backend/app/analytics/feature_engineering.py)
- **Responsibilities**: Extracts date/time features, log transformations, interaction terms, and customer RFM (Recency, Frequency, Monetary) metrics.
- **Artifact Produced**: Enriched DataFrame + `FeatureCatalog`.

### 9. Statistical Analysis Agent
- **Implementation**: [`backend/app/analytics/statistics.py`](../backend/app/analytics/statistics.py)
- **Responsibilities**: Runs SciPy statistical significance tests (Welch's t-test, ANOVA, Chi-Square) and calculates Cohen's d effect sizes.
- **Artifact Produced**: `StatisticalReport` containing p-values, test stats, and effect sizes.

### 10. Machine Learning Agent
- **Implementation**: [`backend/app/analytics/ml_engine.py`](../backend/app/analytics/ml_engine.py)
- **Responsibilities**: Trains Scikit-Learn Random Forest or Logistic Regression predictive models, evaluates accuracy/AUC, and ranks feature importance.
- **Artifact Produced**: `MLAnalysisResult` dictionary.

### 11. Anomaly Detection Agent
- **Implementation**: [`backend/app/analytics/anomaly.py`](../backend/app/analytics/anomaly.py)
- **Responsibilities**: Fits an Isolation Forest model to flag multi-dimensional statistical outliers and suspicious records.
- **Artifact Produced**: `AnomalyReport` with anomaly scores and flagged record indices.

### 12. Segmentation Agent
- **Implementation**: [`backend/app/analytics/segmentation.py`](../backend/app/analytics/segmentation.py)
- **Responsibilities**: Groups entities into clusters using K-Means and evaluates optimal cluster separation using Silhouette scores.
- **Artifact Produced**: `SegmentationReport` with cluster centroids and profile summaries.

### 13. Forecasting Agent
- **Implementation**: [`backend/app/analytics/forecasting.py`](../backend/app/analytics/forecasting.py)
- **Responsibilities**: Extracts trend and seasonality components using Holt-Winters Exponential Smoothing to project future horizons.
- **Artifact Produced**: `ForecastReport` with historical vs predicted point estimates and confidence bands.

### 14. Root Cause Analysis Agent (RCA)
- **Implementation**: [`backend/app/analytics/root_cause.py`](../backend/app/analytics/root_cause.py)
- **Responsibilities**: Fits Decision Tree Regressors to decompose outcome variance and isolate key root drivers.
- **Artifact Produced**: `RCAReport` with decision paths and variance contribution percentages.

### 15. What-If Scenario Agent
- **Implementation**: [`backend/app/analytics/scenario_engine.py`](../backend/app/analytics/scenario_engine.py)
- **Responsibilities**: Simulates baseline vs scenario parameters to project hypothetical financial and operational outcomes.
- **Artifact Produced**: `ScenarioResult` with delta metrics and projected ROI.

### 16. Validation & Guardrail Agent
- **Implementation**: [`backend/app/analytics/visualization.py`](../backend/app/analytics/visualization.py) & [`backend/app/security/sanitizer.py`](../backend/app/security/sanitizer.py)
- **Responsibilities**: Cross-checks LLM text claims against SciPy/Polars output data, flags unsupported statements, and enforces correlation vs causality language boundaries.
- **Artifact Produced**: `ValidationReport` with grounding status.

### 17. Executive Storytelling Agent
- **Implementation**: [`backend/app/services/report_exporter.py`](../backend/app/services/report_exporter.py)
- **Responsibilities**: Renders executive decision briefs, technical analytical reports, and audio narration scripts.
- **Artifact Produced**: `ExecutiveBrief.md` and structured JSON audit payloads.
