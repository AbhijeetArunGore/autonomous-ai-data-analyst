import hashlib
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class GovernanceRecord(BaseModel):
    record_id: str
    analysis_id: str
    dataset_version_hash: str
    code_version: str = "v0.1.0-Enterprise"
    prompt_version: str = "v1.0"
    model_name: str = "mock-engine-v1"
    assumptions: List[str]
    limitations: List[str]
    human_approved: bool = True
    approved_by: str = "Enterprise Analyst Lead"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GovernanceSubsystem:
    """
    Enterprise Governance Subsystem: Maintains dataset version hashes, code versions,
    human approval records, prompt registries, and analytical reproducibility metadata.
    """
    
    _records: Dict[str, GovernanceRecord] = {}

    @classmethod
    def compute_dataset_hash(cls, content: bytes) -> str:
        return f"sha256:{hashlib.sha256(content).hexdigest()}"

    @classmethod
    def record_governance(
        cls,
        analysis_id: str,
        dataset_content: bytes,
        assumptions: List[str],
        limitations: List[str]
    ) -> GovernanceRecord:
        h_val = cls.compute_dataset_hash(dataset_content)
        rec = GovernanceRecord(
            record_id=f"gov_{analysis_id}",
            analysis_id=analysis_id,
            dataset_version_hash=h_val,
            assumptions=assumptions or ["Data sampled representatively"],
            limitations=limitations or ["Observational data association; direct causality not established."]
        )
        cls._records[analysis_id] = rec
        return rec

    @classmethod
    def get_governance(cls, analysis_id: str) -> Optional[GovernanceRecord]:
        return cls._records.get(analysis_id)
