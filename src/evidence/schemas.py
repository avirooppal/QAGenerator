from typing import Literal, Union, Dict, Any, Optional
from pydantic import BaseModel, Field

class EvidenceBase(BaseModel):
    evidence_id: str
    chunk_id: str
    section: str
    source_text: str

class MetricEvidence(EvidenceBase):
    type: Literal["metric"] = "metric"
    metric_name: str
    value: Union[float, str]
    unit: Optional[str] = None

class RiskEvidence(EvidenceBase):
    type: Literal["risk"] = "risk"
    risk_factor: str
    impact: str

class SegmentEvidence(EvidenceBase):
    type: Literal["segment"] = "segment"
    segment_name: str
    metric_name: str
    value: Union[float, str]

class TableRowEvidence(EvidenceBase):
    type: Literal["table_row"] = "table_row"
    table_name: str
    row_data: Dict[str, Any]

class ComparisonEvidence(EvidenceBase):
    type: Literal["comparison"] = "comparison"
    metric_name: str
    value_current: Union[float, str]
    value_previous: Union[float, str]
    trend: str

# To allow Pydantic to cleanly discriminate:
EvidenceUnit = Union[
    MetricEvidence,
    RiskEvidence,
    SegmentEvidence,
    TableRowEvidence,
    ComparisonEvidence
]

class EvidenceUnitWrapper(BaseModel):
    unit: EvidenceUnit = Field(..., discriminator="type")
