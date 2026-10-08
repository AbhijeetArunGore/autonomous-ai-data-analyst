# Governance & Decision Lineage Architecture

## Overview
Enterprise Decision Intelligence platforms must provide complete reproducibility, auditability, and human approval tracking.

## Core Governance Dimensions

1. **Dataset Versioning**: Every uploaded or connected dataset is tracked via SHA-256 content hashes.
2. **Decision Lineage**: Human-In-The-Loop parameter changes (e.g. median -> mean imputation) generate immutable audit records.
3. **Model & Prompt Registries**: ML model metrics, train/test splits, and versioned system prompts are logged per execution.
4. **Assumptions & Limitations Disclosure**: Reports explicitly distinguish between observed facts, statistical associations, and predictive inferences.
5. **Human Approval Gates**: Consequential business recommendations require explicit analyst sign-off before downstream action triggers.
