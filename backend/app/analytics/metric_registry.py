from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class BusinessMetric(BaseModel):
    metric_id: str
    metric_name: str
    domain: str  # Healthcare, Finance, SaaS, Retail, Construction, HR, Logistics, General
    definition: str
    formula: str
    source_fields: List[str]
    business_meaning: str
    owner: str = "Enterprise Analytics Center of Excellence"
    version: str = "1.0"

class MetricRegistry:
    """
    Business Metric Registry: Catalog of standardized metric definitions across industries.
    """
    
    _registry: Dict[str, BusinessMetric] = {}

    @classmethod
    def register_metric(cls, metric: BusinessMetric):
        cls._registry[metric.metric_id] = metric

    @classmethod
    def get_metric(cls, metric_id: str) -> Optional[BusinessMetric]:
        return cls._registry.get(metric_id)

    @classmethod
    def list_metrics(cls, domain: Optional[str] = None) -> List[BusinessMetric]:
        if domain:
            return [m for m in cls._registry.values() if m.domain.lower() == domain.lower()]
        return list(cls._registry.values())

# Pre-register standard enterprise metrics across 8 core domains
standard_metrics = [
    BusinessMetric(
        metric_id="metric_saas_churn",
        metric_name="Customer Churn Rate",
        domain="SaaS",
        definition="Percentage of active customer subscriptions canceled during the observation window",
        formula="MEAN(churn == 1) * 100",
        source_fields=["churn", "customer_id"],
        business_meaning="Core indicator of retention and recurring revenue stability"
    ),
    BusinessMetric(
        metric_id="metric_health_readmission",
        metric_name="30-Day Readmission Rate",
        domain="Healthcare",
        definition="Percentage of discharged patients readmitted within 30 days",
        formula="MEAN(readmitted_30d == 1) * 100",
        source_fields=["readmitted_30d", "patient_id"],
        business_meaning="Primary hospital care quality and post-discharge efficacy metric"
    ),
    BusinessMetric(
        metric_id="metric_fin_margin",
        metric_name="Net Profit Margin",
        domain="Finance",
        definition="Percentage of net revenue remaining after operating expenses",
        formula="(SUM(revenue) - SUM(expenses)) / SUM(revenue) * 100",
        source_fields=["revenue", "expenses"],
        business_meaning="Core financial profitability metric"
    ),
    BusinessMetric(
        metric_id="metric_const_delay",
        metric_name="Project Delay Ratio",
        domain="Construction",
        definition="Average variance between planned milestone target and actual completion date",
        formula="MEAN(actual_days - planned_days)",
        source_fields=["actual_days", "planned_days"],
        business_meaning="Key schedule adherence and contract penalty indicator"
    ),
    BusinessMetric(
        metric_id="metric_hr_attrition",
        metric_name="Employee Attrition Rate",
        domain="HR",
        definition="Percentage of workforce leaving the organization within period",
        formula="COUNT(left_employees) / COUNT(total_employees) * 100",
        source_fields=["employee_status", "employee_id"],
        business_meaning="Human capital retention and organizational stability index"
    ),
    BusinessMetric(
        metric_id="metric_log_otd",
        metric_name="On-Time Delivery Rate (OTD)",
        domain="Logistics",
        definition="Percentage of shipments delivered within promised SLA window",
        formula="MEAN(delivered_on_time == 1) * 100",
        source_fields=["delivered_on_time", "shipment_id"],
        business_meaning="Supply chain reliability and customer satisfaction metric"
    )
]

for m in standard_metrics:
    MetricRegistry.register_metric(m)
