from agent_production_lite.models import AgentState, RiskLevel, Status, TaskRequest
from agent_production_lite.policy import decide
from agent_production_lite.service import validate_task


def test_specific_low_risk_request_is_allowed():
    request = TaskRequest(
        task_id="t1",
        input_data="Validate Invoice 1234 for Acme Corp",
        risk_level=RiskLevel.LOW,
    )
    decision = validate_task(request)
    assert decision.route == "ALLOW"
    assert decision.state.evidence


def test_high_risk_requires_human_approval():
    request = TaskRequest(
        task_id="t2",
        input_data="Validate Invoice 1234 for Acme Corp",
        risk_level=RiskLevel.HIGH,
    )
    assert validate_task(request).route == "HUMAN_APPROVAL"


def test_vague_request_routes_to_human_review():
    request = TaskRequest(task_id="t3", input_data="Review this record")
    decision = validate_task(request)
    assert decision.route == "HUMAN_REVIEW"
    assert decision.reason == "low_confidence"


def test_missing_required_evidence_routes_to_rework():
    request = TaskRequest(task_id="t4", input_data="x", requires_evidence=True)
    state = AgentState(status=Status.COMPLETE, confidence_score=0.95, evidence=[])
    decision = decide(request, state)
    assert decision.route == "REWORK"
    assert decision.reason == "missing_evidence"
