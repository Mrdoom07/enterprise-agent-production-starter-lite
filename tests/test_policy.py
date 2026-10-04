from agent_production_lite.audit import clear_records, list_records
from agent_production_lite.idempotency import build_resource_idempotency_key
from agent_production_lite.models import (
    AgentState,
    IndependentValidation,
    RiskLevel,
    Status,
    TaskRequest,
)
from agent_production_lite.policy import decide
from agent_production_lite.service import validate_task


def test_specific_low_risk_request_is_allowed():
    clear_records()
    request = TaskRequest(
        task_id="t1",
        input_data="Validate Invoice 1234 for Acme Corp",
        risk_level=RiskLevel.LOW,
    )
    decision = validate_task(request)
    assert decision.route == "ALLOW"
    assert decision.state.evidence
    assert decision.validation.resource_resolved is True
    assert decision.validation.resolved_resource_id == "1234"
    assert decision.idempotency_key


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
    assert decision.reason == "independent_validation_failed"


def test_missing_required_evidence_routes_to_rework():
    request = TaskRequest(
        task_id="t4",
        input_data="Review resource 1234",
        resource_id="1234",
        requires_evidence=True,
    )
    state = AgentState(status=Status.COMPLETE, confidence_score=0.99, evidence=[])
    validation = IndependentValidation(
        score=1.0,
        resource_resolved=True,
        resolved_resource_id="1234",
    )
    decision = decide(request, state, validation)
    assert decision.route == "REWORK"
    assert decision.reason == "missing_evidence"


def test_idempotency_key_is_resource_scoped_not_task_scoped():
    first = TaskRequest(
        task_id="task-a",
        input_data="Validate Invoice 1234",
        resource_id="1234",
        action="validate",
    )
    retry = TaskRequest(
        task_id="task-b",
        input_data="Validate Invoice 1234 again",
        resource_id="1234",
        action="validate",
    )
    different_resource = TaskRequest(
        task_id="task-c",
        input_data="Validate Invoice 9999",
        resource_id="9999",
        action="validate",
    )

    first_key = build_resource_idempotency_key(first, first.resource_id)
    retry_key = build_resource_idempotency_key(retry, retry.resource_id)
    other_key = build_resource_idempotency_key(
        different_resource,
        different_resource.resource_id,
    )

    assert first_key == retry_key
    assert first_key != other_key


def test_allow_decisions_are_recorded_in_audit_log():
    clear_records()
    request = TaskRequest(
        task_id="audit-1",
        input_data="Validate Invoice 1234 for Acme Corp",
    )
    decision = validate_task(request)
    assert decision.route == "ALLOW"

    records = list_records()
    assert len(records) == 1
    assert records[0]["route"] == "ALLOW"
    assert records[0]["resource_id"] == "1234"
    assert records[0]["idempotency_key"] == decision.idempotency_key
