import pytest
import io
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_e2e_analysis_lifecycle():
    # 1. Upload CSV Dataset
    csv_data = """customer_id,age,revenue,churn
C001,25,150.0,0
C002,34,300.0,1
C003,45,450.0,0
C004,22,120.0,0
C005,55,800.0,1
"""
    files = {"file": ("test_sales.csv", io.BytesIO(csv_data.encode("utf-8")), "text/csv")}
    upload_res = client.post("/api/v1/datasets", files=files)
    assert upload_res.status_code == 200
    dataset_id = upload_res.json()["dataset_id"]
    assert dataset_id != ""

    # 2. Create Analysis Run
    create_res = client.post("/api/v1/analyses", json={
        "dataset_id": dataset_id,
        "business_goal": "Identify churn drivers and revenue improvement levers"
    })
    assert create_res.status_code == 200
    analysis_id = create_res.json()["analysis_id"]

    # 3. Execute Analysis DAG
    run_res = client.post(f"/api/v1/analyses/{analysis_id}/run")
    assert run_res.status_code == 200, f"Run failed: {run_res.status_code} - {run_res.text}"
    assert run_res.json()["status"] == "COMPLETED"

    # 4. Get Artifacts
    artifact_res = client.get(f"/api/v1/analyses/{analysis_id}/artifacts")
    assert artifact_res.status_code == 200
    artifacts = artifact_res.json()
    assert artifacts["profile"]["total_rows"] == 5
    assert artifacts["insights"] is not None
    assert artifacts["story"]["executive_version"]["narration_script"] != ""

    # 5. Analyst HITL Decision Patch (e.g., Change Imputation Strategy)
    patch_res = client.patch(f"/api/v1/analyses/{analysis_id}/decisions", json={
        "node_id": "imputation",
        "parameter_key": "missing_strategy",
        "new_value": "mean",
        "reason": "Analyst preferred mean imputation for symmetric numeric metrics"
    })
    assert patch_res.status_code == 200
    invalidated_nodes = patch_res.json()["invalidated_downstream_nodes"]
    assert "imputation" in invalidated_nodes
    assert "features" in invalidated_nodes
    assert "insights" in invalidated_nodes

    # 6. Re-run Analysis
    rerun_res = client.post(f"/api/v1/analyses/{analysis_id}/rerun")
    assert rerun_res.status_code == 200
    assert rerun_res.json()["status"] == "COMPLETED"
