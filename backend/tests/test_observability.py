import pytest
from backend.app.observability.logger import StructuredLogger

def test_structured_logger():
    obs = StructuredLogger(service_name="test-obs")
    event = obs.log_agent_execution(
        analysis_id="anl_test123",
        agent_name="KPIDiscoveryAgent",
        node_id="kpis",
        status="VALID",
        duration_ms=125.4,
        token_cost=0.0012
    )
    
    assert event["event_type"] == "AGENT_EXECUTION"
    assert event["agent"] == "KPIDiscoveryAgent"
    assert event["duration_ms"] == 125.4
