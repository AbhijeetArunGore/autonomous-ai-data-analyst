import json
from typing import Dict, Any, Optional

class ReportExporterService:
    """
    Enterprise Report Exporter: Converts analysis run state and evidence DAG artifacts into
    formal Executive Markdown Reports, Technical Appendices, and Audit Trail JSON documents.
    """
    
    @staticmethod
    def export_markdown_report(state: Any) -> str:
        goal = getattr(state, "business_goal", "N/A")
        analysis_id = getattr(state, "analysis_id", "N/A")
        kpis = getattr(state, "kpi_catalog", None)
        insights = getattr(state, "insights", None)
        recs = getattr(state, "recommendations", None)
        story = getattr(state, "story_report", None)
        
        md_lines = [
          f"# Enterprise Executive Analytics Report",
          f"**Analysis ID**: `{analysis_id}`  ",
          f"**Business Objective**: {goal}  ",
          f"**Generated**: {getattr(state, 'created_at', 'N/A')}  ",
          f"---",
          f"## 1. Executive Summary",
        ]
        
        if story and hasattr(story, "executive_version"):
            exec_v = story.executive_version
            md_lines.append(f"### Headline: {exec_v.headline}\n")
            md_lines.append(f"**What Happened**: {exec_v.what_happened}\n")
            md_lines.append(f"**Why It Matters**: {exec_v.why_it_matters}\n")
            md_lines.append(f"**Primary Drivers**: {exec_v.primary_drivers}\n")
            md_lines.append(f"**Recommended Actions**: {exec_v.recommended_actions}\n")
            
        md_lines.append("\n## 2. Key Performance Indicators (KPIs)")
        if kpis and hasattr(kpis, "kpis"):
            for kpi in kpis.kpis:
                md_lines.append(f"- **{kpi.name}**: `{kpi.formatted_value}` (Formula: `{kpi.formula}`)")
                
        md_lines.append("\n## 3. Evidence-Grounded Insights")
        if insights and hasattr(insights, "insights"):
            for idx, ins in enumerate(insights.insights, 1):
                md_lines.append(f"### Insight #{idx}: {ins.title}")
                md_lines.append(f"- **Evidence**: {ins.evidence}")
                md_lines.append(f"- **Magnitude**: {ins.magnitude}")
                md_lines.append(f"- **Business Implication**: {ins.business_implication}\n")

        md_lines.append("\n## 4. Action Recommendations")
        if recs and hasattr(recs, "recommendations"):
            for idx, rec in enumerate(recs.recommendations, 1):
                md_lines.append(f"### Action #{idx}: {rec.recommendation}")
                md_lines.append(f"- **Priority**: {rec.priority} | **Impact**: {rec.expected_impact} | **Effort**: {rec.effort}")
                md_lines.append(f"- **Required Action**: {rec.required_action}")
                md_lines.append(f"- **Owner**: {rec.owner} | **KPI**: {rec.measurement_kpi}\n")
                
        md_lines.append("\n## 5. Governance & Audit Trail")
        decisions = getattr(state, "decisions", [])
        if decisions:
            for dec in decisions:
                md_lines.append(f"- **Decision `{dec.decision_id}`**: {dec.parameter_key} changed `{dec.old_value}` -> `{dec.new_value}` ({dec.reason})")
        else:
            md_lines.append("- No manual analyst interventions logged.")

        return "\n".join(md_lines)

    @staticmethod
    def export_audit_json(state: Any) -> Dict[str, Any]:
        return {
            "analysis_id": getattr(state, "analysis_id", "N/A"),
            "dataset_id": getattr(state, "dataset_id", "N/A"),
            "business_goal": getattr(state, "business_goal", "N/A"),
            "status": getattr(state, "status", "N/A"),
            "total_cost_usd": getattr(state, "total_cost_usd", 0.0),
            "total_duration_ms": getattr(state, "total_duration_ms", 0.0),
            "decisions": [d.model_dump() for d in getattr(state, "decisions", [])],
            "execution_order": state.dag.get_execution_order() if hasattr(state, "dag") else []
        }
