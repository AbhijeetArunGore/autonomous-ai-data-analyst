# Autonomous Analytics & Decision Intelligence Platform 🏢⚡

[![CI Pipeline](https://github.com/AbhijeetArunGore/autonomous-ai-data-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/AbhijeetArunGore/autonomous-ai-data-analyst/actions)
[![Tests Passing](https://img.shields.io/badge/tests-25%20passed-10b981.svg)](./backend/tests)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-3776ab.svg)](./pyproject.toml)
[![Frontend Framework](https://img.shields.io/badge/frontend-Next.js%2016%20App%20Router-black.svg)](./frontend)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

> **Give us a business question. The platform decides what analysis is required, coordinates 17 specialized analytical agents through a dependency-aware workflow, executes deterministic statistical/ML engines, validates evidence, identifies root causes, simulates scenarios, and produces an executive decision brief.**

---

## ⚡ Hero Architecture

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               AUTONOMOUS ANALYTICS & DECISION INTELLIGENCE PLATFORM                    │
│                                                                                        │
│  Business Question  ──►  17 Specialized Analytical Agents  ──►  Evidence  ──► Decision │
└────────────────────────────────────────────────────────────────────────────────────────┘

                                USER BUSINESS QUESTION
                                          │
                                          ▼
                            ┌───────────────────────────┐
                            │   01. Researcher Agent    │
                            │  Understands the problem  │
                            └─────────────┬─────────────┘
                                          ▼
                            ┌───────────────────────────┐
                            │    02. Planner Agent      │
                            │   Creates analysis plan   │
                            └─────────────┬─────────────┘
                                          ▼
        ┌─────────────────────────────────┼─────────────────────────────────┐
        ▼                                 ▼                                 ▼
 ┌─────────────┐                   ┌─────────────┐                   ┌─────────────┐
 │ Data Quality│                   │ KPI Discovery│                   │ Feature Eng │
 │    Agent    │                   │    Agent    │                   │    Agent    │
 └──────┬──────┘                   └──────┬──────┘                   └──────┬──────┘
        │                                 │                                 │
        └─────────────────────────────────┼─────────────────────────────────┘
                                          ▼
                            ┌───────────────────────────┐
                            │    ANALYTICAL ENGINES     │
                            ├───────────────────────────┤
                            │ Statistical Analysis      │
                            │ Machine Learning          │
                            │ Anomaly Detection         │
                            │ Segmentation              │
                            │ Forecasting               │
                            │ Root Cause Analysis (RCA) │
                            │ What-If Simulation        │
                            └─────────────┬─────────────┘
                                          ▼
                            ┌───────────────────────────┐
                            │   Validation Guardrails   │
                            │  Evidence Grounding Agent │
                            └─────────────┬─────────────┘
                                          ▼
                            ┌───────────────────────────┐
                            │   Insight Synthesis       │
                            │ Executive Briefing Agent  │
                            └─────────────┬─────────────┘
                                          ▼
                                  BUSINESS DECISION
```

---

## ⏱️ 30-Second Understanding: What Happens When You Ask a Question?

```text
QUESTION
   │
   ▼
UNDERSTAND (Researcher Agent interprets domain & problem taxonomy)
   │
   ▼
PLAN (Planner Agent constructs dependency-aware execution graph)
   │
   ▼
PROFILE & PREPARE (Intake ➔ Profiling ➔ Quality ➔ Imputation ➔ Feature Eng)
   │
   ▼
ANALYZE (SciPy Stats ➔ Sklearn ML ➔ Isolation Forest Anomalies ➔ K-Means Clusters ➔ Holt-Winters Forecasts)
   │
   ▼
DECISION INTEL (DecisionTree RCA Drivers ➔ Deterministic What-If Simulator)
   │
   ▼
VALIDATE (Guardrails enforce statistical grounding & block false causality)
   │
   ▼
EXECUTIVE DECISION BRIEF (Executive Storytelling Agent + Interactive Next.js Dashboard)
```

---

## 🧠 Why Multi-Agent + Deterministic Engines (Not Just One LLM)?

### Single LLM Approach vs Enterprise Multi-Agent Platform

```text
                    SINGLE LLM APPROACH
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
       LLM Reasoning                 LLM Calculation
            │                               │
       ❌ Unreliable                 ❌ High Hallucination Risk
                                     ❌ Math Errors on Large CSVs

──────────────────────────────────────────────────────────────────────────

              ENTERPRISE MULTI-AGENT ARCHITECTURE
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
  LLM Agents           Deterministic        Validation &
 (Reason & Plan)       Engines              Evidence Graph
       │               (Calculate Math)          │
       │                    │                    │
       └────────────────────┼────────────────────┘
                            ▼
                    TRUSTED DECISION
```

### Core Architectural Principle
> **LLMs reason. Deterministic engines calculate. Evidence proves. Governance records. Humans decide.**

---

## 🗺️ 17 Specialized Analytical Agents Map

```text
1. DISCOVERY & PLANNING
   Data Intake Agent ──► Data Profiling Agent ──► Researcher Agent ──► Planner Agent

2. DATA PREPARATION
   Data Quality Agent ──► Missing Value Agent ──► KPI Discovery Agent ──► Feature Engineering Agent

3. DETERMINISTIC ANALYTICS
   Statistical Analysis Agent ──► Machine Learning Agent ──► Anomaly Detection Agent ──► Segmentation Agent ──► Forecasting Agent

4. DECISION INTELLIGENCE
   Root Cause Analysis Agent (RCA) ──► What-If Scenario Agent ──► Validation & Guardrail Agent

5. SYNTHESIZE & COMMUNICATE
   Insight Synthesis Agent ──► Executive Storytelling Agent
```

---

## 📋 17 Specialized Agents & Tools Matrix

**17 specialized analytical agents coordinated through a dependency-aware workflow, with deterministic statistical, ML, forecasting, anomaly, RCA and scenario engines used as trusted computational tools:**

| # | Agent Name | Category | Primary Responsibility | Execution Tool / Engine | Artifact Produced |
|---|---|---|---|---|---|
| **01** | **Data Intake Agent** | Discovery | File validation, delimiter/encoding detection, schema extraction | Python `magic`, Polars | `DatasetMetadata` |
| **02** | **Data Profiling Agent** | Discovery | Exact missingness, cardinality, distributions, skewness | Polars, NumPy | `DataProfile` |
| **03** | **Researcher Agent** | Discovery | Researches domain problem, methodology, statistical pitfalls | LLM (Mock/OpenAI) | `ResearchReport` |
| **04** | **Planner Agent** | Planning | Converts goal & research into executable DAG analysis plan | Structured LLM | `AnalysisPlan` |
| **05** | **Data Quality Agent** | Data Prep | Detects quality issues, impossible values, extreme outliers | Rule Engine | `QualityReport` |
| **06** | **Missing Value Agent** | Data Prep | Imputes cells via median, mean, mode, KNN, or drop | Polars, Scikit-learn | Clean DataFrame |
| **07** | **KPI Discovery Agent** | Data Prep | Identifies & computes business metrics with exact formulas | Polars, DuckDB | `KPICatalog` |
| **08** | **Feature Engineering Agent**| Data Prep | Derives datetime features, log transforms, RFM metrics | Polars, NumPy | `FeatureCatalog` |
| **09** | **Statistical Analysis Agent**| Analytics | Welch's t-tests, ANOVA, Chi-Square, Cohen's d effect size | SciPy, Statsmodels | `StatisticalReport` |
| **10** | **Machine Learning Agent** | Analytics | Random Forest, Logistic Regression, Feature Importance | Scikit-learn | `MLAnalysisResult` |
| **11** | **Anomaly Detection Agent** | Analytics | Multi-dimensional outlier isolation & scoring | Isolation Forest | `AnomalyReport` |
| **12** | **Segmentation Agent** | Analytics | Discovers customer/unit clusters & evaluates Silhouette | K-Means Clustering | `SegmentationReport`|
| **13** | **Forecasting Agent** | Analytics | Identifies trend/seasonality & projects multi-period | Holt-Winters Smoothing| `ForecastReport` |
| **14** | **Root Cause Agent (RCA)** | Decision Intel | Decision tree variance decomposition to isolate key drivers | DecisionTreeRegressor | `RCAReport` |
| **15** | **What-If Scenario Agent** | Decision Intel | Simulates KPI changes under hypothetical parameter shifts | Deterministic Simulator| `ScenarioResult` |
| **16** | **Validation Guardrail Agent**| Decision Intel | Claim-evidence grounding checks & causality verification | Guardrail Validator | `ValidationReport` |
| **17** | **Executive Storytelling Agent**| Communication| Executive decision brief, technical report, audio script | LLM + Speech Synthesis| `DualStoryReport` |

---

## 🔍 Example Business Question & Full Execution Trace

### User Question:
> *"Analyze why customer revenue dropped in Q3 and recommend actions to improve retention."*

### Autonomous 17-Step Execution Trace:

```text
[01. INTAKE]         ➔ Loaded 'saas_churn_q3.csv' (15,000 rows, 12 columns). File validation clean.
[02. PROFILING]      ➔ Column 'income' has 4.2% missingness. Target 'churn' distribution: 13.7%. Positive revenue skew.
[03. RESEARCH]       ➔ Identified standard SaaS retention metrics: Recency, Frequency, Tenure, MRR, Onboarding Completion.
[04. PLANNER]        ➔ Generated 8-node execution DAG: Impute -> Feature Eng -> Welch t-test -> Random Forest -> RCA.
[05. QUALITY]        ➔ Detected 3 negative revenue values. Flagged & removed via validation rules.
[06. IMPUTATION]     ➔ Applied Median Imputation for 'income' column. 0 missing values remain.
[07. KPI DISCOVERY]  ➔ Computed Monthly Recurring Revenue (MRR), Churn Rate (13.7%), Average Revenue Per User (ARPU).
[08. FEATURE ENG]    ➔ Derived 'tenure_months', 'log_revenue', and 'support_tickets_per_month'.
[09. STATISTICS]     ➔ Welch t-test on tenure between churned vs retained: t = -4.12, p = 0.0002, Cohen's d = 0.74 (Large effect).
[10. ML ENGINE]      ➔ Trained Random Forest Classifier. Accuracy: 86.4%, ROC-AUC: 0.89. Top feature: 'onboarding_days'.
[11. ANOMALY]        ➔ Isolation Forest flagged 14 anomalous accounts with high support tickets & dropping usage.
[12. SEGMENTATION]   ➔ K-Means (K=3) identified High-Risk Segment: Accounts in 0-90 day onboarding window.
[13. FORECASTING]    ➔ Holt-Winters forecasted Q4 MRR loss of $142,000 if onboarding drop-off rate persists.
[14. RCA]            ➔ Decision Tree RCA isolated primary driver: 90-day onboarding completion accounts for 64.2% of churn variance.
[15. SCENARIO]       ➔ Simulated Scenario: A 10% increase in onboarding completion yields +$86,400 Q4 MRR recovery.
[16. VALIDATION]     ➔ Guardrail Agent verified statistical claims (p < 0.05). Enforced correlation vs causality language.
[17. BRIEFING]       ➔ Rendered Executive Decision Brief + Audio narration script + Interactive Next.js dashboard.
```

---

## 🔬 Deterministic Analytics & Decision Capabilities

```text
                     ANALYTICAL CAPABILITIES SUITE
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
Statistical Engine             Machine Learning            Decision Engine
├── Welch's t-test             ├── Random Forest Classifier ├── Decision Tree RCA
├── ANOVA (F-test)             ├── Logistic Regression      ├── What-If Simulator
├── Chi-Square Test            ├── Isolation Forest Anomaly ├── Holt-Winters Forecast
└── Cohen's d Effect Size      └── K-Means Clustering       └── Metric Guardrails
```

1. **Statistical Significance Testing (`backend/app/analytics/statistics.py`)**: Computes exact p-values, test statistics, and Cohen's d effect sizes using SciPy.
2. **Machine Learning & Feature Importance (`backend/app/analytics/ml_engine.py`)**: Trains Scikit-Learn models to determine key predictive features of target outcomes.
3. **Anomaly Isolation (`backend/app/analytics/anomaly.py`)**: Detects multi-dimensional statistical outliers using Isolation Forest.
4. **Cohort & Behavioral Segmentation (`backend/app/analytics/segmentation.py`)**: Discovers meaningful clusters via K-Means with Silhouette score validation.
5. **Time-Series Forecasting (`backend/app/analytics/forecasting.py`)**: Projects future trend horizons using Holt-Winters Exponential Smoothing.
6. **Root Cause Driver Analysis (`backend/app/analytics/root_cause.py`)**: Decomposes outcome variance using Decision Trees to pinpoint root drivers.
7. **What-If Scenario Simulation (`backend/app/analytics/scenario_engine.py`)**: Simulates financial and operational impacts of parameter adjustments.

---

## 🛡️ Evidence & Validation Architecture

To prevent LLM hallucinations and exaggerated claims, the **Validation Guardrail Agent** (`backend/app/analytics/visualization.py`) checks all generated statements against deterministic calculation outputs:

```text
CLAIM GENERATED ──► EVIDENCE CHECK ──► STATISTICAL SIGNIFICANCE? ──► CAUSALITY CHECK ──► APPROVED STATEMENT
```

- **Enforced Causality Boundaries**:
  - ❌ *Disallowed Claim*: `"Discounting caused sales to increase."`
  - ✅ *Validated Enforced Claim*: `"Higher discount levels were associated with higher observed sales (p = 0.002, d = 0.74); causal attribution was not established."`

---

## 🔄 Human-In-The-Loop (HITL) & Selective Invalidation

When an analyst modifies an upstream parameter (e.g. changing missing value imputation from `Median` to `Mean`), the platform uses transitive closure DAG invalidation to recompute **only affected downstream nodes**:

```text
Analyst Update (Imputation: Median ➔ Mean)
        │
        ├─► 01. Data Intake     (VALID — Preserved)
        ├─► 02. Data Profiling  (VALID — Preserved)
        ├─► 03. Researcher      (VALID — Preserved)
        ├─► 04. Planner         (VALID — Preserved)
        │
        ├─► 06. Imputation      (INVALIDATED ➔ Re-executed)
        ├─► 08. Feature Eng     (INVALIDATED ➔ Re-executed)
        ├─► 09. Statistics      (INVALIDATED ➔ Re-executed)
        ├─► 10. ML Engine       (INVALIDATED ➔ Re-executed)
        ├─► 14. Root Cause      (INVALIDATED ➔ Re-executed)
        └─► 17. Briefing        (INVALIDATED ➔ Re-executed)
```

---

## 🌐 Universal Domain Abstraction

The platform uses a **Universal Semantic Layer** (`backend/app/analytics/semantic_layer.py`) and **Business Metric Registry** (`backend/app/analytics/metric_registry.py`) to analyze arbitrary enterprise domain datasets without hard-coded industry logic:

| Enterprise Domain | Primary Entity | Target Candidate | Standard Business KPI / Metric |
|---|---|---|---|
| **Healthcare** | `patient_id` | `readmitted_30d` | 30-Day Readmission Rate, Length of Stay Variance |
| **Finance** | `unit_id` | `expenses` / `revenue` | Net Profit Margin, Operating Expense Ratio |
| **SaaS** | `customer_id` | `churn` / `mrr` | Monthly Churn Rate, LTV/CAC Ratio, Net Retention |
| **Construction** | `project_id` | `delay_days` | Schedule Adherence, Budget Overrun Percentage |
| **Logistics** | `shipment_id` | `delivered_on_time` | On-Time Delivery Rate (OTD), Cycle Time Hours |
| **HR** | `employee_id` | `left_company` | Employee Attrition Rate, Satisfaction Score |
| **Manufacturing** | `production_id` | `defect_count` | Defect Rate, Machine Overall Equipment Effectiveness |
| **Banking** | `account_id` | `is_fraud` | Transaction Anomaly Rate, False Positive Ratio |

---

## 🏗️ Technology Architecture

```text
                                 CLIENT LAYER
                       Next.js 16 App Router (React 19)
                                      │
                                  REST API
                                      │
                                 FastAPI SERVER
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
Multi-Agent Orchestrator     Deterministic Analytics        Governance & Security
(DAG Execution Engine)       (Polars, SciPy, Sklearn)       (SHA-256 Hashing, Audit Log)
```

---

## ⚖️ Engineering Trade-Offs & Decisions

| Decision Area | Chosen Technology | Alternative Considered | Engineering Rationale |
|---|---|---|---|
| **Data Engine** | **Polars + Arrow** | Pandas | 10x-50x faster columnar processing, zero-copy memory, lazy evaluation. |
| **Calculations**| **SciPy / Sklearn**| Pure LLM Prompts | Prevents calculation hallucinations; guarantees exact statistical p-values. |
| **API Framework**| **FastAPI** | Flask / Django | Asynchronous ASGI, automatic Pydantic schema validation, high throughput. |
| **Frontend** | **Next.js 16 (App Router)** | Streamlit | Production enterprise UI capabilities, server components, customizable CSS. |
| **Governance** | **SHA-256 Registry** | Unversioned Memory | Immutable data lineage, audit trace reproducibility for enterprise compliance. |

*See full [Technology Decision Matrix](./docs/technology-decisions.md) for complete evaluations.*

---

## 🛡️ Security & Governance

- **Prompt Injection Defense (`backend/app/security/sanitizer.py`)**: Sanitizes all natural language business questions and wraps inputs inside strict XML boundaries (`<user_question>...</user_question>`).
- **SHA-256 Dataset Hashing (`backend/app/governance/registry.py`)**: Hashing data on intake guarantees complete versioning and audit trace reproducibility.
- **Structured JSON Observability (`backend/app/observability/logger.py`)**: Logs span IDs, duration, and execution metadata for every agent task.

---

## 📊 Benchmark Evaluation Suite Results

Automated benchmark evaluation script (`evaluations/benchmark_runner.py`) running across multi-domain enterprise datasets:

```bash
python evaluations/benchmark_runner.py
```

```text
================================================================================
BENCHMARK SUITE RESULTS
================================================================================
Total Benchmarks Run:        10 / 10 Domains
Overall Pass Rate:           100.0%
Numerical Correctness:       100.0% (Matched exact Polars/SciPy outputs)
Evidence Grounding Rate:     100.0%
Average Execution Latency:   2.48 seconds per DAG run
Estimated Token Cost:        < $0.001 per run
================================================================================
```

---

## 🖥️ UI Dashboard Preview

The frontend is built with **Next.js 16 (App Router)** and **React 19**, featuring a modern dark-mode executive interface:

- **Interactive Execution DAG**: Visualizes agent progress and execution status in real-time.
- **Dataset Insights & Profiling**: Key metrics, missing value distributions, and data quality flags.
- **What-If Interactive Simulator**: Slider-based scenario projection controls for executives.
- **Executive Decision Brief**: One-page executive summary with key recommendations and risk callouts.

---

## 📂 Repository Architecture

```text
autonomous-ai-data-analyst/
├── backend/
│   ├── app/
│   │   ├── analytics/        # 17 Analytical Agents & Computational Engines
│   │   │   ├── anomaly.py            # Isolation Forest Anomaly Detection
│   │   │   ├── feature_engineering.py# Datetime & RFM Feature Engineering
│   │   │   ├── forecasting.py        # Holt-Winters Exponential Smoothing
│   │   │   ├── imputation.py         # Data Imputation Strategies
│   │   │   ├── kpi.py                # Business Metric & KPI Discovery
│   │   │   ├── metric_registry.py    # Cross-Domain Business Metric Registry
│   │   │   ├── ml_engine.py          # Scikit-Learn Predictive Classifier
│   │   │   ├── profiler.py           # Statistical Data Profiling
│   │   │   ├── quality.py            # Data Quality Rule Checks
│   │   │   ├── root_cause.py         # DecisionTree Variance Decomposition RCA
│   │   │   ├── scenario_engine.py    # Deterministic What-If Simulator
│   │   │   ├── segmentation.py        # K-Means Cluster Analysis
│   │   │   ├── semantic_layer.py     # Universal Domain Semantic Layer
│   │   │   ├── statistics.py         # SciPy Statistical Significance Tests
│   │   │   └── visualization.py      # Chart Engine & Grounding Guardrails
│   │   ├── api/              # FastAPI Router & Endpoint Handlers
│   │   ├── governance/       # SHA-256 Dataset Hashing & Decision Audit Trail
│   │   ├── observability/    # Structured JSON Trace Logger
│   │   ├── security/         # XML Boundary & Sanitization Guardrails
│   │   ├── services/         # DAG Runner & Selective Invalidation Service
│   │   └── storage/          # Universal Data Source Abstraction
│   └── tests/                # 25/25 Passing PyTest Integration Test Suite
├── frontend/                 # Next.js 16 App Router React 19 App
│   ├── app/                  # App Router Pages & Dashboard Layout
│   ├── styles.css            # Custom CSS Styling Tokens
│   └── Dockerfile            # Production Multi-Stage Frontend Build
├── docs/                     # Technical Architecture & Strategy Specifications
├── evaluations/              # Multi-Domain Enterprise Benchmark Runner
├── docker-compose.yml        # Production Multi-Container Orchestration
└── pyproject.toml            # Backend Dependencies & Project Configuration
```

---

## 🚀 Quick Start Guide

### 1. Run Backend API Server
```bash
git clone https://github.com/AbhijeetArunGore/autonomous-ai-data-analyst.git
cd autonomous-ai-data-analyst

# Install Python backend dependencies
pip install -e .[dev]

# Start FastAPI API server
uvicorn backend.app.main:app --reload --port 8000
```

### 2. Run Next.js Dashboard
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000 in browser
```

### 3. Run PyTest Verification Suite
```bash
pytest backend/tests/ -v
```

---

## 🐳 Production Docker Deployment

```bash
docker-compose up --build
```

- **FastAPI Backend**: `http://localhost:8000`
- **Next.js Dashboard**: `http://localhost:3000`

---

## 📁 Repository Documentation

- [`docs/final_enterprise_gap_analysis.md`](./docs/final_enterprise_gap_analysis.md) — 24-point audit & gap analysis.
- [`docs/architecture.md`](./docs/architecture.md) — Detailed system architecture & DAG specs.
- [`docs/technology-decisions.md`](./docs/technology-decisions.md) — Technology evaluation matrix.
- [`docs/governance.md`](./docs/governance.md) — Dataset SHA-256 hashing & decision lineage.
- [`docs/agents.md`](./docs/agents.md) — Agent specifications & contracts.
- [`docs/workflow.md`](./docs/workflow.md) — Dependency graph & selective invalidation.
- [`docs/security.md`](./docs/security.md) — Prompt injection & file security defenses.

---

## ⚠️ Architectural Boundaries & Limitations

- **Dataset Scale**: Designed for single-node in-memory processing up to ~5GB per dataset via Polars/Arrow. Distributed Spark/Ray cluster execution is planned for future releases.
- **LLM Provider**: Operates out-of-the-box with fallback mock heuristic reasoning engines for local test environments without requiring an external OpenAI API key.

---

## 🗺️ Future Roadmap

- [ ] Persistent PostgreSQL ORM storage for multi-tenant analysis histories.
- [ ] Distributed Celery / Redis background worker queue for long-running batch jobs.
- [ ] Slack and Microsoft Teams integration for automated executive decision alert distribution.

---

## 📜 License
MIT License. See [LICENSE](./LICENSE) for details.
