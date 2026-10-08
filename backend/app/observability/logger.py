import json
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime, timezone

class StructuredLogger:
    """
    Enterprise Observability Logger: Produces structured JSON log events,
    trace spans, agent telemetry, and token cost metrics.
    """
    
    def __init__(self, service_name: str = "ai-data-analyst-os"):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def log_agent_execution(
        self,
        analysis_id: str,
        agent_name: str,
        node_id: str,
        status: str,
        duration_ms: float,
        token_cost: float = 0.0,
        metadata: Optional[Dict[str, Any]] = None
    ):
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "service": self.service_name,
            "analysis_id": analysis_id,
            "event_type": "AGENT_EXECUTION",
            "agent": agent_name,
            "node_id": node_id,
            "status": status,
            "duration_ms": round(duration_ms, 2),
            "token_cost_usd": round(token_cost, 5),
            "metadata": metadata or {}
        }
        self.logger.info(json.dumps(event))
        return event

logger = StructuredLogger()
