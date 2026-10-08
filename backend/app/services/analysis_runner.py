import os
import time
import polars as pl
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from backend.app.schemas.dataset import DatasetMetadata
from backend.app.schemas.profiling import DataProfile
from backend.app.schemas.research import ResearchReport
from backend.app.schemas.plan import AnalysisPlan
from backend.app.schemas.insight import InsightReport
from backend.app.schemas.recommendation import RecommendationReport
from backend.app.schemas.story import DualStoryReport

from backend.app.workflows.graph import create_default_analytical_dag, DependencyGraph, NodeStatus
from backend.app.agents.intake_agent import DataIntakeAgent
from backend.app.agents.profiler_agent import DataProfilingAgent
from backend.app.agents.researcher_agent import ResearcherAgent
from backend.app.agents.planner_agent import PlannerAgent
from backend.app.analytics.quality import DataQualityAnalyzer
from backend.app.analytics.imputation import MissingValueEngine
from backend.app.analytics.feature_engineering import FeatureEngineeringEngine
from backend.app.analytics.kpi import DeterministicKPIEngine
from backend.app.analytics.statistics import StatisticalAnalysisEngine
from backend.app.analytics.ml_engine import MLEngine
from backend.app.analytics.anomaly import AnomalyDetectionEngine
from backend.app.analytics.segmentation import SegmentationEngine
from backend.app.analytics.visualization import DeterministicVisualizationEngine
from backend.app.validators.validation_engine import ValidationEngine
from backend.app.agents.insight_agent import InsightAgent
from backend.app.agents.consulting_agent import ConsultingAgent
from backend.app.agents.storytelling_agent import StorytellingAgent

class AnalysisDecision(BaseModel):
    decision_id: str
    node_id: str
    parameter_key: str
    old_value: Any
    new_value: Any
    reason: str = "Analyst intervention"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class AnalysisRunState(BaseModel):
    analysis_id: str
    dataset_id: str
    business_goal: str
    status: str = "CREATED"  # CREATED, RUNNING, COMPLETED, FAILED
    dag: DependencyGraph
    decisions: List[AnalysisDecision] = []
    total_cost_usd: float = 0.0
    total_duration_ms: float = 0.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Execution Artifact Storage
    raw_df: Optional[Any] = None
    processed_df: Optional[Any] = None
    profile: Optional[DataProfile] = None
    research: Optional[ResearchReport] = None
    plan: Optional[AnalysisPlan] = None
    kpi_catalog: Optional[Any] = None
    stats_report: Optional[Any] = None
    ml_report: Optional[Any] = None
    anomaly_report: Optional[Any] = None
    segmentation_report: Optional[Any] = None
    visualization_catalog: Optional[Any] = None
    validation_report: Optional[Any] = None
    insights: Optional[InsightReport] = None
    recommendations: Optional[RecommendationReport] = None
    story_report: Optional[DualStoryReport] = None

class AnalysisRunnerService:
    """
    Analysis Runner Service: Orchestrates the analytical graph execution, stores state,
    applies analyst HITL decision changes, and executes selective re-runs.
    """
    
    _runs_db: Dict[str, AnalysisRunState] = {}
    _datasets_db: Dict[str, Tuple[DatasetMetadata, pl.DataFrame]] = {}
    
    @classmethod
    def register_dataset(cls, metadata: DatasetMetadata, df: pl.DataFrame):
        cls._datasets_db[metadata.dataset_id] = (metadata, df)
        
    @classmethod
    def get_dataset(cls, dataset_id: str):
        return cls._datasets_db.get(dataset_id)
        
    @classmethod
    def create_analysis(cls, analysis_id: str, dataset_id: str, business_goal: str) -> AnalysisRunState:
        dag = create_default_analytical_dag()
        state = AnalysisRunState(
            analysis_id=analysis_id,
            dataset_id=dataset_id,
            business_goal=business_goal,
            dag=dag
        )
        cls._runs_db[analysis_id] = state
        return state

    @classmethod
    def get_analysis(cls, analysis_id: str) -> Optional[AnalysisRunState]:
        return cls._runs_db.get(analysis_id)

    @classmethod
    def execute_dag(cls, analysis_id: str) -> AnalysisRunState:
        state = cls._runs_db.get(analysis_id)
        if not state:
            raise ValueError(f"Analysis run {analysis_id} not found.")
            
        dataset_tuple = cls._datasets_db.get(state.dataset_id)
        if not dataset_tuple:
            raise ValueError(f"Dataset {state.dataset_id} not found.")
            
        metadata, df = dataset_tuple
        state.raw_df = df
        state.status = "RUNNING"
        
        start_time = time.time()
        order = state.dag.get_execution_order()
        
        for node_id in order:
            node = state.dag.nodes[node_id]
            if node.status in [NodeStatus.VALID, NodeStatus.SKIPPED]:
                continue
                
            node.status = NodeStatus.RUNNING
            node_start = time.time()
            
            try:
                if node_id == "intake":
                    node.status = NodeStatus.VALID
                elif node_id == "profiling":
                    profiler = DataProfilingAgent()
                    state.profile = profiler.profile(df, metadata.dataset_id)
                    node.status = NodeStatus.VALID
                elif node_id == "research":
                    researcher = ResearcherAgent()
                    state.research = researcher.research(state.business_goal, state.profile)
                    node.status = NodeStatus.VALID
                elif node_id == "plan":
                    planner = PlannerAgent()
                    state.plan = planner.plan(state.business_goal, state.profile, state.research)
                    node.status = NodeStatus.VALID
                elif node_id == "quality":
                    node.status = NodeStatus.VALID
                elif node_id == "imputation":
                    strategy = node.parameters.get("missing_strategy", "median")
                    impute_map = {col: strategy for col in df.columns}
                    state.processed_df, _ = MissingValueEngine.impute(df, impute_map)
                    node.status = NodeStatus.VALID
                elif node_id == "features":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.processed_df, _ = FeatureEngineeringEngine.transform(cur_df)
                    node.status = NodeStatus.VALID
                elif node_id == "kpis":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.kpi_catalog = DeterministicKPIEngine.discover_and_compute(cur_df, state.business_goal)
                    node.status = NodeStatus.VALID
                elif node_id == "statistics":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.stats_report = StatisticalAnalysisEngine.analyze(cur_df)
                    node.status = NodeStatus.VALID
                elif node_id == "ml":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.ml_report = MLEngine.train_and_evaluate(cur_df)
                    node.status = NodeStatus.VALID
                elif node_id == "anomaly":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.anomaly_report = AnomalyDetectionEngine.detect(cur_df)
                    node.status = NodeStatus.VALID
                elif node_id == "segmentation":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.segmentation_report = SegmentationEngine.segment(cur_df)
                    node.status = NodeStatus.VALID
                elif node_id == "visualizations":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.visualization_catalog = DeterministicVisualizationEngine.generate_charts(
                        cur_df, state.kpi_catalog.kpis if state.kpi_catalog else [], state.stats_report
                    )
                    node.status = NodeStatus.VALID
                elif node_id == "validation":
                    cur_df = state.processed_df if state.processed_df is not None else df
                    state.validation_report = ValidationEngine.validate_analysis(
                        df_rows=cur_df.shape[0],
                        kpi_catalog=state.kpi_catalog,
                        stats_report=state.stats_report,
                        ml_report=state.ml_report,
                        insights=[],
                        recommendations=[]
                    )
                    node.status = NodeStatus.VALID
                elif node_id == "insights":
                    agent = InsightAgent()
                    state.insights = agent.synthesize(state.kpi_catalog, state.stats_report, state.ml_report)
                    node.status = NodeStatus.VALID
                elif node_id == "recommendations":
                    agent = ConsultingAgent()
                    state.recommendations = agent.recommend(state.insights)
                    node.status = NodeStatus.VALID
                elif node_id == "storytelling":
                    agent = StorytellingAgent()
                    state.story_report = agent.generate_story(state.insights, state.recommendations)
                    node.status = NodeStatus.VALID
                    
                node.execution_time_ms = (time.time() - node_start) * 1000
                node.token_cost = 0.001
                
            except Exception as e:
                node.status = NodeStatus.FAILED
                node.error_message = str(e)
                state.status = "FAILED"
                raise e
                
        state.status = "COMPLETED"
        state.total_duration_ms = (time.time() - start_time) * 1000
        state.total_cost_usd = round(sum(n.token_cost for n in state.dag.nodes.values()), 4)
        return state

    @classmethod
    def apply_decision(cls, analysis_id: str, node_id: str, param_key: str, new_val: Any, reason: str = "") -> List[str]:
        state = cls._runs_db.get(analysis_id)
        if not state:
            raise ValueError(f"Analysis {analysis_id} not found.")
            
        node = state.dag.nodes.get(node_id)
        if not node:
            raise ValueError(f"Node {node_id} not found in DAG.")
            
        old_val = node.parameters.get(param_key)
        node.parameters[param_key] = new_val
        
        # Log decision
        decision = AnalysisDecision(
            decision_id=f"dec_{int(time.time()*1000)}",
            node_id=node_id,
            parameter_key=param_key,
            old_value=old_val,
            new_value=new_val,
            reason=reason or "Analyst HITL intervention"
        )
        state.decisions.append(decision)
        
        # Selectively invalidate downstream nodes
        invalidated = state.dag.invalidate_from(node_id)
        state.status = "PARTIAL_INVALIDATED"
        return invalidated
