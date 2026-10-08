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

**Every agent links directly to its code implementation and documentation spec:**

| # | Agent Name | Category | Primary Responsibility | Code Implementation | Documentation |
|---|---|---|---|---|---|
| **01** | **Data Intake Agent** | Discovery | Schema extraction & file encoding validation | [`backend/app/storage/data_source.py`](./backend/app/storage/data_source.py) | [Spec 01](./docs/agents.md#1-data-intake-agent) |
| **02** | **Data Profiling Agent** | Discovery | Exact missingness, distributions, skewness | [`backend/app/analytics/profiler.py`](./backend/app/analytics/profiler.py) | [Spec 02](./docs/agents.md#2-data-profiling-agent) |
| **03** | **Researcher Agent** | Discovery | Domain context & analytical taxonomy research | [`backend/app/analytics/semantic_layer.py`](./backend/app/analytics/semantic_layer.py) | [Spec 03](./docs/agents.md#3-researcher-agent) |
| **04** | **Planner Agent** | Planning | Converts question into executable analysis DAG | [`backend/app/services/analysis_runner.py`](./backend/app/services/analysis_runner.py) | [Spec 04](./docs/agents.md#4-planner-agent) |
| **05** | **Data Quality Agent** | Data Prep | Identifies quality issues & extreme anomalies | [`backend/app/analytics/quality.py`](./backend/app/analytics/quality.py) | [Spec 05](./docs/agents.md#5-data-quality-agent) |
| **06** | **Missing Value Agent** | Data Prep | Median/Mean/KNN imputation strategies | [`backend/app/analytics/imputation.py`](./backend/app/analytics/imputation.py) | [Spec 06](./docs/agents.md#6-missing-value-agent) |
| **07** | **KPI Discovery Agent** | Data Prep | Formulates & computes business domain metrics | [`backend/app/analytics/kpi.py`](./backend/app/analytics/kpi.py) | [Spec 07](./docs/agents.md#7-kpi-discovery-agent) |
| **08** | **Feature Engineering Agent**| Data Prep | Datetime, RFM, and log transformations | [`backend/app/analytics/feature_engineering.py`](./backend/app/analytics/feature_engineering.py) | [Spec 08](./docs/agents.md#8-feature-engineering-agent) |
| **09** | **Statistical Analysis Agent**| Analytics | Welch's t-tests, ANOVA, Cohen's d effect sizes | [`backend/app/analytics/statistics.py`](./backend/app/analytics/statistics.py) | [Spec 09](./docs/agents.md#9-statistical-analysis-agent) |
| **10** | **Machine Learning Agent** | Analytics | Random Forest, Logistic Regression feature importance | [`backend/app/analytics/ml_engine.py`](./backend/app/analytics/ml_engine.py) | [Spec 10](./docs/agents.md#10-machine-learning-agent) |
| **11** | **Anomaly Detection Agent** | Analytics | Isolation Forest outlier isolation | [`backend/app/analytics/anomaly.py`](./backend/app/analytics/anomaly.py) | [Spec 11](./docs/agents.md#11-anomaly-detection-agent) |
| **12** | **Segmentation Agent** | Analytics | K-Means clustering & Silhouette evaluation | [`backend/app/analytics/segmentation.py`](./backend/app/analytics/segmentation.py) | [Spec 12](./docs/agents.md#12-segmentation-agent) |
| **13** | **Forecasting Agent** | Analytics | Holt-Winters exponential trend forecasting | [`backend/app/analytics/forecasting.py`](./backend/app/analytics/forecasting.py) | [Spec 13](./docs/agents.md#13-forecasting-agent) |
| **14** | **Root Cause Agent (RCA)** | Decision Intel | DecisionTree variance decomposition | [`backend/app/analytics/root_cause.py`](./backend/app/analytics/root_cause.py) | [Spec 14](./docs/agents.md#14-root-cause-analysis-agent-rca) |
| **15** | **What-If Scenario Agent** | Decision Intel | Parameter shift simulation & ROI calculation | [`backend/app/analytics/scenario_engine.py`](./backend/app/analytics/scenario_engine.py) | [Spec 15](./docs/agents.md#15-what-if-scenario-agent) |
| **16** | **Validation Guardrail Agent**| Decision Intel | Claim grounding & causality verification | [`backend/app/analytics/visualization.py`](./backend/app/analytics/visualization.py) | [Spec 16](./docs/agents.md#16-validation--guardrail-agent) |
| **17** | **Executive Storytelling Agent**| Communication| Briefing generator, Markdown exporter & audio TTS | [`backend/app/services/report_exporter.py`](./backend/app/services/report_exporter.py) | [Spec 17](./docs/agents.md#17-executive-storytelling-agent) |

---

## 🔍 Real Execution Trace & Stage-by-Stage Artifacts

### User Business Question:
> *"Why did customer revenue decline in Q3, what factors contributed to the decline, and what actions could improve retention?"*

### Stage-by-Stage Artifact Evolution

```text
[03. RESEARCHER AGENT] ──► Identified Target: 'churn' | Entity: 'customer_id'
                          Key Objectives: Onboarding Completion, Support Tickets, Tenure, ARPU.

[04. PLANNER AGENT]    ──► Selected Execution DAG:
                          Imputation ➔ Feature Eng ➔ Welch t-test ➔ Random Forest ➔ RCA ➔ What-If Simulator.

[09. STATISTICS AGENT] ──► Numerical Calculation Output:
                          Welch t-test on Early Tenure: t = -4.12, p = 0.0002, Cohen's d = 0.74.
                          Interpretation: Statistically significant drop in early customer tenure.

[10. ML ENGINE AGENT]  ──► Feature Importance Ranking:
                          1. 'onboarding_completion_pct' (0.42)
                          2. 'support_tickets_30d'        (0.28)
                          3. 'avg_session_length'        (0.18)

[14. RCA AGENT]        ──► Driver Variance Decomposition:
                          Decision Tree isolated 64.2% of churn variance to the 0-90 day onboarding window.

[15. SCENARIO AGENT]   ──► Hypothetical Simulation Result:
                          +10% Onboarding Completion ➔ Projected Q4 Revenue Recovery: +$86,400.

[16. VALIDATION AGENT] ──► Evidence Grounding Status: PASSED (100% Grounded)
                          Language Enforcement: Correlation verified; unsubstantiated causal claims blocked.

[17. STORYTELLING]     ──► Executive Decision Brief Rendered (Markdown + Audio TTS Script + React Dashboard).
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

Automated benchmark evaluation script ([`evaluations/benchmark_runner.py`](./evaluations/benchmark_runner.py)) running across multi-domain enterprise datasets:

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

> **Engineering Disclaimer**: *These evaluation metrics are measured on our included benchmark suite across 10 multi-domain enterprise synthetic datasets (`evaluations/benchmark_runner.py`). They serve as empirical verification of single-node DAG execution, zero math hallucinations, and grounding guardrail compliance, rather than a generalized production accuracy SLA across all un-sanitized real-world datasets.*

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

- [`docs/agents.md`](./docs/agents.md) — 17 Agent specifications, contracts & implementation links.
- [`docs/final_enterprise_gap_analysis.md`](./docs/final_enterprise_gap_analysis.md) — 24-point audit & gap analysis.
- [`docs/architecture.md`](./docs/architecture.md) — Detailed system architecture & DAG specs.
- [`docs/technology-decisions.md`](./docs/technology-decisions.md) — Technology evaluation matrix.
- [`docs/governance.md`](./docs/governance.md) — Dataset SHA-256 hashing & decision lineage.
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
