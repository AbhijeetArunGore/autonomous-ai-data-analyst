import pytest
from backend.app.workflows.graph import create_default_analytical_dag, NodeStatus

def test_dag_execution_order():
    dag = create_default_analytical_dag()
    order = dag.get_execution_order()
    
    assert len(order) == 17
    assert order[0] == "intake"
    assert order.index("intake") < order.index("profiling")
    assert order.index("profiling") < order.index("plan")
    assert order.index("plan") < order.index("quality")
    assert order.index("quality") < order.index("imputation")
    assert order.index("imputation") < order.index("features")
    assert order.index("features") < order.index("kpis")
    assert order.index("insights") < order.index("recommendations")

def test_selective_invalidation():
    dag = create_default_analytical_dag()
    
    # Mark all nodes as VALID initially
    for node in dag.nodes.values():
        node.status = NodeStatus.VALID
        
    # User changes parameter on 'imputation' node
    invalidated = dag.invalidate_from("imputation")
    
    # Check that imputation and all downstream nodes are invalidated
    assert "imputation" in invalidated
    assert "features" in invalidated
    assert "kpis" in invalidated
    assert "statistics" in invalidated
    assert "ml" in invalidated
    assert "insights" in invalidated
    assert "recommendations" in invalidated
    assert "storytelling" in invalidated
    
    # Check that independent upstream nodes remain VALID
    assert dag.nodes["intake"].status == NodeStatus.VALID
    assert dag.nodes["profiling"].status == NodeStatus.VALID
    assert dag.nodes["research"].status == NodeStatus.VALID
    assert dag.nodes["plan"].status == NodeStatus.VALID
