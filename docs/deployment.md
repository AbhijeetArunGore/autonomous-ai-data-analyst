# Deployment & Production Architecture

## Docker Containerization

AI Data Analyst OS is designed for multi-container deployment via Docker Compose or Kubernetes:
- **Backend Service**: FastAPI server running Uvicorn.
- **Frontend Service**: Next.js / Vite React static build hosted via Nginx or Node.
- **Database Service**: PostgreSQL for persistent metadata, run state, and artifact catalog.
- **Worker Queue**: Background job execution for async workflow processing.

## Production Configuration Checklist
1. Set `ENVIRONMENT=production` in environment variables.
2. Provide valid production `DATABASE_URL` (PostgreSQL).
3. Configure secret keys and LLM API keys via secret manager.
4. Set CORS origins to allowed domain endpoints.
