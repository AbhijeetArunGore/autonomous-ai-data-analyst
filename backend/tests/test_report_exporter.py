import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_report_export_endpoints():
    # 1. Create Analysis Run
    create_res = client.post("/api/v1/analyses", json={
        "dataset_id": "ds_test",
        "business_goal": "Export report test objective"
    })
    # Since dataset ds_test isn't registered in mock, register it or test via runner directly
    from backend.app.services.analysis_runner import AnalysisRunnerService
    state = AnalysisRunnerService.create_analysis("anl_exp_test", "ds_test", "Export objective")
    
    md_res = client.get("/api/v1/analyses/anl_exp_test/export/markdown")
    assert md_res.status_code == 200
    assert "# Enterprise Executive Analytics Report" in md_res.json()["markdown"]
    
    audit_res = client.get("/api/v1/analyses/anl_exp_test/export/audit")
    assert audit_res.status_code == 200
    assert audit_res.json()["analysis_id"] == "anl_exp_test"
