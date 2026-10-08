import polars as pl
from backend.app.analytics.profiler import DeterministicProfiler
from backend.app.schemas.profiling import DataProfile

class DataProfilingAgent:
    """
    Data Profiling Agent (Agent 2): Performs exact deterministic dataset profiling.
    Strict rule: Never ask LLM to compute mathematical/statistical summaries.
    """
    
    def __init__(self):
        self.engine = DeterministicProfiler()
        
    def profile(self, df: pl.DataFrame, dataset_id: str) -> DataProfile:
        return self.engine.profile_dataframe(df, dataset_id)
