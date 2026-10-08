# Agent Specifications & Responsibilities

AI Data Analyst OS orchestrates 17 specialized agents across the analytical graph lifecycle.

## Agent Roster

### 1. Data Intake Agent
- **Responsibilities**: Validates CSV/Excel files, detects delimiters, encodings, column schemas, empty/duplicate columns, and generates unique dataset IDs.
- **Type**: Deterministic / Technical.

### 2. Data Profiling Agent
- **Responsibilities**: Computes row/column metrics, data types, cardinality, missingness percentages, numerical/categorical distributions, date ranges, correlation matrix, and suspicious columns.
- **Type**: Deterministic computation (Polars / DuckDB).

### 3. Researcher Agent
- **Responsibilities**: Researches domain context, standard KPIs, statistical pitfalls, class imbalance handling, and segmentation methodology based on business goal & profile.
- **Type**: GenAI / LLM Agent.

### 4. Planner Agent
- **Responsibilities**: Translates goal & research into an analytical plan specifying required tests, KPI formulas, ML tasks, and validation rules.
- **Type**: GenAI / Structured LLM Agent.

### 5. Data Quality Agent
- **Responsibilities**: Identifies data quality issues (missing values, outliers, invalid dates, leakage) and provides evidence-backed recommendations and alternative treatments.
- **Type**: Hybrid (Rule-based + GenAI reasoning).

### 6. Missing Value Agent
- **Responsibilities**: Chooses missing value imputation strategy (mean, median, mode, forward fill, KNN, drop) based on distribution and MCAR/MAR/MNAR properties.
- **Type**: Deterministic + Configurable parameter engine.

### 7. KPI Discovery Agent
- **Responsibilities**: Identifies baseline and derived KPIs with exact mathematical formulas, source columns, and business relevance.
- **Type**: Hybrid Engine.

### 8. Feature Engineering Agent
- **Responsibilities**: Derives date features, recency/frequency/monetary metrics, scaling, log transforms, and category encodings with full lineage tracking.
- **Type**: Deterministic transformation + AI discovery.

### 9. Statistical Analysis Agent
- **Responsibilities**: Selects and runs statistical tests (t-test, Mann-Whitney, Chi-Square, ANOVA, Regression), checks assumptions, and explains results without causal overreach.
- **Type**: Hybrid (SciPy/Statsmodels + LLM explanation).

### 10. Machine Learning Agent
- **Responsibilities**: Trains baseline and advanced models (Logistic Regression, Random Forest, XGBoost) for classification/regression with CV metrics and feature importance.
- **Type**: Scikit-Learn Engine + LLM interpretation.

### 11. Anomaly Detection Agent
- **Responsibilities**: Isolates statistical outliers and business anomalies using IQR, Z-Score, and Isolation Forest.
- **Type**: Scikit-Learn / SciPy Engine.

### 12. Segmentation Agent
- **Responsibilities**: Conducts customer/product segmentation via RFM analysis, K-Means, or Hierarchical Clustering with Silhouette score evaluation.
- **Type**: Scikit-Learn Engine.

### 13. Visualization Agent
- **Responsibilities**: Recommends optimal chart types (line, bar, scatter, heatmap, boxplot) mapped directly to analytical questions.
- **Type**: Deterministic JSON Spec generator.

### 14. Validation Agent
- **Responsibilities**: Enforces claim-grounding verification, null-handling validation, metric formula checks, and flags unsupported claims.
- **Type**: Guardrail Engine.

### 15. Insight Agent
- **Responsibilities**: Synthesizes findings across statistical & ML outputs into evidence-backed, structured insight cards.
- **Type**: GenAI Agent.

### 16. Consulting / Recommendation Agent
- **Responsibilities**: Converts insights into actionable, prioritized business recommendations using an Impact/Effort matrix.
- **Type**: GenAI Consulting Agent.

### 17. Storytelling Agent
- **Responsibilities**: Produces dual reports (Executive Summary for leadership and Technical Report for analysts) and generates audio narration scripts.
- **Type**: GenAI Storyteller.
