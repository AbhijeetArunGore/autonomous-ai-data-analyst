# Cost Optimization & Token Budgeting

## Deterministic Offloading Strategy
To optimize LLM costs and prevent token exhaustion:
1. **Raw CSV Files Are Never Sent to LLMs**: Datasets are profiled deterministically using Polars/DuckDB. Only compact structured metadata JSON summaries (schema, distributions, sample rows) are passed to LLM agents.
2. **Model Routing Tiers**:
   - **Economy Mode**: Uses lighter, faster models (e.g. `gpt-4o-mini`, `gemini-1.5-flash`) for all tasks.
   - **Balanced Mode** (Default): Uses lighter models for simple tasks (Profiling, KPI format) and stronger models (`gpt-4o`, `claude-3-5-sonnet`, `gemini-1.5-pro`) for Planning, Synthesis, and Storytelling.
   - **Quality Mode**: Uses top-tier models across all planning, validation, and recommendation steps.

## Response Caching & Structured Outputs
- Deterministic analysis outputs (profiling summary, statistical test outputs) are cached by dataset hash.
- All LLM agents return typed JSON conforming strictly to Pydantic schemas, minimizing redundant retry tokens.
- Token usage and estimated cost ($ USD) are logged per node execution and exposed via the Cost API.
