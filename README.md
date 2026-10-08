# AI Data Analyst OS 🚀

> **Autonomous Multi-Agent Business Intelligence, Data Science and Consulting Platform**

AI Data Analyst OS is a production-grade internal analytics platform that accepts structured datasets (CSV/Excel) and natural language business objectives to autonomously profile data, perform research, plan analysis workflows, compute deterministic KPIs and statistics, engineer features, train baseline ML models, validate claims, and produce executive storytelling with audio narration.

---

## 🌟 Key Architecture & Features

- 🧠 **Multi-Agent DAG Orchestration**: Executes workflows over a structured analytical dependency graph instead of simple linear chains.
- 🔄 **Human-in-the-Loop & Selective Invalidation**: Analysts can modify decisions (e.g., missing value strategy, outlier threshold); the graph selectively invalidates strictly downstream dependent nodes.
- ⚡ **Deterministic Analytics**: Profiling, statistical tests, correlations, missingness, and KPI metrics are calculated exactly using Polars, SciPy, and DuckDB—never guessed by LLMs.
- 🛡️ **Claim & Grounding Guardrails**: Automatically verifies that insights match underlying numerical evidence and flags causal overreach.
- 💵 **Cost-Optimized Architecture**: Raw data is never dumped into LLMs; compact metadata summaries are routed intelligently based on configured cost tiers (`Economy`, `Balanced`, `Quality`).
- 🎧 **Executive Storytelling & Audio Narration**: Dual output for executives and technical analysts, with built-in voice narration scripts.

---

## 🏗 System Architecture

```text
[ Dataset Upload ]
       ↓
[ Deterministic Profiling (Polars/DuckDB) ] ───► [ External Research & Goal Alignment ]
       ↓                                                     ↓
[ Analytical Dependency Graph Planning ] ◄───────────────────┘
       ↓
 ┌─────┴─────────────────────┬────────────────────────┐
 ↓                           ↓                        ↓
[ Data Quality & Imputation ] [ KPI & Feature Discovery] [ Statistical & ML Analysis ]
 └─────┬─────────────────────┴────────────────────────┘
       ↓
[ Validation & Claim Verification Engine ]
       ↓
[ Insight Synthesis & Consulting Recommendations ]
       ↓
[ Executive Dashboard & Audio Narration ]
```

---

## 📁 Repository Structure

```text
ai-data-analyst-os/
├── backend/                  # FastAPI App, Agents, Analytics Engines, Workflows & Schemas
│   ├── app/
│   │   ├── api/              # REST Endpoints
│   │   ├── agents/           # Specialized Agent Wrappers
│   │   ├── analytics/        # Deterministic Polars/SciPy/Sklearn Engines
│   │   ├── workflows/        # Graph Orchestration & Invalidation Engine
│   │   ├── schemas/          # Pydantic Schemas & Artifact Definitions
│   │   ├── validators/       # Guardrail & Evidence Validators
│   │   ├── llm/              # LLM Provider Abstraction Layer
│   │   └── config/           # Application Settings
│   └── tests/                # Unit & Integration Test Suites
├── frontend/                 # React UI Dashboard & Workflow Graph Workspace
├── datasets/                 # Synthetic Demo Datasets (Sales, Churn, Fraud, Operations)
├── prompts/                  # Versioned System Prompts
├── docs/                     # Comprehensive Architecture & System Docs
├── pyproject.toml            # Python Configuration & Dependencies
├── Dockerfile                # Container Specification
├── docker-compose.yml        # Multi-service Orchestration
└── README.md
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend development)

### 2. Backend Setup
```bash
# Clone the repository
git clone https://github.com/your-org/ai-data-analyst-os.git
cd ai-data-analyst-os

# Create & activate virtual environment
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .[dev]

# Set environment variables
cp .env.example .env

# Run FastAPI backend server
uvicorn backend.app.main:app --reload --port 8000
```

### 3. Running Tests
```bash
pytest
```

---

## 📄 Documentation

Detailed documentation is available in the [`docs/`](./docs) directory:
- [System Architecture](./docs/architecture.md)
- [Agent Roster & Specs](./docs/agents.md)
- [Analytical Dependency Graph](./docs/workflow.md)
- [Data Lineage & Evidence System](./docs/data-lineage.md)
- [Evaluation Framework](./docs/evaluation.md)
- [Security & Defense](./docs/security.md)
- [Cost Optimization](./docs/cost-optimization.md)

---

## 📜 License
MIT License. See [LICENSE](./LICENSE) for details.
