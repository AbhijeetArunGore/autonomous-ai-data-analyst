# Security & Guardrails Architecture

## File Upload Security
- **MIME & File Extension Validation**: Uploaded files are verified via byte inspection (`magic` numbers / header checks) for `.csv`, `.xlsx`, `.xls`.
- **File Size & Memory Limits**: Configurable file size limits (default 50MB for upload, streaming DuckDB for large queries).
- **Filename Sanitization & Path Traversal Prevention**: Safe filename generation with strict UUID isolation in temporary directories.

## Prompt Injection Protection
- **Data Content Isolation**: User dataset content is strictly formatted inside XML boundaries (`<DATASET_SAMPLE>`, `<PROFILING_SUMMARY>`) and never mixed with `<SYSTEM_INSTRUCTIONS>`.
- **Instruction Rejection**: Agents are instructed via system prompts to treat dataset string cell values strictly as inert text data, ignoring any embedded instructions (e.g. "Ignore previous instructions").

## Safe Execution Policy
- Arbitrary python code execution directly on the host machine from LLM output is prohibited.
- Predefined, audited analytical routines (Polars, SciPy, Scikit-learn) are used for analytical tasks.
- If custom code execution is required, execution occurs inside isolated sandbox containers with timeout enforcement.
