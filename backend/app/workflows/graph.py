from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, Set
import time

class NodeStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    VALID = "VALID"
    INVALIDATED = "INVALIDATED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

class DAGNode(BaseModel):
    node_id: str
    agent_name: str
    dependencies: List[str] = []
    status: NodeStatus = NodeStatus.PENDING
    parameters: Dict[str, Any] = {}
    inputs: List[str] = []
    outputs: List[str] = []
    execution_time_ms: float = 0.0
    token_cost: float = 0.0
    model_info: str = "mock-engine-v1"
    error_message: Optional[str] = None

class DependencyGraph(BaseModel):
    nodes: Dict[str, DAGNode] = {}

    def add_node(self, node: DAGNode):
        self.nodes[node.node_id] = node

    def get_downstream_nodes(self, start_node_id: str) -> Set[str]:
        """
        Computes the transitive closure of downstream dependent nodes for selective invalidation.
        """
        downstream = set()
        queue = [start_node_id]
        
        while queue:
            curr = queue.pop(0)
            for node_id, node in self.nodes.items():
                if curr in node.dependencies and node_id not in downstream:
                    downstream.add(node_id)
                    queue.append(node_id)
                    
        return downstream

    def invalidate_from(self, node_id: str) -> List[str]:
        """
        Invalidates node_id and all its downstream dependent nodes.
        Returns list of invalidated node IDs.
        """
        if node_id not in self.nodes:
            return []
            
        affected = self.get_downstream_nodes(node_id)
        affected.add(node_id)
        
        invalidated_list = []
        for nid in affected:
            self.nodes[nid].status = NodeStatus.INVALIDATED
            invalidated_list.append(nid)
            
        return invalidated_list

    def get_execution_order(self) -> List[str]:
        """
        Returns topological sort execution order.
        """
        in_degree = {nid: 0 for nid in self.nodes}
        for node in self.nodes.values():
            for dep in node.dependencies:
                if dep in self.nodes:
                    in_degree[node.node_id] += 1
                    
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        order = []
        
        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for nid, node in self.nodes.items():
                if curr in node.dependencies:
                    in_degree[nid] -= 1
                    if in_degree[nid] == 0:
                        queue.append(nid)
                        
        return order

def create_default_analytical_dag() -> DependencyGraph:
    dag = DependencyGraph()
    
    nodes = [
        DAGNode(node_id="intake", agent_name="DataIntakeAgent", dependencies=[]),
        DAGNode(node_id="profiling", agent_name="DataProfilingAgent", dependencies=["intake"]),
        DAGNode(node_id="research", agent_name="ResearcherAgent", dependencies=["profiling"]),
        DAGNode(node_id="plan", agent_name="PlannerAgent", dependencies=["profiling", "research"]),
        DAGNode(node_id="quality", agent_name="DataQualityAgent", dependencies=["profiling", "plan"]),
        DAGNode(node_id="imputation", agent_name="MissingValueAgent", dependencies=["quality"]),
        DAGNode(node_id="features", agent_name="FeatureEngineeringAgent", dependencies=["imputation"]),
        DAGNode(node_id="kpis", agent_name="KPIDiscoveryAgent", dependencies=["features", "plan"]),
        DAGNode(node_id="statistics", agent_name="StatisticalAnalysisAgent", dependencies=["kpis"]),
        DAGNode(node_id="ml", agent_name="MachineLearningAgent", dependencies=["features", "plan"]),
        DAGNode(node_id="anomaly", agent_name="AnomalyDetectionAgent", dependencies=["features"]),
        DAGNode(node_id="segmentation", agent_name="SegmentationAgent", dependencies=["features"]),
        DAGNode(node_id="visualizations", agent_name="VisualizationAgent", dependencies=["statistics", "kpis"]),
        DAGNode(node_id="validation", agent_name="ValidationAgent", dependencies=["statistics", "ml", "visualizations"]),
        DAGNode(node_id="insights", agent_name="InsightAgent", dependencies=["validation"]),
        DAGNode(node_id="recommendations", agent_name="ConsultingAgent", dependencies=["insights"]),
        DAGNode(node_id="storytelling", agent_name="StorytellingAgent", dependencies=["recommendations"])
    ]
    
    for n in nodes:
        dag.add_node(n)
        
    return dag
