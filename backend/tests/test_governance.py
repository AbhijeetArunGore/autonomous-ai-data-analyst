import pytest
from backend.app.governance.registry import GovernanceSubsystem

def test_governance_subsystem():
    raw_bytes = b"customer_id,churn\nC001,0\nC002,1\n"
    rec = GovernanceSubsystem.record_governance(
        analysis_id="anl_gov1",
        dataset_content=raw_bytes,
        assumptions=["Data is complete"],
        limitations=["Small sample"]
    )
    
    assert rec.analysis_id == "anl_gov1"
    assert rec.dataset_version_hash.startswith("sha256:")
    assert rec.human_approved is True
    
    fetched = GovernanceSubsystem.get_governance("anl_gov1")
    assert fetched is not None
    assert fetched.record_id == "gov_anl_gov1"
