from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.router import router as api_router

app = FastAPI(
    title="AI Data Analyst OS API",
    description="Autonomous Multi-Agent BI, Data Science and Consulting Platform Backend",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Data Analyst OS API",
        "version": "0.1.0"
    }
