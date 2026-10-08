import os
import uuid
import tempfile
import polars as pl
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from backend.app.schemas.dataset import DatasetMetadata, DatasetUploadResponse
from backend.app.agents.intake_agent import DataIntakeAgent
from backend.app.services.analysis_runner import AnalysisRunnerService, AnalysisRunState

router = APIRouter()

class CreateAnalysisRequest(BaseModel):
    dataset_id: str
    business_goal: str

class DecisionPatchRequest(BaseModel):
    node_id: str
    parameter_key: str
    new_value: Any
    reason: Optional[str] = "Analyst intervention"

@router.post("/datasets", response_model=DatasetUploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
        
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".csv", ".xlsx", ".xls"]:
        raise HTTPException(status_code=400, detail=f"Unsupported file format: {ext}")

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        agent = DataIntakeAgent()
        metadata, df = agent.process_file(tmp_path, file.filename)
        AnalysisRunnerService.register_dataset(metadata, df)
        return DatasetUploadResponse(
            dataset_id=metadata.dataset_id,
            metadata=metadata,
            message="Dataset uploaded, validated, and profiled successfully."
        )
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

@router.get("/datasets/{dataset_id}")
async def get_dataset_metadata(dataset_id: str):
    data = AnalysisRunnerService.get_dataset(dataset_id)
    if not data:
        raise HTTPException(status_code=404, detail="Dataset not found")
    metadata, _ = data
    return metadata

@router.post("/analyses")
async def create_analysis(req: CreateAnalysisRequest):
    dataset_data = AnalysisRunnerService.get_dataset(req.dataset_id)
    if not dataset_data:
        raise HTTPException(status_code=404, detail="Dataset not found")
        
    analysis_id = f"anl_{uuid.uuid4().hex[:12]}"
    state = AnalysisRunnerService.create_analysis(analysis_id, req.dataset_id, req.business_goal)
    return {
        "analysis_id": state.analysis_id,
        "dataset_id": state.dataset_id,
        "business_goal": state.business_goal,
        "status": state.status,
        "nodes": list(state.dag.nodes.keys())
    }

@router.get("/analyses/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    state = AnalysisRunnerService.get_analysis(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return {
        "analysis_id": state.analysis_id,
        "dataset_id": state.dataset_id,
        "business_goal": state.business_goal,
        "status": state.status,
        "nodes": state.dag.nodes,
        "total_cost_usd": state.total_cost_usd,
        "total_duration_ms": state.total_duration_ms,
        "decisions_count": len(state.decisions)
    }

@router.post("/analyses/{analysis_id}/run")
async def run_analysis(analysis_id: str):
    try:
        state = AnalysisRunnerService.execute_dag(analysis_id)
        return {
            "analysis_id": state.analysis_id,
            "status": state.status,
            "total_duration_ms": state.total_duration_ms,
            "total_cost_usd": state.total_cost_usd
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/analyses/{analysis_id}/decisions")
async def patch_decision(analysis_id: str, req: DecisionPatchRequest):
    try:
        invalidated = AnalysisRunnerService.apply_decision(
            analysis_id, req.node_id, req.parameter_key, req.new_value, req.reason or ""
        )
        return {
            "analysis_id": analysis_id,
            "node_modified": req.node_id,
            "parameter_key": req.parameter_key,
            "new_value": req.new_value,
            "invalidated_downstream_nodes": invalidated,
            "message": f"Parameter updated. {len(invalidated)} downstream nodes invalidated and queued for re-execution."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/analyses/{analysis_id}/rerun")
async def rerun_analysis(analysis_id: str):
    return await run_analysis(analysis_id)

@router.get("/analyses/{analysis_id}/artifacts")
async def get_analysis_artifacts(analysis_id: str):
    state = AnalysisRunnerService.get_analysis(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return {
        "profile": state.profile,
        "research": state.research,
        "plan": state.plan,
        "kpis": state.kpi_catalog,
        "statistics": state.stats_report,
        "ml": state.ml_report,
        "anomalies": state.anomaly_report,
        "segmentation": state.segmentation_report,
        "visualizations": state.visualization_catalog,
        "validation": state.validation_report,
        "insights": state.insights,
        "recommendations": state.recommendations,
        "story": state.story_report
    }

@router.get("/analyses/{analysis_id}/lineage")
async def get_analysis_lineage(analysis_id: str):
    state = AnalysisRunnerService.get_analysis(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return {
        "analysis_id": analysis_id,
        "dataset_id": state.dataset_id,
        "decisions": state.decisions,
        "execution_order": state.dag.get_execution_order(),
        "node_dependencies": {nid: node.dependencies for nid, node in state.dag.nodes.items()}
    }

@router.get("/analyses/{analysis_id}/cost")
async def get_analysis_cost(analysis_id: str):
    state = AnalysisRunnerService.get_analysis(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return {
        "analysis_id": analysis_id,
        "total_cost_usd": state.total_cost_usd,
        "node_costs": {nid: node.token_cost for nid, node in state.dag.nodes.items()}
    }

@router.get("/analyses/{analysis_id}/export/markdown")
async def export_markdown_report(analysis_id: str):
    from backend.app.services.report_exporter import ReportExporterService
    state = AnalysisRunnerService.get_analysis(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    markdown_content = ReportExporterService.export_markdown_report(state)
    return {"analysis_id": analysis_id, "markdown": markdown_content}

@router.get("/analyses/{analysis_id}/export/audit")
async def export_audit_json(analysis_id: str):
    from backend.app.services.report_exporter import ReportExporterService
    state = AnalysisRunnerService.get_analysis(analysis_id)
    if not state:
        raise HTTPException(status_code=404, detail="Analysis run not found")
    return ReportExporterService.export_audit_json(state)
