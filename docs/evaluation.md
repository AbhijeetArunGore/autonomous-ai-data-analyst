# Agent Evaluation Framework & Scorecards

## Evaluation Dimensions

To guarantee analytical correctness and avoid hallucinations, AI Data Analyst OS implements an automated evaluation suite testing 5 key dimensions:

1. **Data Correctness**: Ensures mathematical metrics, missing counts, correlation values, and formulas match exact Polars/SciPy outputs.
2. **Methodological Appropriateness**: Verifies that agents select valid statistical tests based on column data types and distribution assumptions.
3. **Insight Faithfulness**: Tests whether claims synthesized by the Insight Agent match the numerical evidence in statistical artifacts.
4. **Recommendation Grounding**: Verifies that business recommendations directly reference identified insights and actionable levers.
5. **Cost & Latency Efficiency**: Tracks token consumption and total execution duration per agent.

## Agent Scorecard Metrics

The system calculates empirical performance metrics for each agent:
- **Accuracy**: Percentage of calculations matching ground truth.
- **Validation Pass Rate**: Percentage of generated artifacts passing strict schema and claim guardrails.
- **Average Latency**: Mean execution time in milliseconds.
- **Average Cost**: Mean LLM cost per run in USD.
- **Failure Rate**: Percentage of unrecoverable agent errors.
