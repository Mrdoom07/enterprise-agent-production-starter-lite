from enum import Enum
from pydantic import BaseModel, Field


class Status(str, Enum):
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class TaskRequest(BaseModel):
    task_id: str = Field(min_length=1, max_length=100)
    input_data: str = Field(max_length=5000)
    risk_level: RiskLevel = RiskLevel.LOW
    requires_evidence: bool = True
    action: str = Field(default="validate", min_length=1, max_length=100)
    resource_id: str | None = Field(default=None, max_length=200)
    operation_version: str = Field(default="v1", min_length=1, max_length=50)


class AgentState(BaseModel):
    status: Status
    confidence_score: float = Field(ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)
    extracted_entities: list[str] = Field(default_factory=list)


class IndependentValidation(BaseModel):
    score: float = Field(ge=0.0, le=1.0)
    resource_resolved: bool
    resolved_resource_id: str | None = None
    reasons: list[str] = Field(default_factory=list)


class Decision(BaseModel):
    task_id: str
    route: str
    reason: str
    state: AgentState
    validation: IndependentValidation
    idempotency_key: str | None = None
